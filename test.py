import unittest

from file_system import LogicalDisk


class TestDisk(unittest.TestCase):
    def test(self):
        disk = LogicalDisk("file.fat32")
        boot_sector = disk.boot_sector
        fs_sector = disk.fs_info_sector

        self.assertAlmostEqual(boot_sector.system_id, 'mkfs.fat')

        self.assertAlmostEqual(boot_sector.sector_size, 512)
        self.assertAlmostEqual(boot_sector.sec_per_clus, 1)
        self.assertAlmostEqual(boot_sector.reserved, 32)
        self.assertAlmostEqual(boot_sector.fats, 2)
        self.assertAlmostEqual(boot_sector.dir_entries, 0)
        self.assertAlmostEqual(boot_sector.sectors, 0)
        self.assertAlmostEqual(boot_sector.media, "STATIONARY")
        self.assertAlmostEqual(boot_sector.fat_length, 0)
        self.assertAlmostEqual(boot_sector.secs_track, 32)
        self.assertAlmostEqual(boot_sector.heads, 64)
        self.assertAlmostEqual(boot_sector.hidden, 0)
        self.assertAlmostEqual(boot_sector.total_sect, 102400)

        self.assertAlmostEqual(boot_sector.length, 788)
        self.assertAlmostEqual(boot_sector.flags, 0)
        self.assertAlmostEqual(boot_sector.version, 0)
        self.assertAlmostEqual(boot_sector.root_cluster, 2)
        self.assertAlmostEqual(boot_sector.info_sector, 1)
        self.assertAlmostEqual(boot_sector.backup_boot, 6)
        self.assertAlmostEqual(boot_sector.drive_number, 128)
        self.assertAlmostEqual(boot_sector.vol_id[0], 0x32C6)
        self.assertAlmostEqual(boot_sector.vol_id[1], 0x2AEE)
        self.assertAlmostEqual(boot_sector.vol_label, "NO NAME    ")
        self.assertAlmostEqual(boot_sector.fs_type, "FAT32   ")

        self.assertAlmostEqual(fs_sector.signature1, 0x41615252)
        self.assertAlmostEqual(fs_sector.signature2, 0x61417272)
        self.assertAlmostEqual(fs_sector.free_clusters, 100767)
        self.assertAlmostEqual(fs_sector.next_clusters, 76)


if __name__ == '__main__':
    unittest.main()
