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


def hexundump(data, linesize):
    r"""
    Reverse of `hexdump`.

        >>> data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        >>> data = hexundump(\"\"\"
        0000   41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50   ABCDEFGHIJKLMNOP
        0010   51 52 53 54 55 56 57 58 59 5A                     QRSTUVWXYZ
        \"\"\", linesize=16)
    """
    raw = []
    for line in data.split("\n")[1:-1]:
        line = line.lstrip()    # strip left most spaces
        line = line[line.find(" "):].lstrip()
        bytes = [int2byte(int(s,16)) for s in line[:3*linesize].split()]
        raw.extend(bytes)
    return b"".join(raw)


if __name__ == "__main__":
    # 0. 使用 hexundump 解析 hexdump 输出结果，并再次使用 hexdump 输出
    data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print(data)
    data = hexundump("""
        0000   41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50   ABCDEFGHIJKLMNOP
        0010   51 52 53 54 55 56 57 58 59 5A                     QRSTUVWXYZ
        """, linesize=16)
    print(hexdump(data))

    # 1. 使用 hexundump 解析 hexdump 输出结果，并再次使用 hexdump 输出
    print("Revert hexdump output:")
    data = hexundump("""
        0000   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0010   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0020   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0030   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0040   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0050   30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30   0000000000000000
        0060   30 30 30 30                                       0000
        """, linesize=16)
    print(hexdump(data))

    # 2. 使用 hexundump 解析 xxd 工具输出结果(linesize=16)，并使用 hexdump 输出
    print("Revert xxd output with linesize=16:")
    data = hexundump('''$ xxd -g 1 -c 16 -l 120 utils.py
        00000000: 23 21 2f 75 73 72 2f 62 69 6e 2f 65 6e 76 20 70  #!/usr/bin/env p
        00000010: 79 74 68 6f 6e 33 0a 0a 49 4e 54 32 42 59 54 45  ython3..INT2BYTE
        00000020: 5f 43 41 43 48 45 20 3d 20 7b 69 3a 62 79 74 65  _CACHE = {i:byte
        00000030: 73 28 5b 69 5d 29 20 66 6f 72 20 69 20 69 6e 20  s([i]) for i in
        00000040: 72 61 6e 67 65 28 32 35 36 29 7d 0a 0a 0a 64 65  range(256)}...de
        00000050: 66 20 69 6e 74 32 62 79 74 65 28 63 68 61 72 61  f int2byte(chara
        00000060: 63 74 65 72 29 3a 0a 20 20 20 20 22 22 22 43 6f  cter):.    """Co
        00000070: 6e 76 65 72 74 73 20 28                          nverts (
    ''', linesize=16)
    print(hexdump(data))

    # 3. 使用 hexundump 解析 xxd 工具输出结果(linesize=8)，并使用 hexdump 输出
    print("Revert xxd output with linesize=8:")
    data = hexundump('''$ xxd -g 1 -c 8 -l 60 utils.py
        00000000: 23 21 2f 75 73 72 2f 62  #!/usr/b
        00000008: 69 6e 2f 65 6e 76 20 70  in/env p
        00000010: 79 74 68 6f 6e 33 0a 0a  ython3..
        00000018: 49 4e 54 32 42 59 54 45  INT2BYTE
        00000020: 5f 43 41 43 48 45 20 3d  _CACHE =
        00000028: 20 7b 69 3a 62 79 74 65   {i:byte
        00000030: 73 28 5b 69 5d 29 20 66  s([i]) f
        00000038: 6f 72 20 69              or i
        ''', linesize=8)
    print(hexdump(data, linesize=8))

    # 4. 使用 hexundump 解析 hexdump 工具输出结果，并使用 hexdump 输出
    print("Revert hexdump output:")
    data = hexundump('''$ hexdump -Cv -n 120 utils.py
        00000000  23 21 2f 75 73 72 2f 62  69 6e 2f 65 6e 76 20 70  |#!/usr/bin/env p|
        00000010  79 74 68 6f 6e 33 0a 0a  49 4e 54 32 42 59 54 45  |ython3..INT2BYTE|
        00000020  5f 43 41 43 48 45 20 3d  20 7b 69 3a 62 79 74 65  |_CACHE = {i:byte|
        00000030  73 28 5b 69 5d 29 20 66  6f 72 20 69 20 69 6e 20  |s([i]) for i in |
        00000040  72 61 6e 67 65 28 32 35  36 29 7d 0a 0a 0a 64 65  |range(256)}...de|
        00000050  66 20 69 6e 74 32 62 79  74 65 28 63 68 61 72 61  |f int2byte(chara|
        00000060  63 74 65 72 29 3a 0a 20  20 20 20 22 22 22 43 6f  |cter):.    """Co|
        00000070  6e 76 65 72 74 73 20 28                           |nverts (|
        00000078
        ''', linesize=16)
    print(hexdump(data))