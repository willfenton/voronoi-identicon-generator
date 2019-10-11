#==========================================
# Author: Will Fenton
# Date: October 11 2019
#==========================================

import hashlib
from PIL import Image
from bitstring import BitArray
import sys

#==========================================

string = sys.argv[1]

hash = hashlib.sha256()

hash.update(bytes(string, encoding="utf-8"))

hex_digest = hash.hexdigest()

print(f"String: {string}")
print(f"SHA-256 Hash: {hex_digest}")

byte_digest = hash.digest()

num_bytes = hash.digest_size
assert(num_bytes % 4 == 0)

num_sectors = num_bytes // 4

points = []
colours = []

# Get point coordinates and colours from the hash digest
point_bytes = byte_digest[:num_sectors*2]
for i in range(num_sectors):
    x_coord = point_bytes[i*2]
    y_coord = point_bytes[(i*2)+1]
    points.append((x_coord, y_coord))

colour_bytes = byte_digest[num_sectors*2:]
for i in range(num_sectors):
    c = BitArray(colour_bytes[i*2:(i*2)+2])
    red = c[:5]
    green = c[5:11]
    blue = c[11:]
    colours.append((red.uint * 8, green.uint * 4, blue.uint * 8))

for i in range(num_sectors):
    print(f"Sector {i+1}: Point={points[i]}, Colour={colours[i]}")

# Create image
image = Image.new("RGB", (256, 256), (255, 255, 255))

for x in range(256):
    for y in range(256):
        min_squared_dist = (256 ** 2) * 2
        colour = (0, 0, 0)
        for i in range(num_sectors):
            point = points[i]
            squared_dist = ((x - point[0]) ** 2) + ((y - point[1]) ** 2)
            if squared_dist < min_squared_dist:
                min_squared_dist = squared_dist
                colour = colours[i]
        image.putpixel((x, y), colour)

image.save(f"{string}.png", "PNG")
