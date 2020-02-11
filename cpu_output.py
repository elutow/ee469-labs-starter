#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import struct

"""Functions to parse output from the TinyFPGA USB port"""

# Adjust this to be the number of bytes from the debug port
DEBUG_BYTES = 7

def _io_unpack(struct_format, buf):
    """Reads from io.BytesIO with format according to struct_format"""
    size = struct.calcsize(struct_format)
    data = buf.read(size)
    return struct.unpack(struct_format, data)

def parse_cycle_output(cycle_count, cycle_output):
    """Parse one cycle output"""

    if int.from_bytes(cycle_output, 'little') == 0:
        # Hack to wait for initialization
        print('Waiting...')
        return

    buf_io = io.BytesIO(cycle_output)

    # Example of decoding: arg1, arg2, arg3 = _io_unpack('>I2B', buf_io)
    # See Python docs for format: https://docs.python.org/3/library/struct.html#format-strings

    print("ERROR: CPU output decoding is not implemented!")
