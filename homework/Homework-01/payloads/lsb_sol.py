from pwn import *
from Crypto.Util.number import long_to_bytes


def main():
    # nc edu-ctf.zoolab.org 10102
    r = remote("edu-ctf.zoolab.org", 10102)
    n = int(r.recvline().decode('utf-8').strip())
    e = int(r.recvline().decode('utf-8').strip())
    e_p = [pow(3, -e*i, n) for i in range(1500)]
    e_pi = [pow(3, -i, n) for i in range(1500)]
    enc = int(r.recvline().decode('utf-8').strip())
    
    pt = 0
    dig = []
    
    # while True:
    for i in range(1300):
        enc_1 = (enc * e_p[i]) % n
        # lsb oracle
        r.sendline(str(enc_1))
        p = int(r.recvline().decode('utf-8').strip())
        sub = 0
        for j in range(i):
            sub = (sub + e_pi[i-j]*dig[j]) % n
        p = (p - sub) % 3
        dig = dig + [p]
        i += 1
        if i % 100 == 0:
            print(i)
    
    pt = ''.join([str(x) for x in dig[::-1]])
    print(long_to_bytes(int(pt, 3)))
    # b'FLAG{lE4ST_519Nific4N7_Bu7_m0S7_1MporT4Nt}\xbc\x86zP\xc6\xce \x9bSy;\x95\xa3\xea\xd9w\xc4\xd5\xb1\x86[\xf2L\xfb\x97}\xa2\x7f\xd3D|+\x9f\x82=\xe8\xfe\x8b\x95\xc5\xe3\xaf\xb5g\xf9\x88\x02\xbcGy=\xb5\x1eP\x07\xd8a_\xcaX\x91\x15\x06\x11G-s]~?UJ\x1dd.\x8b\xec\x90\xd6\xd1\xb8\xf7\xfa\xf5\x11\xc0\x95`W\xe431\xb9\x95\xddd\x17\xc7Q^\xb2\x16\x19\x7f\x11\t$\xcc.\x82\xe9\xd7P\xe7\x82\x19\x01\x06S\xa3\x84w\x15a\xa2-*\xaa\xf0Z\xf2\xe4K\xc9S\xa9,\xf6\x04\x9f\xc1Z]\xe7# F\r\xe3:\xbeuu#\xd5O\n\x0e\x87a}u5\xb4\xa1\xb6\x86\xf9\xe1 \x89A\xce\x98W\xdfG\x90nj\x05\x8au[\xae}\xcd\xe4\xc5\xba\x8dU\xd4\x9e\xb0\xa4\x9bf\xe639\xce\x87\x1c\xc0%&\x00\xe8\xd1\x90\x03\x9c\xc1'

if __name__ == "__main__":
    main()
