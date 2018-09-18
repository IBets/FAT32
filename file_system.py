from fat_struct import *
import datetime

FAT_EOF = 0x0FFFFFFF
FAT_MEDIA = 0x0FFFFFF8
FAT_FREE = 0x00000000
FAT_ATTRIB_POS = 11
FAT_ATTRIB_LONG_NAME = 0x0f
FAT_ATTRIB_FILE = 0x20
FAT_ATTRIB_DIR = 0x10


class ElementTable:
    FILE_ATTRIB = {FAT_ATTRIB_FILE: "FILE",
                   FAT_ATTRIB_DIR: "DIR"}

    def __init__(self, directory_entry, list_lfn):

        self.directory_entry = None
        self.file_atributes = None
        self.size = None
        self.name = None
        self.written = None
        self.access = None
        self.created = None

        self.directory_entry = (directory_entry.starthi << 16) | directory_entry.start
        self.file_atributes = directory_entry.attr
        self.size = directory_entry.size
        if len(list_lfn) == 0:
            self.name = (chr(directory_entry.state) + directory_entry.name).strip()
        else:
            self.name = self._lfn_string(list_lfn)

        try:
            self.written = datetime.datetime(year=directory_entry.date[0],
                                             month=directory_entry.date[1],
                                             day=directory_entry.date[2],
                                             hour=directory_entry.time[0],
                                             minute=directory_entry.time[1],
                                             second=directory_entry.time[2])

            self.access = datetime.datetime(year=directory_entry.adate[0],
                                            month=directory_entry.adate[1],
                                            day=directory_entry.adate[2],
                                            hour=0,
                                            minute=0,
                                            second=0)
            self.created = datetime.datetime(year=directory_entry.cdate[0],
                                             month=directory_entry.cdate[1],
                                             day=directory_entry.cdate[2],
                                             hour=directory_entry.ctime[0],
                                             minute=directory_entry.ctime[1],
                                             second=directory_entry.ctime[2])
        except Exception:
            pass

    def _lfn_string(self, list_lfn):

        full_str = b''
        for e_lfn in reversed(list_lfn):
            sub_str = e_lfn.name0_4 + e_lfn.name5_10 + e_lfn.name11_12
            full_str += sub_str

        p_index = 0
        lenght = len(full_str)
        for index in range(1, lenght):
            if full_str[lenght - index] == 0xFF:
                p_index += 1
        return full_str[:lenght - p_index - 2].decode("utf-16").rstrip().strip()

    def is_file(self):
        return self.file_atributes == FAT_ATTRIB_FILE

    def is_dir(self):
        return self.file_atributes == FAT_ATTRIB_DIR

    def __str__(self):
        str_output = io.StringIO()
        str_output.write("<{}> ".format(ElementTable.FILE_ATTRIB[self.file_atributes]))
        str_output.write("\t{} ".format(self.name))
        str_output.write("\t{}".format(self.created))
        if self.file_atributes == FAT_ATTRIB_FILE:
            str_output.write("\t{}".format(self.size))
        return str_output.getvalue()


class LogicalDisk:
    def __init__(self, file_name):
        self.file_desc = None
        self.boot_sector = None
        self.fs_info_sector = None
        self.fat = None
        self.root = None
        self.bps = 0
        self.spc = 0
        self.dps = 0

        self.p_fat_sec = None
        self.p_data_sec = 0
        self.count_root_clus = 0

        self.file_desc = open(file_name, "rb")
        self._read_boot_entry()
        self._read_fs_info()
        self._read_fat()
        self._read_root_dir()

    def _read_boot_entry(self):
        self.file_desc.seek(0)
        self.boot_sector = FAT_BOOT_SECTOR(self.file_desc.read(FAT_BOOT_SECTOR.SIZE))

        self.bps = self.boot_sector.sector_size
        self.spc = self.boot_sector.sec_per_clus
        self.dps = int((self.bps * self.spc) / FAT_DIR_ENTRY.SIZE)
        self.p_data_sec = (self.boot_sector.reserved + self.boot_sector.fats * self.boot_sector.length)
        self.p_fat_sec = self.boot_sector.reserved

    def _read_fs_info(self):
        self.file_desc.seek(self.boot_sector.info_sector * self.bps)
        self.fs_info_sector = FAT_BOOT_FSINFO(self.file_desc.read(FAT_BOOT_FSINFO.SIZE))

    def _read_fat(self):
        self.file_desc.seek(self.p_fat_sec * self.bps)
        self.fat = [le32(self.file_desc.read(4)) for x in range(self.boot_sector.length * self.bps)]

    def _read_root_dir(self):
        self.root = self.read_dir(self.boot_sector.root_cluster)

    def _read_cluster(self, cluster):
        self.file_desc.seek((self.p_data_sec + (cluster - 2) * self.spc) * self.bps)
        return self.file_desc.read(self.spc * self.bps)

    def _read_table(self, index):
        result = [index]
        while self.fat[index] != FAT_EOF and self.fat[index] != FAT_MEDIA:
            index = self.fat[index]
            result.append(index)
        return result

    def _read_clusters(self, table):
        return [self._read_cluster(x) for x in table]

    def read_dir(self, index):
        if index == 0:
            return self.root

        result = []
        variable_long_name = []
        for clus in self._read_clusters(self._read_table(index)):
            byte_clus = io.BytesIO(clus)
            for index in range(0, self.dps):
                data = byte_clus.read(FAT_DIR_ENTRY.SIZE)
                if data[0] == 0xE5:
                    continue
                if data[FAT_ATTRIB_POS] == FAT_ATTRIB_LONG_NAME:
                    variable_long_name.append(FAT_LFN(data))
                if FAT_ATTRIB_DIR == data[FAT_ATTRIB_POS] or data[FAT_ATTRIB_POS] == FAT_ATTRIB_FILE:
                    result.append(ElementTable(FAT_DIR_ENTRY(data), variable_long_name.copy()))
                    variable_long_name.clear()

        return result

    def read_file(self, index, size):
        result = io.BytesIO()
        clusters = self._read_clusters(self._read_table(index))
        for clus in clusters:
            result.write(clus)
        result.seek(0)
        max_len = len(clusters) * self.bps * self.spc
        if size > max_len:
            return result.read(max_len)
        else:
            return result.read(size)

    @property
    def boot_entry(self):
        return self.boot_sector

    @property
    def fs_info(self):
        return self.fs_info_sector
