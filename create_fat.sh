#! /bin/bash

# from https://unix.stackexchange.com/questions/629492/create-and-populate-fat32-filesystem-without-mounting-it

if [ ! -f example1.txt ]; then
  echo $'test123\nrow2\r\nrow3' > example1.txt
fi

if [ ! -f example2.txt ]; then
  echo $'#$SAH1227&^S\nrow2\r\nrow3' > example2.txt
fi

if [ ! -f example3.txt ]; then
  echo $'iamindirectory\nrow2\r\nrow3' > example3.txt
fi

dd if=/dev/zero of=disk.img bs=1M count=2
mformat -i disk.img ::
mcopy -i disk.img example1.txt example2.txt ::
mmd -i disk.img ::something
mcopy -i disk.img example3.txt ::something
mdir -i disk.img
#mcopy -i disk.img ::/example1.txt extracted1.txt


