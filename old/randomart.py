#==========================================
# Author: Will Fenton
# Date: October 10 2019
# OpenSSH fingerprint visualization algorithm
#==========================================

import hashlib

#==========================================

# dont judge my trash code right now im so tired

class Tile:
    def __init__(self):
        self.char = ' '
        self.n = 0

def print_tiles(tiles):
    print(" +-----------------+")
    for i in range(9):
        print(" |", end='')
        for j in range(17):
            print(tiles[j][i].char, end='')
        print('|')
    print(" +-----------------+")


string = "yeet"

hash = hashlib.md5()

hash.update(bytes(string, encoding="utf-8"))

digest = hash.hexdigest()

chars = [' ','.','o','+','=','*','B','O','X','@','%','&','#','/','^']
start_char = 'S'
end_char = 'E'

width = 17
height = 9

tiles = [[Tile() for y in range(height)] for x in range(width)]

x = 8
y = 4

tiles[x][y].n += 1


byte_digest = hash.digest()

moves = []

for i in range(len(byte_digest)):
    for pair in range(4):
        move = (byte_digest[i] >> 2*pair) & 3
        moves.append(move)

for move in moves:
    if move == 0:
        x = max(x-1, 0)
        y = max(y-1, 0)
    elif move == 1:
        x = min(x+1, 16)
        y = max(y-1, 0)
    elif move == 2:
        x = max(x-1, 0)
        y = min(y+1, 8)
    elif move == 3:
        x = min(x+1, 16)
        y = min(y+1, 8)
    tiles[x][y].n += 1
    tiles[x][y].char = chars[tiles[x][y].n]

tiles[8][4].char = start_char
tiles[x][y].char = end_char

print()
print(f"String: {string}")
print(f"MD5 Hash: {digest}")
print_tiles(tiles)
print()