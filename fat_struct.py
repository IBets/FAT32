from string_cfg import LFN, BOOT_SECTOR, FSINFO, DIR_ENTRY
import io


def le8(value):
    return int.from_bytes(value, byteorder='little', signed=False)


def le16(value):
    return int.from_bytes(value, byteorder='little', signed=False)


def le32(value):
    return int.from_bytes(value, byteorder='little', signed=False)


def get_time(value):
    value = int.from_bytes(value, byteorder='little', signed=False)
    second = value & 0x1F
    minute = (value & 0x7E0) >> 5
    hour = (value & 0xF800) >> 11
    return hour, minute, second


def get_date(value):
    value = int.from_bytes(value, byteorder='little', signed=False)
    day = value & 0x1F
    month = (value & 0x1E0) >> 5
    year = (value & 0xFE00) >> 9
    return (year + 1980, month, day)


class FAT_STRUCT_SIZE:
    FAT_BOOT_SECTOR = 512
    FAT_BOOT_FSINFO = 512
    FAT_DIR_ENTRY = 32
    FAT_LFN = 32


class FAT_BOOT_SECTOR:
    SIZE = FAT_STRUCT_SIZE.FAT_BOOT_SECTOR
    TYPE_MEDIA = {
        0xf8: "STATIONARY",
        0xf0: "DETACHABLE",
    }

    def __init__(self, arr_byte):
        file_desc = io.BytesIO(arr_byte)

        file_desc.seek(510)
        if le16(file_desc.read(2)) != 0xAA55:
            raise Exception("Not a valid filesystem")
        file_desc.seek(0)

        self.ignored = int.from_bytes(file_desc.read(3), byteorder='little', signed=False)
        self.system_id = file_desc.read(8).decode(encoding="ascii")
        self.sector_size = le16(file_desc.read(2))
        self.sec_per_clus = le8(file_desc.read(1))
        self.reserved = le16(file_desc.read(2))
        self.fats = le8(file_desc.read(1))
        self.dir_entries = le16(file_desc.read(2))
        self.sectors = le16(file_desc.read(2))
        self.media = FAT_BOOT_SECTOR.TYPE_MEDIA[le8(file_desc.read(1))]
        self.fat_length = le16(file_desc.read(2))
        self.secs_track = le16(file_desc.read(2))
        self.heads = le16(file_desc.read(2))
        self.hidden = le32(file_desc.read(4))
        self.total_sect = le32(file_desc.read(4))

        self.length = le32(file_desc.read(4))
        self.flags = le16(file_desc.read(2))
        self.version = le16(file_desc.read(2))
        self.root_cluster = le32(file_desc.read(4))
        self.info_sector = le16(file_desc.read(2))
        self.backup_boot = le16(file_desc.read(2))
        self.reserved2 = file_desc.read(12)
        self.drive_number = le8(file_desc.read(1))
        self.state = le8(file_desc.read(1))
        self.signature = le8(file_desc.read(1))
        self.vol_id = le16(file_desc.read(2)), le16(file_desc.read(2))
        self.vol_label = file_desc.read(11).decode(encoding="ascii")
        self.fs_type = file_desc.read(8).decode(encoding="ascii")

    def __str__(self):
        str_output = io.StringIO()
        str_output.writelines(BOOT_SECTOR.IGNORED + "{}\n".format(self.ignored))
        str_output.writelines(BOOT_SECTOR.SYSTEM_ID + "{}\n".format(self.system_id))
        str_output.writelines(BOOT_SECTOR.SECTOR_SIZE + "{}\n".format(self.sector_size))
        str_output.writelines(BOOT_SECTOR.SECTOR_PER_CLUS + "{}\n".format(self.sec_per_clus))
        str_output.writelines(BOOT_SECTOR.RESERVED + "{}\n".format(self.reserved))
        str_output.writelines(BOOT_SECTOR.FATS + "{}\n".format(self.fats))
        str_output.writelines(BOOT_SECTOR.DIR_ENTRIES + "{}\n".format(self.dir_entries))
        str_output.writelines(BOOT_SECTOR.SECTORS + "{}\n".format(self.sectors))
        str_output.writelines(BOOT_SECTOR.MEDIA + "{}\n".format(self.media))
        str_output.writelines(BOOT_SECTOR.FAT_LENGTH + "{}\n".format(self.fat_length))
        str_output.writelines(BOOT_SECTOR.SECT_TRACK + "{}\n".format(self.secs_track))
        str_output.writelines(BOOT_SECTOR.HEADS + "{}\n".format(self.heads))
        str_output.writelines(BOOT_SECTOR.HIDDEN + "{}\n".format(self.hidden))
        str_output.writelines(BOOT_SECTOR.TOTAL_SECT + "{}\n".format(self.total_sect))
        str_output.writelines(BOOT_SECTOR.LENGTH + "{}\n".format(self.length))
        str_output.writelines(BOOT_SECTOR.FLAGS + "{}\n".format(self.flags))
        str_output.writelines(BOOT_SECTOR.VERSION + "{}\n".format(self.version))
        str_output.writelines(BOOT_SECTOR.ROOT_CLUSTER + "{}\n".format(self.root_cluster))
        str_output.writelines(BOOT_SECTOR.INFO_SECTOR + "{}\n".format(self.info_sector))
        str_output.writelines(BOOT_SECTOR.BACKUP_BOOT + "{}\n".format(self.backup_boot))
        str_output.writelines(BOOT_SECTOR.DRIVE_NUMBER + "{}\n".format(self.drive_number))
        str_output.writelines(BOOT_SECTOR.VOL_ID + "{:X}-{:X}\n".format(self.vol_id[0], self.vol_id[1]))
        str_output.writelines(BOOT_SECTOR.VOL_LABEL + "{}\n".format(self.vol_label))
        str_output.writelines(BOOT_SECTOR.FS_TYPE + "{}\n".format(self.fs_type))
        return str_output.getvalue()


