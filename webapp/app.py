from flask import Flask, render_template, send_file, redirect, url_for, Response
import os
import pathlib
import json
import sys
import hashlib
from bitstring import BitArray
from PIL import Image, ImageFilter


app = Flask(__name__, static_folder=os.path.join(os.getcwd(), "static"))


def map_val(val, min, max):
    # returns val of 0-255 between min-max
    return int((val / 255) * (max - min) + min)


def generate_identicon(string, hash_function="SHA-512", size=512, blur=0):
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

    # Create image
    image = Image.new("HSV", (size, size), (255, 255, 255))

    for x in range(size):
        for y in range(size):
            min_squared_dist = (size ** 2) * 2
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

    image_dir = f"static/images/{hash_function}/{size}/{blur}"
    image_path = f"{image_dir}/{string}.png"
    
    os.makedirs(image_dir, exist_ok=True)

    image.save(image_path, "PNG")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/identicons/<string:hash_algorithm>/<int:image_size>/<int:blur_strength>/<string:identicon_string>")
def get_identicon(hash_algorithm, image_size, blur_strength, identicon_string):
    identicon_path = f"static/images/{hash_algorithm}/{image_size}/{blur_strength}/{identicon_string}.png"

    if not os.path.exists(identicon_path):
        generate_identicon(identicon_string, hash_algorithm, image_size, blur_strength)

    return json.dumps({
        "image_url": identicon_path
    })


if __name__ == "__main__":
    app.run(debug=True)