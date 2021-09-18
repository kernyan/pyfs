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
            Msg = 'Failed to read header {}'.format(path)
            raise Exception(Msg)

        if self.fat['fs_type'] != b'FAT32   ':
            raise Exception('Only FAT32 is supported')

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

    lfn_header = ['id', 'name0_4', 'attr', 'reserved', 'alias_checksum',
                  'name5_10', 'start', 'name11_12']

    lfn_fmt = '<B10sBBB12sH4s'

    def IsDir(self):
        return self.dir['attr'] == 0x10

    def __init__(self, b: bytes, i: int):

        self.lfname = ''

        if b[i+11] == 0xf:
            self.lfn = dict(zip(self.lfn_header, struct.unpack(self.lfn_fmt, b[i:i+32])))
            out = self.lfn['name0_4'] + self.lfn['name5_10'] + self.lfn['name11_12']
            self.lfname = out[:out.index(b'\x00\x00\xff\xff')].decode('utf-16')
            self.dir = dict(zip(self.dir_header, struct.unpack(self.dir_fmt, b[i+32:i+64])))
            self.dir['d_cnt'] = 2
        else:
            self.dir = dict(zip(self.dir_header, struct.unpack(self.dir_fmt, b[i:i+32])))
            self.dir['d_cnt'] = 1
        self.dir['pos'] = i

    def GetExtension(self):
        return self.dir['name'][8:].decode('utf-8').strip()

    def __repr__(self):
        fname = ''
        if self.lfname != '':
            fname = self.lfname
        else:
            fname = self.dir['name'][:8].decode('utf-8').strip()
        Extension = '' if self.IsDir() else '.' + self.GetExtension()
        return (fname.lower() if self.dir['lcase'] == 0x8 else fname) + \
               (Extension.lower() if self.dir['lcase'] == 0x10 else Extension)

class File():
    def __init__(self, d: DIRENT):
        self.d = d

    def read(self):
        return self.d.dir['start'] + (self.d.dir['starthi'] << 1)


class pfs():
    def __init__(self, path: str):
        self.BPH = BPH(path)
        self.fs = open(path, 'rb')
        self.root_dir = self.parse_rootdir()

    def open(self, fn: str):
        return self.root_dir

    def parse_rootdir(self):
        self.fs.seek(self.BPH.dat_offset)
        b = self.fs.read(512)
        out = []
        i = 0
        while True:
            c = DIRENT(b, i)
            if c.dir['name'][0] == 0:
                break
            out.append(c)
            i = c.dir['pos'] + c.dir['d_cnt'] * 32
        return out

    def open(self, fn: str):
        for e in self.root_dir:
            if repr(e) == fn:
                return File(e)

def open_fs(path: str):
    fs = pfs(path)
    return fs


