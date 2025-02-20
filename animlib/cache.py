from manim import VGroup, Square, LEFT, RIGHT, UP, DOWN, MathTex, WHITE
from math import log2

from .hexdec import Hexadecimal
from .funcs import randomHexByte, inttstr

class Set(VGroup):
	def __init__(self, blockSize:int):
		super().__init__()

		self.tag:int = 0x0
		self.tagText:Hexadecimal = Hexadecimal(randomHexByte(), "white", 30)

		self.valid:int = 0
		self.validText:MathTex = MathTex("0").scale(0.8)

		self.data:list[int] = []
		self.dataText:list[Hexadecimal] = [ Hexadecimal(randomHexByte(), "white", 30) for i in range(blockSize) ]

		for i in range(2):
			self.add(Square(0.6))

		for i in range(blockSize):
			self.add(Square(0.6))

		self.arrange(RIGHT, buff=0.01)

		self.add(self.tagText.move_to(self.submobjects[0].get_center()))
		self.add(self.validText.move_to(self.submobjects[1].get_center()))

		for i in range(blockSize):
			idx = i+2
			self.add(self.dataText[i].move_to(self.submobjects[idx].get_center()))

	def getByte(self, tag:int, offset:int) -> tuple[int, Hexadecimal]:
		# print("Getting byte with tag 0x{0:x}".format(tag))

		if not self.valid: return -1, None

		if self.tag != tag: return -1, None

		return self.data[offset], self.dataText[offset+2]
	
	def setByte(self, tag:int, offset:int, data:int) -> tuple[Hexadecimal, MathTex, MathTex]:
		self.valid = 1
		self.tag = tag

		validText = self.validText
		self.validText = MathTex("1").scale(0.8).move_to(validText.get_center())

		tagText = self.tagText
		self.tagText = Hexadecimal(inttstr(tag)[2:], "white", 30).move_to(tagText.get_center())

		dataText = self.dataText[offset]
		self.dataText[offset] = data.move_to(dataText.get_center())#Hexadecimal(inttstr(data)[2:], fontSize=30).move_to(dataText.get_center())

		return (dataText.animate.become(self.dataText[offset]),
						# data.animate.move_to(self.submobjects[offset+2].get_center()),
						validText.animate.become(self.validText), tagText.animate.become(self.tagText))


class Way(VGroup):
	def __init__(self, blockSize:int, sets:int):
		super().__init__()

		self.sets:list[Set] = []

		for _set in range(sets):
			self.sets.append(Set(blockSize))

		self.add(*self.sets)
		self.arrange(DOWN, buff=0.01)

	def getByte(self, tag:int, setIndex:int, offset:int) -> tuple[int, Hexadecimal]:
		# print("Getting byte for tag 0x{0:x} with set index of {1:d} and offset of {2:d}".format(tag, setIndex, offset))

		return self.sets[setIndex].getByte(tag, offset)
	
	def setByte(self, tag:int, setIndex:int, offset:int, data:Hexadecimal) -> tuple[Hexadecimal, MathTex, MathTex]:
		return self.sets[setIndex].setByte(tag, offset, data)

class Cache(VGroup):
	def __init__(self, A:int, B:int, C:int):
		'''
		Parameters
		----------
		A
			Associativity (number of ways).
		B
			Number of bytes per line (in one way).
		C
			Total capacity of the cache in bytes.
		'''
		super().__init__()

		self.wordsize = 12

		self.assoc = A
		self.blockSize = B
		self.capacity = C
		self.sets = C // (A * B)

		# Used for address splitting
		self.b:int = int(log2(B))
		self.s:int = int(log2(self.sets))
		self.t:int = self.wordsize - self.s - self.b

		self.ways:list[Way] = []

		for i in range(A):
			self.ways.append(Way(B, self.sets))

		self.add(*self.ways)
		self.arrange(RIGHT, buff=0.25)

	def getByte(self, addr:int) -> tuple[int, Hexadecimal]:
		tag, seti, offset = self._splitAddr(addr)

		# print("0b{0:b}".format(addr))
		# print("0b{0:b}, 0b{1:b}, 0b{2:b}".format(tag, seti, offset))

		for way in self.ways:
			# Iterating through the ways since the current way may not have the tag
			byte, byteText = way.getByte(tag, seti, offset)
			if byteText != None: return byte, byteText

		return -1, None

	def setByte(self, addr:int, data:Hexadecimal) -> tuple[Hexadecimal, MathTex, MathTex]:
		tag, seti, offset = self._splitAddr(addr)

		for way in self.ways:
			return way.setByte(tag, seti, offset, data)
		
		return None, None, None
		

	def _splitAddr(self, addr:int) -> tuple[int, int, int]:
		offset = addr & (2**self.b - 1)
		seti = (addr >> self.b) & (2**self.s - 1)
		# print("0b{0:b}".format(2**self.s-1))
		tag = (addr >> (self.b + self.s)) & (2**self.t - 1)
		
		return tag, seti, offset

	def _validAddr(self, addr:int) -> bool: pass
