#!/usr/bin/env python3

INT2BYTE_CACHE = {i:bytes([i]) for i in range(256)}


def int2byte(character):
    """Converts (0 through 255) integer into b'...' character."""
    return INT2BYTE_CACHE[character]


def byte2int(character):
    """Converts b'...' character into (0 through 255) integer."""
    return character[0]


def str2bytes(string):
    """Converts '...' string into b'...' string. On PY2 they are equivalent. On PY3 its utf8 encoded."""
    return string.encode("utf8")


def bytes2str(string):
    """Converts b'...' string into '...' string. On PY2 they are equivalent. On PY3 its utf8 decoded."""
    return string.decode("utf8")


# Map an integer in the inclusive range 0-255 to its string byte representation
PRINTABLE = [bytes2str(int2byte(i)) if 32 <= i < 127 else '.' for i in range(256)]
HEXPRINT = [format(i, '02X') for i in range(256)]


def hexdump(data, linesize=16):
    r"""
    Turns bytes into a unicode string of the format:

    ::

        >>>print(hexdump(b'0' * 100, 16))
        hexundump(\"\"\"
        0000   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0010   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0020   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0030   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0040   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0050   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0060   30 30 30 30                                       0000
        \"\"\")
    """
    if len(data) < 16**4:
        fmt = "%%04X   %%-%ds   %%s" % (3*linesize-1,)
    elif len(data) < 16**8:
        fmt = "%%08X   %%-%ds   %%s" % (3*linesize-1,)
    else:
        raise ValueError("hexdump cannot process more than 16**8 or 4294967296 bytes")
    prettylines = []
    prettylines.append('hexundump("""')
    for i in range(0, len(data), linesize):
        line = data[i:i+linesize]
        hextext = " ".join(HEXPRINT[b] for b in line)
        rawtext = "".join(PRINTABLE[b] for b in line)
        prettylines.append(fmt % (i, str(hextext), str(rawtext)))
    prettylines.append('""", linesize={})'.format(linesize))
    prettylines.append("")
    return "\n".join(prettylines)


def hexundump(data, linesize=16):
    r"""
    Reverse of `hexdump`.
    """
    raw = []
    for line in data.split("\n")[1:-1]:
        line = line.lstrip()    # strip left most spaces
        line = line[line.find(" "):].lstrip()
        bytes = [int2byte(int(s,16)) for s in line[:3*linesize].split()]
        raw.extend(bytes)
    return b"".join(raw)


if __name__ == "__main__":
    data = hexundump("""
0000   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
0010   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
0020   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
0030   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
0040   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
0050   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
0060   30 30 30 30                                       0000
""")
    print(hexdump(data))

    data = hexundump("""
    0000   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
    0010   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
    0020   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
    0030   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
    0040   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
    0050   30 30 30 30 30 30 30 30 7f 7f 7f 7f 7f 7f 7f 7f   0000000000000000
    0060   30 30 30 30                                       0000
    """)
    print(hexdump(data))