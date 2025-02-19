from random import randint


def inttstr(num:int) -> str:
	'''
	Converts the given number to its hexadecimal representation as a string.
	'''

	lookup:list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

	hexstr:str = ""

	while (num):
		lsbit:int = num & 0xf
		num = num >> 4
		hexstr += lookup[lsbit]

	if len(hexstr) == 1: hexstr += "0"

	hexstr += "x0"

	return hexstr[::-1]

def splithex(hexstr:str) -> list[str]:
	'''
	Splits the given string, representing a hexadecimal, into byte components,
	returning a list of such components where the 0th element is the most significant
	byte.
	'''

	hexstr = hexstr[2:]

	# In the case that the hexstring is something likee ff2, there needs to be a 0
	# in front of the first f -> 0x0f, 0xf2
	if len(hexstr) % 2 != 0:
		hexstr = "0" + hexstr

	_bytes = [ hexstr[i:i+2] for i in range(0, len(hexstr), 2) ]
	arr = [f"0x{byte}" for byte in _bytes]	

	return arr

def randomHexByte() -> str:
	byteint = randint(0, 255)

	return (inttstr(byteint))[2:]