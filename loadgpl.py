#!/bin/env python3
# Loads a GIMP palette file (gpl) into an indexed image
# This needs https://github.com/drj11/pypng
import png
from PIL import Image
import re
import os
import sys

color = re.compile('^\s*(\d{1,3})\s+(\d{1,3})\s+(\d{1,3}).*$')

# manage command line arguments
if len(sys.argv) == 1 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("./loadgpl.py image.png palette.gpl [output.png]")
    exit(0)

filename = sys.argv[1]
if filename.split('.')[-1] != 'png':
    print("Please give a .png file", file=sys.stderr)
    exit(1)

palettefile = sys.argv[2]
if palettefile.split('.')[-1] != 'gpl':
    print("Please give a .gpl file", file=sys.stderr)
    exit(1)

if len(sys.argv) >= 4:
    output = sys.argv[3]
    if output.split('.')[-1] != 'png':
        print("Please give a .png file", file=sys.stderr)
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

# write new image
w = png.Writer(original[0], original[1], palette=palette, bitdepth=8)
f = open(output, 'wb')
w.write(f, original[2])
f.close()

print('Wrote to ' + output)