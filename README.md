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

## Development Notes

To get verbose place & route output during builds, use the following:

```sh
apio build --verbose-nextpnr
```
