# pyfs

Python implementation of filesystem

## FAT32
[x] read BIOS parameter block (BPB)
[x] recursive read directory
[x] read file spanning multiple sectors
[x] long file name

## Usage
```python
import util
fs = util.open_fs('disk32.img')
fs.open('something/EXAMPLE3.TXT').read()
```
