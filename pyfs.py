#! /usr/bin/env python3

import util

if __name__ == '__main__':

  img = 'disk32.img'

  file = 'AAA.TXT'

  b = util.open_fs(img)

  print(b.open(file).read())
