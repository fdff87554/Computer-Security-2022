from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes


while True:
    r = remote("edu-ctf.zoolab.org", 10104)
    p = int(r.recvline().decode('utf-8').strip())
    if (p - 1) % 3 != 0:
        r.close()
        continue
    g = pow(2, (p - 1) // 3, p)
    r.sendline(str(g))
    output = r.recvline()
    if b'Bad :(' not in output:
        print(output)
        print(long_to_bytes(int(output)))
        break
    r.close()
    continue

# FLAG{M4yBe_i_N33d_70_checK_7he_0rDEr_OF_G}