#!/usr/bin/env python3
"""Pure Python MD5 implementation."""
import struct,sys,math
T=[int(2**32*abs(math.sin(i+1)))&0xffffffff for i in range(64)]
S=[[7,12,17,22]*4,[5,9,14,20]*4,[4,11,16,23]*4,[6,10,15,21]*4]
S=[x for r in S for x in r]
def lr(x,n): return ((x<<n)|(x>>(32-n)))&0xffffffff
def md5(msg):
    if isinstance(msg,str): msg=msg.encode()
    ml=len(msg)*8
    msg+=b"\x80"
    while len(msg)%64!=56: msg+=b"\x00"
    msg+=struct.pack("<Q",ml)
    a0,b0,c0,d0=0x67452301,0xefcdab89,0x98badcfe,0x10325476
    for i in range(0,len(msg),64):
        M=[struct.unpack("<I",msg[i+j:i+j+4])[0] for j in range(0,64,4)]
        A,B,C,D=a0,b0,c0,d0
        for j in range(64):
            if j<16: F=(B&C)|((~B)&D);g=j
            elif j<32: F=(D&B)|((~D)&C);g=(5*j+1)%16
            elif j<48: F=B^C^D;g=(3*j+5)%16
            else: F=C^(B|(~D));g=(7*j)%16
            F=(F+A+T[j]+M[g])&0xffffffff
            A,D,C,B=D,C,B,(B+lr(F,S[j]))&0xffffffff
        a0=(a0+A)&0xffffffff;b0=(b0+B)&0xffffffff;c0=(c0+C)&0xffffffff;d0=(d0+D)&0xffffffff
    return struct.pack("<4I",a0,b0,c0,d0).hex()
if __name__=="__main__":
    import hashlib
    for t in ["","abc","hello"]:
        assert md5(t)==hashlib.md5(t.encode()).hexdigest()
    print("All MD5 tests passed")
    if len(sys.argv)>1: print(md5(sys.argv[1]))
