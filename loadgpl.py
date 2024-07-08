#!/bin/env python3
#Copyright (c) 2020-2024, Basxto
#All rights reserved.
#
#This source code is licensed under the MIT license found in the
#LICENSE file in the root directory of this source tree.

# Loads a GIMP palette file (gpl) into an indexed image
# This needs https://github.com/drj11/pypng
import png
from PIL import Image
import re
import os
import sys
import argparse

color = re.compile('^\\s*(\\d{1,3})\\s+(\\d{1,3})\\s+(\\d{1,3}).*$')

parser = argparse.ArgumentParser(
                    description='Loads Gimp palette (.gpl) into an indexed PNG with support for subpalettes and shared colors')
parser.add_argument('input',
                    help='input indexed PNG')
parser.add_argument('palette',
                    help='Gimp palette (.gpl)')
parser.add_argument('output', nargs='?',
                    help='output indexed PNG instead of overwriting input')
parser.add_argument('-c', '--colors', type=int, nargs='?', const=4, default=4,
                    help='Amount of colors per subpalette (default: 4)')
parser.add_argument('-s', '--shared', type=int, nargs='?', const=0, default=0,
                    help='Amount of colors shared by all subpalettes (default: 0)')
parser.add_argument('-u', '--subpalette', type=int,
                    help='Replace specified subpalette (starts with 1)')

args = parser.parse_args()

filename = args.input
if filename.split('.')[-1] != 'png':
    print("Please give a .png file as input", file=sys.stderr)
    exit(1)

palettefile = args.palette
if palettefile.split('.')[-1] != 'gpl':
    print("Please give a .gpl file", file=sys.stderr)
    exit(1)

if args.output:
    output = args.output
    if output.split('.')[-1] != 'png':
        print("Please give a .png file as output", file=sys.stderr)
        exit(1)
else:
    split = filename.split('.')
    split[0] += '_' + os.path.basename(palettefile).split('.')[0]
    output = '.'.join(split)

# get palette
palette = []
with open(palettefile) as f:
    content = f.readlines()
    for c in content:
        match = color.match(c)
        if match:
            palette.append((int(match.group(1)),int(match.group(2)),int(match.group(3))))

# read original image
r=png.Reader(filename=filename)
original = r.read()

# mix palettes
if args.subpalette >= 1:
    palettenew = r.palette()
    subcolors = args.colors - args.shared
    spbase = (args.subpalette - 1) * (args.colors - args.shared)
    for i in range(0, args.shared):
        palettenew[i] = palette[i]
    for i in range(args.shared, args.colors):
        palettenew[spbase + i] = palette[i]
    palette = palettenew

# write new image
w = png.Writer(original[0], original[1], palette=palette, bitdepth=8)
f = open(output, 'wb')
w.write(f, original[2])
f.close()

print('Wrote to ' + output)