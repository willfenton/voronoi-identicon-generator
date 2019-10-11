#==========================================
# Author: Will Fenton
# Date: October 10 2019
#==========================================

import hashlib

#==========================================

# dont judge my trash code right now im so tired

string = "yeet"

hash = hashlib.sha256()

hash.update(bytes(string, encoding="utf-8"))

hash_value = hash.hexdigest()

chars = [' ', 'x', 'o', '@', '#', '%', '*', '+', '~', '=', '&', '<', '>', '?', '-', '$']

print()
print(f"String: {string}")
print(f"SHA-256 Hash: {hash_value}")
print(" -------------------")
for i in range(8):
    print(' | ', end='')
    s = hash_value[8*i:8*(i+1)]
    for j in range(8):
        print(chars[int(s[j], base=16)] + ' ', end='')
    print('|')
print(" -------------------")
print()