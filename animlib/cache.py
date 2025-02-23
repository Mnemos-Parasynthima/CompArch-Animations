from manim import VGroup, Square, LEFT, RIGHT, UP, DOWN, MathTex, WHITE, Rectangle, ManimColor
from math import log2

from .hexdec import Hexadecimal
from .funcs import randomHexBytes, inttstr

class Set(VGroup):
	def __init__(self, blockSize:int):
		super().__init__()

		self.tag:int = 0x0
		randomHex = randomHexBytes(0xfff)
		if len(randomHex) < 3: randomHex = "0" + randomHex
		self.tagText = Hexadecimal(randomHex, "white", 30)

		self.dirty:int = 0
		self.dirtyText = MathTex("0").scale(0.8)

		self.valid:int = 0
		self.validText = MathTex("0").scale(0.8)

		self.data:list[int] = [-1]*blockSize
		self.dataText:list[Hexadecimal] = [ Hexadecimal(randomHexBytes(), "white", 30) for i in range(blockSize) ]

		self.cacheLineSize = blockSize

		# Add squares for the tag, dirty, and valid
		self.add(Rectangle(height=0.6, width=self.tagText.width + 0.2))
		for i in range(2):
			self.add(Square(0.6))

		for i in range(blockSize):
			self.add(Square(0.6))

		self.arrange(RIGHT, buff=0.01)

		self.add(self.tagText.move_to(self.submobjects[0].get_center()))
		self.add(self.dirtyText.move_to(self.submobjects[1].get_center()))
		self.add(self.validText.move_to(self.submobjects[2].get_center()))

		for i in range(blockSize):
			idx = i+3
			self.add(self.dataText[i].move_to(self.submobjects[idx].get_center()))

	def getByte(self, tag:int, offset:int) -> tuple[int, Hexadecimal]:
		print("Getting byte with tag 0x{0:x} and offset {1:d}".format(tag, offset))
		# print(self.data[offset])
		# print(self.dataText[offset])
		# print(self.tag)

		if not self.valid: return -1, None

		if self.tag != tag: return -1, None

		return self.data[offset], self.dataText[offset]
	
	def setByte(self, tag:int, offset:int, data:Hexadecimal) -> tuple[Hexadecimal, MathTex, MathTex]:
		self.valid = 1
		self.tag = tag

		validText = self.validText
		self.validText = MathTex("1").scale(0.8).move_to(validText.get_center())

		tagText = self.tagText
		self.tagText = Hexadecimal(inttstr(tag)[2:], "white", 30).move_to(tagText.get_center())

		dataText = self.dataText[offset]
		self.dataText[offset] = data.move_to(dataText.get_center())#Hexadecimal(inttstr(data)[2:], fontSize=30).move_to(dataText.get_center())

		self.data[offset] = int(data.value, 16)

		return (dataText.animate.become(self.dataText[offset]).build(),
						# data.animate.move_to(self.submobjects[offset+2].get_center()),
						validText.animate.become(self.validText).build(), tagText.animate.become(self.tagText).build())

	def initBytes(self, _set:list[tuple[int, int, int, int]]):
		# print(f"Setting 0x{_set[0][3]:x} at {_set[0][2]} with tag 0x{_set[0][0]:x}")

		subobjOffset = 3 + self.cacheLineSize

		self.tag = _set[0][0] # Since the tag of all tuples in the list are the same, doesn't matter which one
		oldTagText = self.tagText
		self.tagText = Hexadecimal(inttstr(_set[0][0])[2:], "white", 30).move_to(oldTagText.get_center())
		self.submobjects[subobjOffset + 0] = self.tagText

		self.valid = 1
		oldValidText = self.validText
		self.validText = MathTex("1").scale(0.8).move_to(oldValidText.get_center())
		self.submobjects[subobjOffset + 2] = self.validText

		# What matters now is offset (tuple[2]) and data (tuple[3])
		# Not guaranteed that it is ordered by increasing offset

		for _tuple in _set:
			offset = _tuple[2]
			data = _tuple[3]

			self.data[offset] = data

			oldDataText = self.dataText[offset]
			self.dataText[offset] = Hexadecimal(inttstr(data)[2:], "white", 30).move_to(oldDataText.get_center())
			self.submobjects[subobjOffset + 3 + offset] = self.dataText[offset]		

