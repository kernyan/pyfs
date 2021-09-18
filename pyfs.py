#! /usr/bin/env python3

import fs
import util

def walk(img):
  out = []
  a = fs.open_fs("fat://" + img)

  for path in a.walk.files():
    out.append(path)
  return out

if __name__ == '__main__':
  img = 'disk32.img'

  #file = '/something/EXAMPLE3.TXT'
  file = 'AAA.TXT'

  a = fs.open_fs("fat://" + img)
  b = util.open_fs(img)

  #print('ls %s\n' % img, walk(img))

  #print(a.open(file).read())
  print(b.open(file).read())
  #print('ls %s\n' % img, util.ls(img))
