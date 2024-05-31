#!/usr/bin/env -S python3 -B

import argparse
import os
import socket
import struct
import subprocess
import sys

sys.path.append('libs/ypinyin-python')
from ypinyin import normalize_pinyin

unnormalized_letters = set()
pinyin_possibilities = set()

pinyin2hanzi = {}

mozillang_normalized = ""

with open("mozillang-source/pinyin-data/pinyin.txt", "r") as f:
  while True:
    line = f.readline()
    if not line:
      break
    #print(line[0],line[2],line[7])
    if line[0] == '#' or line[2] == 'E':
      continue
    if line[6] != ':':
      continue
    code = line[2:6]
    pinyin = line[8:].split(' ')[0]
    pinyin = normalize_pinyin(pinyin)
    for x in pinyin:
      if x == ",":
        continue
      if x >= "a" and x <= "z":
        continue
      if x in u_letters:
        continue
      unnormalized_letters.add(x)
    pinyin = pinyin.split(',')
    pinyin_possibilities.update(pinyin)
    word = bytearray.fromhex(code).decode("utf-16be")
    line = word + " " + ",".join(set(pinyin))
    print(line)
    mozillang_normalized = mozillang_normalized + line + "\n"

    for yin in pinyin:
      if yin not in pinyin2hanzi:
        pinyin2hanzi[yin] = set((word,))
      else:
        pinyin2hanzi[yin].add(word)

if unnormalized_letters:
  print("WARNING: special cases found!", sorted(unnormalized_letters))
#print(pinyin_possibilities)
with open("data/pinyin_possibilities.txt", "w") as f:
  f.write(" ".join(pinyin_possibilities))

#print(pinyin2hanzi)
with open("data/pinyin2hanzi.txt", "w") as f:
  for k, v in pinyin2hanzi.items():
    f.write(k + " " + ",".join(v) + "\n")

with open("data/mozillang_normalized.txt", "w") as f:
  f.write(mozillang_normalized)
