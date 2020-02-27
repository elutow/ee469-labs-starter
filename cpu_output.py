#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import struct

"""Functions to parse output from the TinyFPGA USB debug port"""

# Adjust this to be the number of bytes from the debug port
DEBUG_BYTES = 7

# Helper methods

def _io_unpack(struct_format, buf):
    """Reads from io.BytesIO with format according to struct_format"""
    size = struct.calcsize(struct_format)
    data = buf.read(size)
    return struct.unpack(struct_format, data)

def _io_read_by_bitcount(struct_format, buf_io, *args):
    """
    Read multiple values from a single value and returns a tuple of those values

    Example: fourbits, twobits, sixbits, thirteenbits = _io_read_by_bitcount('>I', buf_io, 4, 2, 6, 13)

    args specifies a sequence of bit counts
    """
    assert args
    orig_value, = _io_unpack(struct_format, buf_io)
    results = list()
    for bitcount in reversed(args):
        results.append(orig_value % (1 << bitcount))
        orig_value >>= bitcount
    return tuple(reversed(results))

# Public functions

def parse_cycle_output(cycle_count, cycle_output):
    """Parse one cycle output"""

    if int.from_bytes(cycle_output, 'little') == 0:
        # Hack to wait for initialization
        print('Waiting...')
        return

    buf_io = io.BytesIO(cycle_output)

    # Example of decoding: arg1, arg2, arg3 = _io_unpack('>I2B', buf_io)
    # See Python docs for format: https://docs.python.org/3/library/struct.html#format-strings

    print('raw:', cycle_output.hex())
