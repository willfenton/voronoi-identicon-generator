# Identicon
## Authors: Will Fenton & Giancarlo Pernudi Segura

This is a short one-day project to make an Identicon generator (see [drhus/awesome-identicons](https://github.com/drhus/awesome-identicons)).

### Versions

`identicon.py`
+ outputs a simple ascii image based on a SHA-256 hash

`randomart.py`
+ implements the OpenSSH ascii fingerprint algorithm

`identicon.pde`
+ recursively colors rectangles based on a string seed

`sectors_rgb.py`
+ uses nearest neighbors algorithm to generate an unique image based on a SHA-256 hash

`sectors.py`
+ same as sectors_rgb.py but uses HSV for nicer colors (and some nice features like command line input)
+ Uasge: `./sectors.py <string>...`
+ images are saved in `output/` folder


### Examples

gino:
![gino.png](gino.png "gino.png")

will:
![will.png](will.png "will.png")

yeet:
![yeet.png](yeet.png "yeet.png")

💯:
![💯.png](💯.png "💯.png")
