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

if [ ! -f aaa.txt ]; then
  python3 -c "print('A'*512+'B'*512+'C'*6)" >> aaa.txt
fi

# create FAT32 disk
dd if=/dev/zero of=disk32.img bs=1M count=33
mformat -F -i disk32.img ::
mcopy -i disk32.img example1.txt example2.txt ::
mmd -i disk32.img ::something
mcopy -i disk32.img example3.txt ::something
mcopy -i disk32.img aaa.txt ::
mdir -i disk32.img
