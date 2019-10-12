#!/usr/bin/env python
#==========================================
# Author: Will Fenton and Giancarlo Pernudi
# Date: October 11 2019
#==========================================

import hashlib
import sys
import os
import getopt
from PIL import Image, ImageFilter
from bitstring import BitArray

#==========================================

def printUsage():
    sys.stderr.write(
        "Usage: ./sectors.py [options] <string>...\n"
        "Options:\n"
        "  (-s | --size) <pixels>       the size of the image in pixels, creates square image [default: 256]\n"
        "  (-b | --blur) <strength>     the blur strength of the image [default: 2]\n"
        "  (-f | --hash-function) <MD5 | SHA-256 | SHA 512>\n"
        "                               hash function to use [default: SHA-512]\n"
        "  -h, --help                   show this screen\n")

#==========================================

def main():

    pipe = []
    if not sys.stdin.isatty():
        pipe = sys.stdin.readlines()
    pipe = [x.strip() for x in pipe]

    if len(sys.argv) == 1 and len(pipe) == 0:
        printUsage()
        sys.exit(1)

    # read options
    try:
        options = "hf:s:b:"
        longOptions = ["help", "hash-function=", "size=", "blur="]
        opts, args = getopt.getopt(sys.argv[1:], options, longOptions)
    except getopt.GetoptError:
        printUsage()
        sys.exit(1)

    hash_function = "SHA-512"
    size = 256
    blur = 2

    # parse options
    for o, v in opts:
        if o in ("-h", "--help"):
            printUsage()
            sys.exit()
        if o in ("-f", "--hash-function"):
            hash_function = v
        if o in ("-s", "--size"):
            size = int(v)
        if o in ("-b", "--blur"):
            blur = int(v)

    if len(args) == 0 and len(pipe) == 0:
        raise Exception("Need to specify a string")

    try:
        os.mkdir("output")
    except FileExistsError:
        pass

    # generate identicons for all strings
    for string in pipe:
        generate_identicon(string, hash_function, size, blur)
    for string in args:
        generate_identicon(string, hash_function, size, blur)



#==========================================

def map_val(val, min, max):
    # returns val of 0-255 between min-max
    return int((val / 255) * (max - min) + min)

def generate_identicon(string, hash_function, size, blur):

    if hash_function == "MD5":
        hash = hashlib.md5()
    elif hash_function == "SHA-256":
        hash = hashlib.sha256()
    elif hash_function == "SHA-512":
        hash = hashlib.sha512()
    else:
        raise Exception("Invalid hash function")

    hash.update(bytes(string, encoding="utf-8"))

    hex_digest = hash.hexdigest()

    print(f"String: {string}")
    print(f"{hash_function} Hash: {hex_digest}")

    byte_digest = hash.digest()

    num_bytes = hash.digest_size
    assert(num_bytes % 4 == 0)

    num_sectors = num_bytes // 3

    points = []
    colours = []

    saturation = map_val(int(byte_digest[-1]), 160, 210)
    brightness = map_val(int(byte_digest[-2]), 200, 255)

    # Get point coordinates and colours from the hash digest
    point_bytes = byte_digest[:num_sectors*2]
    for i in range(num_sectors):
        x_coord = point_bytes[i*2]
        y_coord = point_bytes[(i*2)+1]
        points.append((map_val(x_coord, 0, size), map_val(y_coord, 0, size)))

    colour_bytes = byte_digest[num_sectors*2:num_sectors*3]
    for i in range(num_sectors):
        c = colour_bytes[i]
        colours.append((int(c), saturation, brightness))

    # for i in range(num_sectors):
        # print(f"Sector {i+1}: Point={points[i]}, Colour={colours[i]}")

    # Create image
    image = Image.new("HSV", (size, size), (255, 255, 255))

    for x in range(size):
        for y in range(size):
            min_squared_dist = (256 ** 2) * 2
            colour = (0, 0, 0)
            for i in range(num_sectors):
                point = points[i]
                squared_dist = ((x - point[0]) ** 2) + ((y - point[1]) ** 2)
                if squared_dist < min_squared_dist:
                    min_squared_dist = squared_dist
                    colour = colours[i]
            image.putpixel((x, y), colour)

    image = image.convert("RGB")
    image = image.filter(ImageFilter.BoxBlur(blur))
    image.save(f"output/{string}.png", "PNG")

    print(f"Identicon saved to ./output/{string}.png")

#==========================================

if __name__ == "__main__":
    main()

#==========================================