class Way(VGroup):
	def __init__(self, blockSize:int, sets:int):
		super().__init__()

		self.sets:list[Set] = []

		for _ in range(sets):
			self.sets.append(Set(blockSize))

		self.add(*self.sets)
		self.arrange(DOWN, buff=0.01)

	def getByte(self, tag:int, setIndex:int, offset:int) -> tuple[int, Hexadecimal]:
		# print("Getting byte for tag 0x{0:x} with set index of {1:d} and offset of {2:d}".format(tag, setIndex, offset))

		return self.sets[setIndex].getByte(tag, offset)
	
	def setByte(self, tag:int, setIndex:int, offset:int, data:Hexadecimal) -> tuple[Hexadecimal, MathTex, MathTex]:
		return self.sets[setIndex].setByte(tag, offset, data)

	def initBytes(self, way:list[tuple[int, int, int, int]]):
		# Will initBytes in one go for each set
		# That is, all tuples with the same seti (different offsets) and same tag for one set, etc
		# Allows only one access to each set

		sets:list[list[tuple[int, int, int, int]]] = [[] for _ in range(len(self.sets))]

		# Even though tuples with the same seti (and same tag) are placed next to each other
		# split them
		for _datatuple in way:
			seti = _datatuple[1]

			sets[seti].append(_datatuple)

		for i, _set in enumerate(self.sets):
			if sets[i]: _set.initBytes(sets[i])

class Cache(VGroup):
	def __init__(self, A:int, B:int, C:int, wordsize:int):
		'''
		Parameters
		----------
		A
			Associativity (number of ways).
		B
			Number of bytes per line (in one way) or the cache line size.
		C
			Total capacity of the cache in bytes.
		'''
		super().__init__()

		self.wordsize = wordsize

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

	def __str__(self):
		return (f"Cache of: Associativity: {self.assoc}; Line size: {self.blockSize} ({self.b} bits); " 
			f"Capacity: {self.capacity}; Sets: {self.sets} ({self.s} bits). Using {self.t} bits for tag. Wordsize of {self.wordsize}.")

	def getByte(self, addr:int) -> tuple[int, Hexadecimal]:
		tag, seti, offset = self._splitAddr(addr)

		# print("0b{0:b}".format(addr))
		# print("0b{0:b}, 0b{1:b}, 0b{2:b}".format(tag, seti, offset))

		for way in self.ways:
			# Iterating through the ways since the current way may not have the tag
			byte, byteText = way.getByte(tag, seti, offset)
			if byteText != None: return byte, byteText

		return -1, None

	def setByte(self, addr:int, data:Hexadecimal, way:int) -> tuple[Hexadecimal, MathTex, MathTex]:
		tag, seti, offset = self._splitAddr(addr)

		# print("0x{0:x}, 0x{1:b}, 0x{2:x}".format(tag, seti, offset))

		# No need to manage "replacement" here, can simply provide the Way
		return self.ways[way].setByte(tag, seti, offset, data)
		
	def initBytes(self, dataarr:list[tuple[int, int]]):
		data:list[tuple[int, int, int, int]] = []

		# [(tag, seti, offset, data), (...), ...]

		for _, (addr, _data) in enumerate(dataarr):
			tag, seti, offset = self._splitAddr(addr)
			
			dataTuple = (tag, seti, offset, _data)
			data.append(dataTuple)

		# Will initBytes in one go for each way
		# That is, group all tuples with non-equal seti for one way, the next group for the next way, etc
		# Allows only one access to each way

		def sortfunc(val): return val[1]
		data.sort(key=sortfunc)

		ways:list[list[tuple[int, int, int, int]]] = [[] for _ in range(self.assoc)]

		# Place tuples in such way that allows a way to place all its data lines as appropriate
		for _datatuple in data:
			for i, way in enumerate(ways):
				# only add the _datatuple in way if there is no other tuple with the same seti
				# since each way only has one cache line
				# but keep in same way only if same tag

				added = False

				if len(way) == 0:
					way.append(_datatuple)
					break

				for _tuple in way:
					# print("Looking to add _datatuple")
					# sleep(2)
					if _tuple[1] == _datatuple[1] and _tuple[0] != _datatuple[0]:
						# data that has the same set index as _datatuple already exists in this way but do not have same tag
						# go to the next way
						break
				else:
					way.append(_datatuple)
					added = True
					break

				if added: break

		for i, way in enumerate(self.ways):
			way.initBytes(ways[i])

	def highlightSet(self, index:int, way:int, color:ManimColor) -> Set:
		return self.ways[way].sets[index].animate.set_color(color)

	def dehighlightSet(self, index:int, way:int) -> Set:
		return self.ways[way].sets[index].animate.set_color(WHITE)

	def _splitAddr(self, addr:int) -> tuple[int, int, int]:
		offset = addr & (2**self.b - 1)
		seti = (addr >> self.b) & (2**self.s - 1)
		# print("0b{0:b}".format(2**self.s-1))
		tag = (addr >> (self.b + self.s)) & (2**self.t - 1)
		
		return tag, seti, offset

	def _validAddr(self, addr:int) -> bool: pass
