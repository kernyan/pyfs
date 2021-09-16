# util module for fat file system

# read BPB (BIOS parameter block)
# calculate reserved sector
# calculate FAT sector
# parse root directory
# read file


# linux/include/uapi/linux/msdos_fs.h

'''
struct fat_boot_sector {
	__u8	ignored[3];	/* Boot strap short or near jump */
	__u8	system_id[8];	/* Name - can be used to special case
				   partition manager volumes */
	__u8	sector_size[2];	/* bytes per logical sector */
	__u8	sec_per_clus;	/* sectors/cluster */
	__le16	reserved;	/* reserved sectors */
	__u8	fats;		/* number of FATs */
	__u8	dir_entries[2];	/* root directory entries */
	__u8	sectors[2];	/* number of sectors */
	__u8	media;		/* media code */
	__le16	fat_length;	/* sectors/FAT */
	__le16	secs_track;	/* sectors per track */
	__le16	heads;		/* number of heads */
	__le32	hidden;		/* hidden sectors (unused) */
	__le32	total_sect;	/* number of sectors (if sectors == 0) */
'''

import struct


class BPH:
    header = ['ignored', 'system_id', 'sector_size', 'sec_per_clus',
              'reserved', 'fats', 'dir_entries', 'sectors', 'media',
              'fat_length', 'secs_track', 'heads', 'hidden', 'total_sect']

    header_fmt = '<3s8sHBHBHHBHHHII'

    def __init__(self, path):
        with open(path, 'rb') as f:
            self.boot_sector = f.read(512)
            a = dict(zip(self.header, struct.unpack(self.header_fmt, self.boot_sector[:36])))
            for each in a:
                print('{:15} {}'.format(each, a[each]))


def walk(path: str):
    a = BPH(path)


