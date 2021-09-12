#! /usr/bin/env python3

import fs
import os

def walk(img):
  out = []
  a = fs.open_fs("fat://" + img)

  for path in a.walk.files():
    out.append(path)
  return out

if __name__ == '__main__':
  img = 'disk.img'
  print('ls %s\n' % img, walk(img))
  

