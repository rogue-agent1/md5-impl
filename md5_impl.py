#!/usr/bin/env python3
"""MD5 hash from scratch."""
import sys,struct,math
T=[int(2**32*abs(math.sin(i+1)))&0xFFFFFFFF for i in range(64)]
S=[7,12,17,22]*4+[5,9,14,20]*4+[4,11,16,23]*4+[6,10,15,21]*4
M=0xFFFFFFFF
def left_rotate(x,n): return ((x<<n)|(x>>(32-n)))&M
def md5(msg):
    if isinstance(msg,str): msg=msg.encode()
    orig_len=len(msg)*8; msg+=b'\x80'
    while len(msg)%64!=56: msg+=b'\x00'
    msg+=struct.pack('<Q',orig_len)
    a0,b0,c0,d0=0x67452301,0xefcdab89,0x98badcfe,0x10325476
    for i in range(0,len(msg),64):
        M16=struct.unpack('<16I',msg[i:i+64])
        A,B,C,D=a0,b0,c0,d0
        for j in range(64):
            if j<16: F=(B&C)|((~B)&D); g=j
            elif j<32: F=(D&B)|((~D)&C); g=(5*j+1)%16
            elif j<48: F=B^C^D; g=(3*j+5)%16
            else: F=C^(B|(~D)&M); g=(7*j)%16
            F=(F+A+T[j]+M16[g])&M
            A,D,C,B=D,C,B,(B+left_rotate(F,S[j]))&M
        a0,b0,c0,d0=(a0+A)&M,(b0+B)&M,(c0+C)&M,(d0+D)&M
    return struct.pack('<4I',a0,b0,c0,d0).hex()
def main():
    if "--demo" in sys.argv:
        for m,e in [("","d41d8cd98f00b204e9800998ecf8427e"),("abc","900150983cd24fb0d6963f7d28e17f72")]:
            h=md5(m); print(f"md5('{m}')={h} {'✓' if h==e else '✗'}")
    elif len(sys.argv)>1: print(md5(sys.argv[1]))
    else: print(md5(sys.stdin.buffer.read()))
if __name__=="__main__": main()