class FAT_BOOT_FSINFO:
    SIZE = FAT_STRUCT_SIZE.FAT_BOOT_FSINFO

    def __init__(self, arr_byte):
        file_desc = io.BytesIO(arr_byte)
        self.signature1 = le16(file_desc.read(4))
        self.reserved1 = file_desc.read(480)
        self.signature2 = le16(file_desc.read(4))
        self.free_clusters = le16(file_desc.read(4))
        self.next_clusters = le16(file_desc.read(4))
        self.reserved2 = file_desc.read(16)

    def __str__(self):
        str_output = io.StringIO()
        str_output.writelines(FSINFO.SIGNATURE_1 + "0x{:X}\n".format(self.signature1))
        str_output.writelines(FSINFO.SIGNATURE_2 + "0x{:X}\n".format(self.signature2))
        str_output.writelines(FSINFO.FREE_CLUSTERS + "{}\n".format(self.free_clusters))
        str_output.writelines(FSINFO.NEXT_CLUSTERS + "{}\n".format(self.next_clusters))
        return str_output.getvalue()


class FAT_DIR_ENTRY:
    SIZE = FAT_STRUCT_SIZE.FAT_DIR_ENTRY

    def __init__(self, arr_byte):
        file_desc = io.BytesIO(arr_byte)
        self.state = le8(file_desc.read(1))
        self.name = file_desc.read(7).decode(encoding="cp1251")
        self.ext = file_desc.read(3).decode(encoding="cp1251")
        self.attr = le8(file_desc.read(1))
        self.lcase = le8(file_desc.read(1))
        self.ctime_cs = le8(file_desc.read(1))
        self.ctime = get_time(file_desc.read(2))
        self.cdate = get_date(file_desc.read(2))
        self.adate = get_date(file_desc.read(2))
        self.starthi = le16(file_desc.read(2))
        self.time = get_time(file_desc.read(2))
        self.date = get_date(file_desc.read(2))
        self.start = le16(file_desc.read(2))
        self.size = le32(file_desc.read(4))

    def __str__(self):
        str_output = io.StringIO()

        str_output.write(DIR_ENTRY.STATE + "{}\n".format(self.state))
        str_output.write(DIR_ENTRY.NAME + "{}.{}\n".format(self.name, self.ext))
        str_output.writelines(DIR_ENTRY.ATTRIB + "{}\n".format(self.attr))
        str_output.writelines(DIR_ENTRY.CTIME_CS + "{}\n".format(self.ctime_cs))
        str_output.writelines(DIR_ENTRY.CTIME + "{}:{}:{}\n".format(self.ctime[0],
                                                                    self.ctime[1],
                                                                    self.ctime[2]))

        str_output.writelines(DIR_ENTRY.CDATE + "{}:{}:{}\n".format(self.cdate[0],
                                                                    self.cdate[1],
                                                                    self.cdate[2]))

        str_output.writelines(DIR_ENTRY.ADATE + "{}:{}:{}\n".format(self.adate[0],
                                                                    self.adate[1],
                                                                    self.adate[2]))
        str_output.writelines(DIR_ENTRY.STARTHI + "{}\n".format(self.starthi))
        str_output.writelines(DIR_ENTRY.TIME + "{}:{}:{}\n".format(self.time[0],
                                                                   self.time[1],
                                                                   self.time[2]))

        str_output.writelines(DIR_ENTRY.DATE + "{}:{}:{}\n".format(self.date[0],
                                                                   self.date[1],
                                                                   self.date[2]))
        str_output.writelines(DIR_ENTRY.START + "{}\n".format(self.start))
        str_output.writelines(DIR_ENTRY.SIZE + "{}\n".format(self.size))
        return str_output.getvalue()


class FAT_LFN:
    SIZE = FAT_STRUCT_SIZE.FAT_LFN

    def __init__(self, arr_byte):
        file_desc = io.BytesIO(arr_byte)
        self.id = le8(file_desc.read(1))
        self.name0_4 = file_desc.read(10)
        self.attr = le8(file_desc.read(1))
        self.reserved = le8(file_desc.read(1))
        self.alias_checksum = le8(file_desc.read(1))
        self.name5_10 = file_desc.read(12)
        self.start = le16(file_desc.read(2))
        self.name11_12 = file_desc.read(4)

    def __str__(self):
        str_output = io.StringIO()
        str_output.writelines(LFN.ID + "{}\n".format(self.id))
        str_output.writelines(LFN.NAME0_4 + "{}\n".format(self.name0_4.decode(encoding="utf-16")))
        str_output.writelines(LFN.ATTR + "{}\n".format(self.attr))
        str_output.writelines(LFN.ALIAS_CHECKSUM + "{}\n".format(self.alias_checksum))
        str_output.writelines(LFN.NAME5_10 + "{}\n".format(self.name5_10.decode(encoding="utf-16")))
        str_output.writelines(LFN.NAME11_12 + "{}\n".format(self.name11_12.decode(encoding="utf-16")))
        return str_output.getvalue()
