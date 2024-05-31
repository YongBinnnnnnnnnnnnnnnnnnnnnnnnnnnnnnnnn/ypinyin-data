#!/usr/bin/env -S python3 -B

import argparse
import os
import socket
import struct
import subprocess
import sys
import unicodedata

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
    pinyin = unicodedata.normalize('NFKD', pinyin)
    pinyin = pinyin.split(',')
    print(code, pinyin)
