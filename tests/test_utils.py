import unittest
from utils import hexdump, hexundump

class TestHexdumpMethods(unittest.TestCase):
    def test_hexdump(self):
        print("Test hexdump")

    def test_hexundump(self):
        for i in range(35):
            data = b'0' * i
            print(hexdump(data))
            # TEST: data == hexundump(hexdump(data), linesize=16)
            self.assertEqual(data, hexundump(hexdump(data), linesize=16))

        data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = hexundump("""
            0000   41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50   ABCDEFGHIJKLMNOP
            0010   51 52 53 54 55 56 57 58 59 5A                     QRSTUVWXYZ
            """, linesize=16)
        self.assertEqual(data, result)

        # 55 bytes data
        # $ xxd - g 1 - c 16 - l 55 - i < tests / test_utils.pyc
        # 0x03, 0xf3, 0x0d, 0x0a, 0x43, 0x7d, 0x38, 0x62, 0x63, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        # 0x00, 0x03, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x73, 0x42, 0x00, 0x00, 0x00, 0x64, 0x00,
        # 0x00, 0x64, 0x01, 0x00, 0x6c, 0x00, 0x00, 0x5a, 0x00, 0x00, 0x64, 0x02, 0x00, 0x65, 0x00, 0x00,
        # 0x6a, 0x01, 0x00, 0x66, 0x01, 0x00, 0x64
        #
        # $ xxd -g 1 -c 16 -l 55 tests/test_utils.pyc
        # 00000000: 03 f3 0d 0a 43 7d 38 62 63 00 00 00 00 00 00 00  ....C}8bc.......
        # 00000010: 00 03 00 00 00 40 00 00 00 73 42 00 00 00 64 00  .....@...sB...d.
        # 00000020: 00 64 01 00 6c 00 00 5a 00 00 64 02 00 65 00 00  .d..l..Z..d..e..
        # 00000030: 6a 01 00 66 01 00 64                             j..f..d
        #
        # $ xxd -g 1 -c 8 -l 55  tests/test_utils.pyc
        # 00000000: 03 f3 0d 0a 43 7d 38 62  ....C}8b
        # 00000008: 63 00 00 00 00 00 00 00  c.......
        # 00000010: 00 03 00 00 00 40 00 00  .....@..
        # 00000018: 00 73 42 00 00 00 64 00  .sB...d.
        # 00000020: 00 64 01 00 6c 00 00 5a  .d..l..Z
        # 00000028: 00 00 64 02 00 65 00 00  ..d..e..
        # 00000030: 6a 01 00 66 01 00 64     j..f..d
        #
        # $ hexdump -Cv -n 55 tests/test_utils.pyc
        # 00000000  03 f3 0d 0a 43 7d 38 62  63 00 00 00 00 00 00 00  |....C}8bc.......|
        # 00000010  00 03 00 00 00 40 00 00  00 73 42 00 00 00 64 00  |.....@...sB...d.|
        # 00000020  00 64 01 00 6c 00 00 5a  00 00 64 02 00 65 00 00  |.d..l..Z..d..e..|
        # 00000030  6a 01 00 66 01 00 64                              |j..f..d|
        # 00000037
        #
        data = bytes([
            0x03, 0xf3, 0x0d, 0x0a, 0x43, 0x7d, 0x38, 0x62, 0x63, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x03, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x73, 0x42, 0x00, 0x00, 0x00, 0x64, 0x00,
            0x00, 0x64, 0x01, 0x00, 0x6c, 0x00, 0x00, 0x5a, 0x00, 0x00, 0x64, 0x02, 0x00, 0x65, 0x00, 0x00,
            0x6a, 0x01, 0x00, 0x66, 0x01, 0x00, 0x64
        ])
        result = hexundump("""
            0000   03 F3 0D 0A 43 7D 38 62 63 00 00 00 00 00 00 00   ....C}8bc.......
            0010   00 03 00 00 00 40 00 00 00 73 42 00 00 00 64 00   .....@...sB...d.
            0020   00 64 01 00 6C 00 00 5A 00 00 64 02 00 65 00 00   .d..l..Z..d..e..
            0030   6A 01 00 66 01 00 64                              j..f..d
            """, linesize=16)
        self.assertEqual(data, result)

        result = hexundump("""$ xxd -g 1 -c 16 -l 55 tests/test_utils.pyc
            00000000: 03 f3 0d 0a 43 7d 38 62 63 00 00 00 00 00 00 00  ....C}8bc.......
            00000010: 00 03 00 00 00 40 00 00 00 73 42 00 00 00 64 00  .....@...sB...d.
            00000020: 00 64 01 00 6c 00 00 5a 00 00 64 02 00 65 00 00  .d..l..Z..d..e..
            00000030: 6a 01 00 66 01 00 64                             j..f..d
            """, linesize=16)
        self.assertEqual(data, result)

        result = hexundump("""$ xxd -g 1 -c 8 -l 55  tests/test_utils.pyc
            00000000: 03 f3 0d 0a 43 7d 38 62  ....C}8b
            00000008: 63 00 00 00 00 00 00 00  c.......
            00000010: 00 03 00 00 00 40 00 00  .....@..
            00000018: 00 73 42 00 00 00 64 00  .sB...d.
            00000020: 00 64 01 00 6c 00 00 5a  .d..l..Z
            00000028: 00 00 64 02 00 65 00 00  ..d..e..
            00000030: 6a 01 00 66 01 00 64     j..f..d
            """, linesize=8)
        self.assertEqual(data, result)

        result = hexundump("""$ hexdump -Cv -n 55 tests/test_utils.pyc
            00000000  03 f3 0d 0a 43 7d 38 62  63 00 00 00 00 00 00 00  |....C}8bc.......|
            00000010  00 03 00 00 00 40 00 00  00 73 42 00 00 00 64 00  |.....@...sB...d.|
            00000020  00 64 01 00 6c 00 00 5a  00 00 64 02 00 65 00 00  |.d..l..Z..d..e..|
            00000030  6a 01 00 66 01 00 64                              |j..f..d|
            00000037
            """, linesize=16)
        self.assertEqual(data, result)


# $ python3 -m unittest -v tests/test_utils.py
if __name__ == '__main__':
    unittest.main()