keys = [0x8D909984B8BEBAB3, 0x8D9A929E98D18B92, 0x0D0888BD19290D29C, 0x8C9DC08F978FBDD1, 0x0D9C7C7CCCDCB92C2, 0x0C8CFC7CEC2BE8D91, 0x0FFFFFFFFFFFFCF82]

for i in range(len(keys)):
    tmp = hex(keys[i])[2:]
    tmp = tmp[:12] + tmp[14:] + tmp[12:14]
    keys[i] = int(f"0x{tmp}", base=16)

for i in range(len(keys)):
    
    # print( bytes.fromhex(hex((~keys[i] & 0xFFFFFFFFFFFFFFFF) + 1)[2:])[::-1].decode('utf-8'), end='' )
    print( bytes.fromhex(hex(~keys[i] + 1 & 0xFFFFFFFFFFFFFFFF)[2:])[::-1].decode('utf-8'), end='' )
