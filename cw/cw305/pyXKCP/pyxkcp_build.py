#!/usr/bin/env python3
# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import os

from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef("""
typedef uint8_t BitSequence;
typedef size_t BitLength;
int cSHAKE128( const BitSequence *input, BitLength inputBitLen, BitSequence *output, BitLength outputBitLen, const BitSequence *name, BitLength nameBitLen, const BitSequence *customization, BitLength customBitLen );
int cSHAKE256( const BitSequence *input, BitLength inputBitLen, BitSequence *output, BitLength outputBitLen, const BitSequence *name, BitLength nameBitLen, const BitSequence *customization, BitLength customBitLen );
int KMAC128(const BitSequence *key, BitLength keyBitLen, const BitSequence *input, BitLength inputBitLen, BitSequence *output, BitLength outputBitLen, const BitSequence *customization, BitLength customBitLen);
int KMAC256(const BitSequence *key, BitLength keyBitLen, const BitSequence *input, BitLength inputBitLen, BitSequence *output, BitLength outputBitLen, const BitSequence *customization, BitLength customBitLen);
""")

ffibuilder.set_source(
    "_xkcp",  # name of the output C extension
    """
    #include "../vendor/xkcp_xkcp/align.h"
    #include "../vendor/xkcp_xkcp/Phases.h"
    #include "../vendor/xkcp_xkcp/KeccakSponge.h"
    #include "../vendor/xkcp_xkcp/SP800-185.h"
    #include "../vendor/xkcp_xkcp/KeccakP-1600-SnP.h"
    #include "../vendor/xkcp_xkcp/SnP-Relaned.h"
    #include "../vendor/xkcp_xkcp/brg_endian.h"

""",
    sources=[
        '../vendor/xkcp_xkcp/SP800-185.c',
        '../vendor/xkcp_xkcp/KeccakSponge.c',
        '../vendor/xkcp_xkcp/KeccakP-1600-compact64.c'
    ],
    libraries=[])


def create_config_file():
    with open('../vendor/xkcp_xkcp/config.h', 'w') as the_file:
        the_file.write('// Copyright lowRISC contributors\n')
        the_file.write(
            '// Licensed under the Apache License, Version 2.0, see LICENSE for details.\n'
        )
        the_file.write('// SPDX-License-Identifier: Apache-2.0 \n\n')
        the_file.write('// This file is autogenerated by ' + __file__ +
                       '\n// DO NOT CHANGE!\n\n')
        # Define which KeccakPermutation is used
        the_file.write('#define XKCP_has_KeccakP1600\n')
        the_file.close()


def initialize():
    cw = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    if not os.path.exists("_xkcp.o"):
        print("Building xkcp-extension")
        create_config_file()
        ffibuilder.compile(verbose=False)
    os.chdir(cw)


if __name__ == "__main__":
    create_config_file()
    ffibuilder.compile(verbose=True)
