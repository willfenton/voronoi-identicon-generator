# Identicon

This is a short one-day project to make an Identicon generator (see https://github.com/drhus/awesome-identicons).

Versions:
1. identicon.py - outputs a simple ascii image based on a SHA-256 hash
2. randomart.py - implements the OpenSSH ascii fingerprint algorithm
3. identicon.pde - recursively colors rectangles based on a string seed
4. sectors_rgb.py - uses nearest neighbors algorithm to generate an unique image based on a SHA-256 hash
5. sectors.py - same as sectors_rgb.py but uses HSV for nicer colors (and some nice features like command line input)
