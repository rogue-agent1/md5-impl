#!/usr/bin/env python3
"""md5_impl - MD5 from scratch (no hashlib)."""
import argparse, struct, sys, math

T = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
S = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4

def left_rotate(x, c): return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

def md5(data: bytes) -> str:
    a0,b0,c0,d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    msg = bytearray(data)
    ml = len(data) * 8
    msg.append(0x80)
    while len(msg) % 64 != 56: msg.append(0)
    msg += struct.pack('<Q', ml)
    for i in range(0, len(msg), 64):
        M = struct.unpack('<16I', msg[i:i+64])
        A, B, C, D = a0, b0, c0, d0
        for j in range(64):
            if j < 16: F = (B & C) | (~B & D); g = j
            elif j < 32: F = (D & B) | (~D & C); g = (5*j+1) % 16
            elif j < 48: F = B ^ C ^ D; g = (3*j+5) % 16
            else: F = C ^ (B | ~D); g = (7*j) % 16
            F = (F + A + T[j] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, S[j])) & 0xFFFFFFFF
        a0 = (a0+A) & 0xFFFFFFFF; b0 = (b0+B) & 0xFFFFFFFF
        c0 = (c0+C) & 0xFFFFFFFF; d0 = (d0+D) & 0xFFFFFFFF
    return struct.pack('<4I', a0, b0, c0, d0).hex()

def main():
    p = argparse.ArgumentParser(description="MD5 from scratch")
    p.add_argument("input", nargs="?")
    p.add_argument("-s", "--string")
    args = p.parse_args()
    if args.string: data = args.string.encode()
    elif args.input: data = open(args.input, "rb").read()
    else: data = sys.stdin.buffer.read()
    print(md5(data))

if __name__ == "__main__":
    main()
