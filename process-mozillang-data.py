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
pinyin_possiblities = set()

pinyin2hanzi = {}

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
    pinyin_possiblities.update(pinyin)
    word = bytearray.fromhex(code).decode("utf-16be")
    print(word, pinyin)
    for yin in pinyin:
      if yin not in pinyin2hanzi:
        pinyin2hanzi[yin] = set((word,))
      else:
        pinyin2hanzi[yin].add(word)

if unnormalized_letters:
  print("WARNING: special cases found!", sorted(unnormalized_letters))
print(pinyin_possiblities)
print(pinyin2hanzi)
