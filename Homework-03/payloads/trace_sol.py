tmp = [0x37, 0x3D, 0x30, 0x36, 0x0A, 0x25, 0x3, 0x30, 0x12, 0x42, 0x2E, 0x3C, 0x42, 0x2E, 0x40, 0x37, 0x2E, 0x24, 0x2E, 0x12, 0x30, 0x3F, 0x0C, 0x0]

for i in range(len(tmp)):
    tmp[i] = tmp[i] ^ 0x71

print("".join([chr(i) for i in tmp]))