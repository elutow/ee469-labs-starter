# UW ECE/CSE 469 Labs and Final Project

This repository contains the code for the UW EE/CSE 469 Labs and Final Project.

This branch contains the modified lab starter code to work with [my forked apio](https://github.com/elutow/apio). The parent branch is `upstream`.

## Setup

Requirements:

* Either Linux for x86-64 (amd64) or macOS. (Help wanted to support other platforms!)
* Python 3
* TinyFPGA BX

Steps:

1. Clone this repo: `git clone https://github.com/elutow/ee469-labs-starter`
	* NOTE: If you have existing code, you should copy them into this repo. This repo modifies some files like `SConstruct` to work with [the forked apio](https://github.com/elutow/apio).
2. Follow instructions for setting up Python, up until the `pip install` command: https://tinyfpga.com/bx/guide.html
3. (Optional, but highly recommended) Setup [virtualenv](https://virtualenv.pypa.io/en/latest/) or [venv](https://docs.python.org/3/library/venv.html). Then, activate the virtualenv/venv.
	* NOTE: This will break Atom's `apio-ide`, so you will need to use the command-line instead (i.e. `apio build`, `apio upload`, etc.)
4. `pip3 install -r requirements.txt`
5. Continue following the user guide instructions after the `pip install` command: https://tinyfpga.com/bx/guide.html
6. If you are setting up Atom, install `apio-ide` by typing in `FPGAwars/apio-ide` and selecting to download from git. This will fix any `apio` version incompatibility warnings.

## Uploading to FPGA

For command-line:

```sh
apio build
apio upload
```

Alternatively, you can use Atom with `apio-ide`.

## Testing

Requirements:

1. Install dependencies for cocotb: https://cocotb.readthedocs.io/en/latest/quickstart.html#native-linux-installation
2. Install GTKwave. For Debian/Ubuntu: `# apt install gtkwave`

Tests are written in cocotb with the Verilator backend. To run the cocotb tests:

```sh
apio verify
```

To show the waveform from the tests (requires GTKwave to be installed):

```sh
apio sim
```

## Development Notes

### Tips

* Use `apio lint`, `apio verify`, and `apio build --verbose-yosys` often to validate your design

### Writing cocotb tests

All cocotb tests live in `tests` with the suffix `_cocotb.py`. The file `tests/cpu_cocotb.py` contains a test that simulates running the FPGA and processing the USB debug port output.

At this time, there are some caveats with cocotb + Verilator:

* All tests run back-to-back, so any values written or signals set will stay until the test is done.
* The `dut` is actually `cocotb_dut`, which is an auto-generated Verilog file stored in `tests/gen/cocotb_dut.sv`. It automatically finds all modules defined in `.sv` files inside `cpu` and attaches them with all their signals to `cocotb_dut`. All signal names are prefixed with the module name.
* You can only access top-level signals; no access to internal submodules or signals. See the section [Debugging internal signals](#debugging-internal-signals) below for workarounds.
* `cocotb_dut` is generated with `tests/generate_cocotb_dut.py`, which has some additional restrictions on how you write your modules:
	* There must be exactly one module per `.sv` file; otherwise the first one is used.
	* All I/O must be within the parenthesis of `module NAME(...)`
	* I/O entries of the same type cannot be grouped, e.g. `input one, two` is not supported

cocotb also supports a number of other simulators including ModelSim and IVerilog, but the code here supports only Verilator.

cocotb documentation: https://cocotb.readthedocs.io/en/latest/quickstart.html#creating-a-test

### Debugging internal signals

There are two ways to debug internal signals with cocotb + Verilator:

1. Use `apio sim`. The waveform is produced from running all cocotb tests back-to-back.
2. Use SystemVerilog `$display`, `$error`, and `assert` (immediate assertions only) statements in your Verilog code. This code configures Verilator to check these assertions while cocotb tests are running. However, since yosys doesn't support these statements\*, you will want to guard your checks like so:

	```verilog
	`ifndef SYNTHESIS
		$display("Hello world!");
		assert(2'b10 + 2'b10 == 2'b100) else begin
			$error("Oh no");
		end
	`endif // SYNTHESIS
	```

	You can place these anywhere, such as inside `initial`, `always_comb` or `always_ff` blocks.

\* yosys technically does support these statements with the `-formal` flag, but it's not very useful without something like SymbiYosys installed (a formal verification tool).

### Increase synthesis verbosity

To get verbose compilation & synthesis output during builds (and statistics of FPGA resources used), add the `--verbose-yosys` flag to `apio build`.

To get verbose place & route output during builds, add the `--verbose-nextpnr` flag to `apio build`.
