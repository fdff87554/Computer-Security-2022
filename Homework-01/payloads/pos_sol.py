from pwn import *


def main():
    # nc edu-ctf.zoolab.org 10101
    r = remote("edu-ctf.zoolab.org", 10101)
    
    # get iv and ct from server
    inp = bytes.fromhex(r.recvline().decode('utf-8').strip())
    
    # this is the iv and ct block
    ct_block = [inp[i:i+16] for i in range(0, len(inp), 16)]

    for i in range(len(ct_block) - 1):
        ans = []
        iv, ct = ct_block[i], ct_block[i+1]
        for j in range(1, len(iv) + 1):
            for k in range(1, 256):
                # Create target IV to loop out right PT byte for padding
                if j == 1:
                    tmp_iv = b'\x00' * (len(iv) - j) + bytes([k])
                else:
                    tmp_iv = b'\x00' * (len(iv) - j) + bytes([k]) + iv[-(j-1):]
                tmp = tmp_iv + ct
                r.sendline(tmp.hex())
                output = r.recvline()
                if b')' in output:
                    print(chr(tmp_iv[-j] ^ 0x80 ^ iv[-j]))
                    ans.append(chr(tmp_iv[-j] ^ 0x80 ^ iv[-j]))
                    if j == 1:
                        iv = iv[:-j] + bytes([0x80 ^ k])
                    else:
                        iv = iv[:-j] + bytes([0x80 ^ k]) + iv[-(j-1):]
                    break
        ans.reverse()
        print(''.join(ans))


if __name__ == "__main__":
    main()

# FLAG{ip4d_pr0_iS_r3ally_pr0_4Nd_f1aT!!!!}
