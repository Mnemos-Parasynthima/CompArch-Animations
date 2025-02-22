from random import randint


def inttstr(num:int) -> str:
	'''
	Converts the given number to its hexadecimal representation as a string.
	'''

	lookup = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

	hexstr = ""

	while (num):
		lsnib = num & 0xf
		num = num >> 4
		hexstr += lookup[lsnib]

	if len(hexstr) <= 1: hexstr += "0"

	hexstr += "x0"

	return hexstr[::-1]

def inttobin(num:int) -> str:
	'''
	Converts the given number to its binary representation as a string.
	'''
	
	lookup = ["0", "1"]

	binstr = ""

	while (num):
		lsbit = num & 0b1
		num = num >> 1
		binstr += lookup[lsbit]

	if len(binstr) <= 1: binstr += "0"

	binstr += "b0"

	return binstr[::-1]

def splithex(hexstr:str) -> list[str]:
	'''
	Splits the given string, representing a hexadecimal, into byte components,
	returning a list of such components where the 0th element is the most significant
	byte.
	'''

	hexstr = hexstr[2:]

	# In the case that the hexstring is something likee ff2, there needs to be a 0
	# in front of the first f -> 0x0f, 0xf2
	if len(hexstr) % 2 != 0: hexstr = "0" + hexstr

	_bytes = [ hexstr[i:i+2] for i in range(0, len(hexstr), 2) ]
	arr = [f"0x{byte}" for byte in _bytes]	

	return arr

def splitbin(binstr:str, lenbits:list[int]=None) -> list[str]:
	'''
	Splits the given string, representing a binary, into components determined by the given lengths.
	If none, it defaults to bytes (lenbits=8). It returns a list of such components where the 0th element is the most significant portion.

	lenbits is to be in the format of:
	lenbits[0] = number of bits to be included from the most significant bits
	'''


	binstr = binstr[2:]

	if lenbits: assert(sum(lenbits) == len(binstr))

	if len(binstr) % 2 != 0: binstr = "0" + binstr

	if not lenbits:
		bits = [ binstr[i:i+8] for i in range(0, len(binstr), 8)]
	else:
		bits = []
		binstrIdx = 0
		lenbitsIdx = 0
		while binstrIdx < len(binstr):
			size = lenbits[lenbitsIdx]

			bits.append(binstr[binstrIdx:binstrIdx+size])
			lenbitsIdx += 1
			binstrIdx += size

	arr = [f"0b{comp}" for comp in bits]

	return arr

def randomHexByte() -> str:
	byteint = randint(0, 255)

	# return inttstr(0)[2:]
	return (inttstr(byteint))[2:]