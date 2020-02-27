import cocotb

from cpu_output import DEBUG_BYTES, parse_cycle_output

from _tests_common import init_posedge_clk

# Number of CPU clock cycles to run
NUM_CYCLES = 42

@cocotb.test()
async def test_cpu(dut):
    """Run cpu normally and process debug port outputs"""

    clkedge = init_posedge_clk(dut.cpu_clk)

    # Reset CPU
    dut.cpu_nreset <= 0
    await clkedge
    dut.cpu_nreset <= 1
    await clkedge
    dut._log.debug('Reset complete')

    print("===========BEGIN PARSED DEBUG PORT OUTPUT===========")
    for cycle_count in range(NUM_CYCLES):
        dut._log.debug(f'Running CPU cycle {cycle_count}')
        # TODO: Combine cpu_debug_port* into a single signal of DEBUG_BYTES long
        # This will require some modifications to the top module
        debug_port_bytes = dut.cpu_debug_port1.value.integer.to_bytes(DEBUG_BYTES, 'big')
        debug_port_bytes += dut.cpu_debug_port2.value.integer.to_bytes(DEBUG_BYTES, 'big')
        debug_port_bytes += dut.cpu_debug_port3.value.integer.to_bytes(DEBUG_BYTES, 'big')
        debug_port_bytes += dut.cpu_debug_port4.value.integer.to_bytes(DEBUG_BYTES, 'big')
        debug_port_bytes += dut.cpu_debug_port5.value.integer.to_bytes(DEBUG_BYTES, 'big')
        debug_port_bytes += dut.cpu_debug_port6.value.integer.to_bytes(DEBUG_BYTES, 'big')
        debug_port_bytes += dut.cpu_debug_port7.value.integer.to_bytes(DEBUG_BYTES, 'big')
        parse_cycle_output(cycle_count, debug_port_bytes)
        await clkedge
    print("===========END PARSED DEBUG PORT OUTPUT===========")
