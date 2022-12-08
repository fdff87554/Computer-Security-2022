from Crypto.Util.number import long_to_bytes


flag_len = 336
output = [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
F = GF(2^65)
poly = 0x1da785fc480000001
FF.<x> = GF(2^64, modulus=F.fetch_int(poly))

# x^64 + x^63 + x^62 + x^60 + x^59 + x^57 + x^54 + x^53 + x^52 + x^51 + x^46 + x^44 + x^43 + x^42 + x^41 + x^40 + x^39 + x^38 + x^34 + x^31 + 1
# 0x0000000000000001

def gf_getbit():
	global init_state
	init_state *= (x^36)
	ret = (init_state.integer_representation() >> 63 ) & 1
	init_state *= (x^1)
	return ret

def getbit():
	global state
	state <<= 1
	if state & (1 << 64):
		state ^^= poly
		return 1
	return 0

cur_state = (x^36)
cm = []
for _ in range(64):
	tmp = []
	for bit in range(64):
		cur_bit = ((x^bit) * cur_state)
		cur_bit = cur_bit.integer_representation()
		cur_bit = (cur_bit >> 63) & 1
		tmp.append(cur_bit)
	cur_state *= (x^37)
	cm.append(tmp)

cm = Matrix(FF, cm)
vec = Matrix(FF, output[-70:-6]).T
ret = (cm^-1)*vec
ret = (ret.T)[0]

init_state = 0
for i in range(64):
    init_state += ret[i]*x^i

init_state *= (x^-(37*336))
state = init_state.integer_representation()
print(hex(init_state.integer_representation()))

xorkey = []
for i in range(len(output)-70):
	for _ in range(36):
		getbit()
	ori_bit = getbit()
	gf_bit = gf_getbit()
	assert(ori_bit==gf_bit)
	xorkey.append(gf_bit)

print('xorkey', xorkey)
flag = ''.join([ str(a^^b) for a,b in zip(xorkey,output[:-70])])
print(flag)
flag = long_to_bytes(int(flag,2))
print(flag)
