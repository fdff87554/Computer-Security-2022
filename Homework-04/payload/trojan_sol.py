tmp = "0vCh8RrvqkrbxN9Q7Ydx"
keys = [ord(t) for t in tmp]
keys.append(0x00)


with open('tmp.txt', 'r',encoding="unicode_escape") as fp:
    inp = fp.read()
    # hex_list = ["{:02x}".format(ord(c)) for c in fp.read()]

hex_list = bytes.fromhex(inp)

answer = []
for i in range(len(hex_list)):
    ans = hex(hex_list[i] ^ keys[i%21])[2:]
    if len(ans) == 1:
        ans = "0" + ans

    answer.append(ans)
print("".join(answer))