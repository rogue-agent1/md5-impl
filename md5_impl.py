#!/usr/bin/env python3
"""md5_impl - Pure Python MD5 implementation."""
import sys, struct, math

def _left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

T = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
S = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4

def md5(message):
    if isinstance(message, str):
        message = message.encode()
    msg = bytearray(message)
    orig_len = len(msg) * 8
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += struct.pack("<Q", orig_len)
    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    for i in range(0, len(msg), 64):
        M = list(struct.unpack("<16I", msg[i:i+64]))
        A, B, C, D = a0, b0, c0, d0
        for j in range(64):
            if j < 16:
                F = (B & C) | (~B & D) & 0xFFFFFFFF
                g = j
            elif j < 32:
                F = (D & B) | (~D & C) & 0xFFFFFFFF
                g = (5 * j + 1) % 16
            elif j < 48:
                F = B ^ C ^ D
                g = (3 * j + 5) % 16
            else:
                F = C ^ (B | ~D) & 0xFFFFFFFF
                g = (7 * j) % 16
            F = (F + A + T[j] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + _left_rotate(F, S[j])) & 0xFFFFFFFF
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF
    return struct.pack("<4I", a0, b0, c0, d0).hex()

def test():
    import hashlib
    assert md5("") == hashlib.md5(b"").hexdigest()
    assert md5("abc") == hashlib.md5(b"abc").hexdigest()
    assert md5("hello world") == hashlib.md5(b"hello world").hexdigest()
    assert md5("a" * 100) == hashlib.md5(b"a" * 100).hexdigest()
    print("OK: md5_impl")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: md5_impl.py test")
