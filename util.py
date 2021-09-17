# util module for fat file system

# read BPB (BIOS parameter block)
# calculate reserved sector
# calculate FAT sector
# parse root directory
# read file



import struct

def ppd(dat: dict): # pretty print dict
    for each in dat:
        print('{:15} {}'.format(each, dat[each]))


class BPH:
    bph_header = ['ignored', 'system_id', 'sector_size', 'sec_per_clus',
                  'reserved', 'fats', 'dir_entries', 'sectors', 'media',
                  'fat_length', 'secs_track', 'heads', 'hidden', 'total_sect']

    bph_fmt    = '<3s8sHBHBHHBHHHII'

    fat_header = ['length', 'flags', 'version', 'root_cluster',
                  'info_sector', 'backup_boot', 'reserved2', 'drive_number',
                  'state', 'signature', 'vol_id', 'vol_label', 'fs_type']

    fat_fmt    = '<IHHIHH12sBBB4s11s8s'

    def __init__(self, path):
        try:
            with open(path, 'rb') as f:
                self.boot_sector = f.read(512)
                self.bph = dict(zip(self.bph_header, struct.unpack(self.bph_fmt, self.boot_sector[:36])))
                self.fat = dict(zip(self.fat_header, struct.unpack(self.fat_fmt, self.boot_sector[36:90])))
        except:
            raise Exception('Failed to read header {}'.format(path))

        self.sec_size = self.bph['sector_size']
        self.dat_offset = (self.bph['reserved']
                + self.fat['length'] * self.bph['fats']
                )* self.sec_size

        self.fat_offset = self.bph['reserved'] * self.sec_size

class DIRENT:
    dir_header = ['name', 'attr', 'lcase', 'ctime_cs', 'ctime',
                  'cdate', 'adate', 'starthi', 'time', 'date',
                  'start', 'size']

    dir_fmt = '<11sBBBHHHHHHHI'

    def __init__(self, dat):
        self.dir = dict(zip(self.dir_header, struct.unpack(self.dir_fmt, dat)))

def walk(path: str):

    a = BPH(path)

    root_dir = open(path, 'rb')
    root_dir.seek(a.dat_offset)
    b = root_dir.read(512)
    i = 0

    Files = []

    while True:
        c = DIRENT(b[i*32:i*32+32]).dir
        i += 1
        if c['name'][0] == 0:
            break
        Files.append(c)

    for e in Files:
        print(e['name'])



