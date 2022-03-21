#!/usr/bin/env python3


def dump_hex_string(file, line):
    with open(file, 'rb') as f:
        data = f.read()
        print('file: %s' % file)
        print('size: %d' % len(data))
        print('data:')
        for x in range(0, len(data)):
            print('0x%02x, ' % data[x], end='')
            if x % line == line - 1:
                print()
    print()

if __name__ == '__main__':
    VERSION = 'v1.0.0'
    DATE = '2017.07.24'
    AUTHOR = 'Rocky Gu'

    import argparse

    parser = argparse.ArgumentParser(
        prog='bin2hexstr',
        description='convert binary to hex strings like: 0x11, 0x12, 0x13',
        epilog=VERSION + ' by ' + AUTHOR + ' [' + DATE + ']'
    )
    parser.add_argument("file",
                        help="input binary file name (*.bin)")
    parser.add_argument("-l", "--line", type=int, nargs='?', default=16,
                        help="hex string for each line, default is 16")
    args = parser.parse_args()
    dump_hex_string(args.file, args.line)
