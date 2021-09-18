#! /usr/bin/env python3

import util

if __name__ == '__main__':

  img = 'disk32.img'

  F = ['EXAMPLE1.TXT', 'EXAMPLE2.TXT', 'AAA.TXT', 'something/EXAMPLE3.TXT']

  b = util.open_fs(img)

  for fn in F:
      print(fn)
      print(b.open(fn).read(), '\n')
