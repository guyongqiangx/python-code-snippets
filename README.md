# 工具函数说明

## 1. hexdump

> 用法: `hexdump(data, linesize=16)`, 以 16 进制的方式打印输出 `data` 数据，每行按照 `linesize` 指定的长度换行。

```python
>>> data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> print(hexdump(data))
hexundump("""
0000   41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50   ABCDEFGHIJKLMNOP
0010   51 52 53 54 55 56 57 58 59 5A                     QRSTUVWXYZ
""", linesize=16)
>>>
>>> print(hexdump(data, linesize=8))
hexundump("""
0000   41 42 43 44 45 46 47 48   ABCDEFGH
0008   49 4A 4B 4C 4D 4E 4F 50   IJKLMNOP
0010   51 52 53 54 55 56 57 58   QRSTUVWX
0018   59 5A                     YZ
""", linesize=8)
```



## 2. hexundump

> 用法: `hexundump(data, linesize)`, 解析 `行号: A0 B1 C2 D3....` 格式的字符串为相应的十六进制数据,  `linesize` 指定每行解析得到的最大的字节数。

```python
>>> data = hexundump("""
        0000   41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50   ABCDEFGHIJKLMNOP
        0010   51 52 53 54 55 56 57 58 59 5A                     QRSTUVWXYZ
        """, linesize=16)
>>> print(data)
b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>>
>>> data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> print(hexundump(hexdump(data), linesize=16))
b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> print(hexdump(hexundump(hexdump(data), linesize=16)))
hexundump("""
0000   41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50   ABCDEFGHIJKLMNOP
0010   51 52 53 54 55 56 57 58 59 5A                     QRSTUVWXYZ
""", linesize=16)
```
- 解析 xxd 工具操作的结果:
```python
>>> data = hexundump('''
				$ xxd -g 1 -c 8 -l 60 utils.py
        00000000: 23 21 2f 75 73 72 2f 62  #!/usr/b
        00000008: 69 6e 2f 65 6e 76 20 70  in/env p
        00000010: 79 74 68 6f 6e 33 0a 0a  ython3..
        00000018: 49 4e 54 32 42 59 54 45  INT2BYTE
        00000020: 5f 43 41 43 48 45 20 3d  _CACHE =
        00000028: 20 7b 69 3a 62 79 74 65   {i:byte
        00000030: 73 28 5b 69 5d 29 20 66  s([i]) f
        00000038: 6f 72 20 69              or i
        ''', linesize=8)
>>> print(data)
b'#!/usr/bin/env python3\n\nINT2BYTE_CACHE = {i:bytes([i]) for i'
```
- 解析 hexdump 工具操作的结果:
```python
>>> data = hexundump('''
				$ hexdump -Cv -n 120 utils.py
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
>>> print(data)
b'#!/usr/bin/env python3\n\nINT2BYTE_CACHE = {i:bytes([i]) for i in range(256)}\n\n\ndef int2byte(character):\n    """Converts ('
```

