#!/usr/bin/env python3

def add_line_number(infile, outfile, width=3):
    with open(infile, 'r') as inf, open(outfile, 'w') as outf:
        for (num, line) in enumerate(inf, start=1):
            str = '{1:{0:d}d} {2:s}'.format(width, num, line)
            print(str, end='')
            outf.write(str)
        outf.close()
        inf.close()


if __name__ == '__main__':
    VERSION = 'v1.0.0'
    DATE = '2017.10.19'
    AUTHOR = 'Rocky Gu'

    import argparse

    parser = argparse.ArgumentParser(
        prog='linemumber',
        description='add line numbers for infile at the front of each line',
        epilog=VERSION + ' by ' + AUTHOR + ' [' + DATE + ']'
    )
    parser.add_argument("infile",
                        help="input file (text like, non binary)")
    parser.add_argument("outfile",
                        help="output file with line numbers")
    parser.add_argument("-w", "--width", type=int, nargs='?', default=3,
                        help="reserved width for line numbers")
    args = parser.parse_args()

    add_line_number(args.infile, args.outfile, args.width)
