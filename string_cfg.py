from configparser import ConfigParser

config = ConfigParser()
config.read("string.cfg", encoding='utf-8')


class BOOT_SECTOR:
    IGNORED = config.get("FAT_BOOT_SECTOR", "IGNORED")
    SYSTEM_ID = config.get("FAT_BOOT_SECTOR", "SYSTEM_ID")
    SECTOR_SIZE = config.get("FAT_BOOT_SECTOR", "SECTOR_SIZE")
    SECTOR_PER_CLUS = config.get("FAT_BOOT_SECTOR", "SECTOR_PER_CLUS")
    RESERVED = config.get("FAT_BOOT_SECTOR", "RESERVED")
    FATS = config.get("FAT_BOOT_SECTOR", "FATS")
    DIR_ENTRIES = config.get("FAT_BOOT_SECTOR", "DIR_ENTRIES")
    SECTORS = config.get("FAT_BOOT_SECTOR", "SECTORS")
    MEDIA = config.get("FAT_BOOT_SECTOR", "MEDIA")
    FAT_LENGTH = config.get("FAT_BOOT_SECTOR", "FAT_LENGTH")
    SECT_TRACK = config.get("FAT_BOOT_SECTOR", "SECT_TRACK")
    HEADS = config.get("FAT_BOOT_SECTOR", "HEADS")
    HIDDEN = config.get("FAT_BOOT_SECTOR", "HIDDEN")
    TOTAL_SECT = config.get("FAT_BOOT_SECTOR", "TOTAL_SECT")

    LENGTH = config.get("FAT_BOOT_SECTOR", "LENGTH")
    FLAGS = config.get("FAT_BOOT_SECTOR", "FLAGS")
    VERSION = config.get("FAT_BOOT_SECTOR", "VERSION")
    ROOT_CLUSTER = config.get("FAT_BOOT_SECTOR", "ROOT_CLUSTER")
    INFO_SECTOR = config.get("FAT_BOOT_SECTOR", "INFO_SECTOR")
    BACKUP_BOOT = config.get("FAT_BOOT_SECTOR", "BACKUP_BOOT")
    DRIVE_NUMBER = config.get("FAT_BOOT_SECTOR", "DRIVE_NUMBER")
    VOL_ID = config.get("FAT_BOOT_SECTOR", "VOL_ID")
    VOL_LABEL = config.get("FAT_BOOT_SECTOR", "VOL_LABEL")
    FS_TYPE = config.get("FAT_BOOT_SECTOR", "FS_TYPE")


class FSINFO:
    SIGNATURE_1 = config.get("FAT_BOOT_FSINFO", "SIGNATURE_1")
    SIGNATURE_2 = config.get("FAT_BOOT_FSINFO", "SIGNATURE_2")
    FREE_CLUSTERS = config.get("FAT_BOOT_FSINFO", "FREE_CLUSTERS")
    NEXT_CLUSTERS = config.get("FAT_BOOT_FSINFO", "NEXT_CLUSTERS")


class LFN:
    ID = config.get("FAT_LFN", "ID")
    NAME0_4 = config.get("FAT_LFN", "NAME0_4")
    ATTR = config.get("FAT_LFN", "ATTR")
    ALIAS_CHECKSUM = config.get("FAT_LFN", "ALIAS_CHECKSUM")
    NAME5_10 = config.get("FAT_LFN", "NAME5_10")
    NAME11_12 = config.get("FAT_LFN", "NAME11_12")


class DIR_ENTRY:
    STATE = config.get("FAT_DIR_ENTRY", "STATE")
    NAME = config.get("FAT_DIR_ENTRY", "NAME")
    ATTRIB = config.get("FAT_DIR_ENTRY", "ATTRIB")
    CTIME_CS = config.get("FAT_DIR_ENTRY", "CTIME_CS")
    CTIME = config.get("FAT_DIR_ENTRY", "CTIME")
    CDATE = config.get("FAT_DIR_ENTRY", "CDATE")
    ADATE = config.get("FAT_DIR_ENTRY", "ADATE")
    STARTHI = config.get("FAT_DIR_ENTRY", "STARTHI")
    TIME = config.get("FAT_DIR_ENTRY", "TIME")
    DATE = config.get("FAT_DIR_ENTRY", "DATE")
    START = config.get("FAT_DIR_ENTRY", "START")
    SIZE = config.get("FAT_DIR_ENTRY", "SIZE")


class COMMANDER:
    ERROR_INFO = config.get("COMMANDER", "ERROR_INFO")
    ERROR_INFO_INPUT = config.get("COMMANDER", "ERROR_INFO_INPUT")

    ERROR_CD_INPUT = config.get("COMMANDER", "ERROR_CD_INPUT")
    ERROR_CD_NOT_FOUND = config.get("COMMANDER", "ERROR_CD_NOT_FOUND")

    ERROR_CAT = config.get("COMMANDER", "ERROR_CAT")
    ERROR_CAT_INPUT = config.get("COMMANDER", "ERROR_CAT_INPUT")
    ERROR_CAR_NOT_FOUND = config.get("COMMANDER", "ERROR_CAR_NOT_FOUND")

    ERROR_LOOP = config.get("COMMANDER", "ERROR_LOOP")

class MAIN:
    ERROR_INPUT_PARAM = config.get("MAIN", "ERROR_INPUT_PARAM")