from manim import VGroup, Rectangle, RIGHT, DOWN, AnimationGroup, UP, Transform, ApplyFunction, ReplacementTransform, FadeTransform
from manim import Square, LEFT, Tex, PI, Arrow, DoubleArrow, ManimColor, GREEN, RED, YELLOW, WHITE
from manim.opengl import OpenGLVGroup

from numpy import array_equal, array
from _io import TextIOWrapper

from .hexdec import Hexadecimal, CodeBlock
from .funcs import inttstr, splithex, splitbin, inttobin


class MemoryBlock(VGroup):
	HORIZONTAL = 0
	VERTICAL = 1

	def __init__(self, 
							numBlocks=2, layout=HORIZONTAL, 
							startAddr=Hexadecimal("0x0"), endAddr=Hexadecimal("0x1"),
							blockWidth:float=-1, blockHeight:float=-1,
							start:int=0x0, end:int=0x1, **kwargs):
		'''
		'''
		if numBlocks <= 0: raise ValueError("Number of blocks cannot be 0 or negative.")

		super().__init__(**kwargs)

		self.start = start
		self.end = end

		# Allow the use of manually adding dimensions if something different needs to be done
		maxBlocks = 10
		scale = min(1, maxBlocks / numBlocks)
		if blockWidth	== -1 or blockHeight == -1:
			blockSize = 0.75 * scale

			aspectRatio = 1 if layout == self.HORIZONTAL else 1.5

			blockWidth = blockSize*aspectRatio if layout == self.VERTICAL else blockSize
			blockHeight = blockSize

		'''
		Order of this.VMobjects[]:
		0 -> blocks: VGroup
		1 -> startLabel: Hexadecimal
		2 -> endLabel: Hexadecimal
		3... -> byteData: Hexadecimal

		Order of the exact data depends on the order of this.setByte()
		'''

		self.blocks = VGroup(*[ Rectangle(width=blockWidth,height=blockHeight) for _ in range(numBlocks) ])
		self.layout = layout

		# byteData will hold the organized data bytes based on a provided index
		self.byteData:list[Hexadecimal|CodeBlock] = [None] * numBlocks

		if layout == self.HORIZONTAL:
			self.blocks.arrange(RIGHT, buff=0.03)
			labelDir = DOWN
		elif layout == self.VERTICAL:
			self.blocks.arrange(UP, buff=0.03)
			labelDir = RIGHT
		
		self.add(self.blocks)

		if startAddr != None and endAddr != None:
			self.textScale = scale * 0.75
			startLabel = startAddr.scale(self.textScale).next_to(self.blocks[0], labelDir, buff=0.1)
			self.add(startLabel)

			self.labels:list[Hexadecimal] = []

			endLabel = endAddr.scale(self.textScale).next_to(self.blocks[-1], labelDir, buff=0.1)
			self.add(endLabel)

	def transpose(self):
		aspectRatio:float|int = 0

		if self.layout == self.HORIZONTAL: 
			self.layout = self.VERTICAL
			aspectRatio = 1.5
			dir = UP
		else: 
			self.layout = self.HORIZONTAL
			aspectRatio = 1
			dir = RIGHT
		
		blockSize:float = self.blocks[0].width
		newBlockSize:float = blockSize * aspectRatio if self.layout == self.VERTICAL else blockSize

		animations:list[VGroup|Hexadecimal] = []

		newBlocks = VGroup()

		# FIXME/TODO: Looks very funky and I do not like it; this depends on transposing outside of this function
		for i, block in enumerate(self.blocks):
			newWidth:float = newBlockSize if array_equal(dir, UP) else blockSize
			newHeight:float = newBlockSize / (aspectRatio * 2) if array_equal(dir, UP) else blockSize
			# animations.append(block.animate.stretch_to_fit_width(newWidth).stretch_to_fit_height(newHeight))
			# animations.append(block.animate.stretch_to_fit_width(newWidth))
			# animations.append(block.animate.stretch_to_fit_height(newHeight))
			_blck = block.copy().stretch_to_fit_width(newWidth).stretch_to_fit_height(newHeight)

			animations.append(FadeTransform(block, _blck))
			self.remove(block)
			# self.blocks[i] = _blck
			newBlocks.add(_blck)
			# animations.append(Transform(block, block.copy().stretch_to_fit_width(newWidth).stretch_to_fit_height(newHeight), replace_mobject_with_target_in_scene=True))

			# print(f"After stretching [w,h]: {self.blocks[i].width}, {self.blocks[i].height}\n")

		# for i in range(len(self.blocks)): print(self.blocks[i].width)

		# animations.append(self.blocks.animate.arrange(dir, buff=0))


		# startLabel:Hexadecimal = self.submobjects[1]
		# endLabel:Hexadecimal = self.submobjects[2]

		# animations.append(startLabel.animate.next_to(self.blocks[0], RIGHT, buff=0.1))
		# animations.append(self.submobjects[2].animate.next_to(self.blocks[-1], RIGHT, buff=0.1))

		self.blocks = newBlocks

		return AnimationGroup(*animations)
	
	def updateTextPos(self):
		if self.layout == self.HORIZONTAL:
			dir = DOWN
		else:
			dir = RIGHT

		animations:list[Hexadecimal] = []

		startLabel:Hexadecimal = self.submobjects[1]
		endLabel:Hexadecimal = self.submobjects[2]

		animations.append(startLabel.animate.next_to(self.blocks[0], dir, buff=0.1))
		animations.append(endLabel.animate.next_to(self.blocks[-1], dir, buff=0.1))

		for block, data in zip(self.blocks, self.byteData):
			if data is not None:
				animations.append(data.animate.move_to(block.get_center()))
		
		return AnimationGroup(*animations)

	def showLabel(self, index:int) -> Hexadecimal:
		label = Hexadecimal(inttstr(self.start + index)).scale(self.textScale).next_to(self.blocks[index], RIGHT, buff=0.1)
		self.add(label)
		self.labels.append(label)
		return label.animate.fade(0).build()

	# def hideLabel(self, index:int) -> Hexadecimal:

	def getByte(self, index:int) -> Hexadecimal|CodeBlock: 
		return self.byteData[index]

	def initBytes(self, dataarr:list[Hexadecimal|CodeBlock]) -> None:
		for i,data in enumerate(dataarr):
			self.add(data)
			self.byteData[i] = data
			data.move_to(self.blocks[i].get_center())

	def setByte(self, index:int, data:Hexadecimal|CodeBlock) -> Hexadecimal|CodeBlock:
		# TODO: Have it such that the original size of data is irrelevant as the function will
		# automatically scale it in according to the size of the blocks
		self.add(data)
		self.byteData[index] = data
		# data exists in two places:
		# 	byteData: the organized array of bytes (to show proper order)
		# 	self.submobjects: the actual vgroup itself

		return data.animate.move_to(self.blocks[index].get_center())

	def clearByte(self, index:int):
		byte = self.byteData[index]

		# To clear a byte, it means to remove it from byteData and from the vgroup itself
		self.remove(byte)
		self.byteData[index] = None
		
		return byte.animate.fade(1).build()

	def highlightByte(self, index:int, color:str) -> Rectangle:
		return self.blocks[index].animate.set_color(color)
	
	def dehighlightByte(self, index:int) -> Rectangle:
		return self.blocks[index].animate.set_color("#ffffff")
	
	def dehighlightBytes(self) -> AnimationGroup:
		anims:list[Rectangle] = []

		for i in range(len(self.blocks)):
			anims.append(self.dehighlightByte(i))

		return AnimationGroup(*anims)

class Memory(VGroup):
	def __init__(self, kaddr:int, ndata:int):
		super().__init__()
		
		self.kaddr = kaddr
		self.ndata = ndata

		mem = VGroup()
		for _ in range(5):
			mem.add(Rectangle(height=3.5, width=0.5))
		mem.arrange(RIGHT, buff=0.4)
		mem.add(Square(4.5))

		
		self.addrbus:MemoryBlock = MemoryBlock(kaddr, startAddr=None, endAddr=None).scale(0.5).next_to(mem, UP, buff=0.5)
		# MemoryBlock is used for the buses even though the buses are not really memory
		# since the individual blocks are needed and MemoryBlock already comes with it
		# Might as well use it
		self.databus:MemoryBlock = MemoryBlock(ndata, startAddr=None, endAddr=None).scale(0.5).next_to(mem, DOWN, buff=0.5)

		self._re = Rectangle(height=0.65, width=0.45).next_to(mem, LEFT, buff=0).shift(UP*0.6)
		self._reText = Tex("\\verb|RE|").move_to(self._re.get_center()).rotate(PI/2)
		self._we = Rectangle(height=0.65, width=0.45).next_to(mem, LEFT, buff=0).shift(DOWN*0.6)
		self._weText = Tex("\\verb|WE|").move_to(self._we.get_center()).rotate(PI/2)

		addrArrow = Arrow(start=self.addrbus.get_bottom(), end=mem.get_top(), buff=0)
		dataArrow = DoubleArrow(start=mem.get_bottom(), end=self.databus.get_top(), buff=0)

		self.add(self.addrbus, self.databus, mem, self._re, self._we, self._reText, self._weText, addrArrow, dataArrow)

	def setWE(self, enable:bool = True) -> Rectangle: 
		color:ManimColor = None

		if enable: color = GREEN
		else: color = WHITE
		
		return self._we.animate.set_color(color)

	def setRE(self, enable:bool = True) -> Rectangle: 
		color:ManimColor = None

		if enable: color = GREEN
		else: color = WHITE
		
		return self._re.animate.set_color(color)

	def setAddr(self, addr:list[Hexadecimal]) -> AnimationGroup:
		anims:list[Hexadecimal] = []

		for k in range(self.kaddr):
			anims.append(self.addrbus.setByte(k, addr[k]))

		return AnimationGroup(*anims)

	def getAddr(self) -> list[Hexadecimal]:
		addr:list[Hexadecimal] = []

		for k in range(self.kaddr):
			addr.append(self.addrbus.getByte(k))

		return addr

	def setData(self, data:list[Hexadecimal]) -> AnimationGroup:
		anims:list[Hexadecimal] = []

		for n in range(self.ndata):
			anims.append(self.databus.setByte(n, data[n]))

		return AnimationGroup(*anims)

	def getData(self) -> list[Hexadecimal]:
		data:list[Hexadecimal] = []

		for n in range(self.ndata):
			data.append(self.databus.getByte(n))

		return data

	def getMemoryBlock(self, index:int) -> Rectangle:
		return self.submobjects[2][index]

class SplittableAddress(VGroup):
	def __init__(self, addr:int, binsections:list[int]=None, binary:bool=False, buff:float=0.05):
		super().__init__()

		self.addr = addr

		self.baseBin:Hexadecimal = None
		self.binarr:list[Hexadecimal] = None

		self.baseHex:Hexadecimal = None
		self.hexarr:list[Hexadecimal] = None

		if binary:
			self.baseBin = Hexadecimal(inttobin(addr))		
			self.binarr = [ Hexadecimal(val[2:]) for _,val in enumerate(splitbin(self.baseBin.value, binsections)) ]
		else:
			self.baseHex = Hexadecimal(inttstr(addr))
			self.hexarr = [ Hexadecimal(val[2:]) for _,val in enumerate(splithex(self.baseHex.value)) ]

		addrGroup = VGroup(Hexadecimal("0x" if not binary else "0b"), *(self.hexarr if not binary else self.binarr))
		addrGroup.arrange(RIGHT, buff)
		self.add(addrGroup)
		
	def highlightGroup(self, index:int) -> Hexadecimal:
		group:Hexadecimal = self.getGroup(index)

		return group.animate.set_color(YELLOW)
	
	def dehighlightGroup(self, index:int) -> Hexadecimal:
		group:Hexadecimal = self.getGroup(index)

		return group.animate.set_color(WHITE)

	def getGroup(self, index:int) -> Hexadecimal:
		return self.submobjects[0].submobjects[index+1]

class Instructions():
	LIMIT = 15

	def __init__(self, asmfile:str):
		infile = open(asmfile, "r")

		self.instructions:list[str] = []

		assembly, maxLen = self.__parseAssembly(infile)
		infile.close()

		self.assembly:list[str] = assembly
		self.maxLen = maxLen
		self.size = len(assembly)

	def getInstructionText(self, index:int) -> str:
		return self.instructions[index]

	def __parseAssembly(self, file:TextIOWrapper) -> tuple[list[str], int]:
		'''
		Parses the assembly file, taking out any labels. Assumes it is stripped of any other data that is not a label or instructions.
		This does not check the validity of the assembly.
		It also employs a limit to how many instructions it will allow to display.
		'''

		assembly:list[str] = []

		maxLen = 0
		line:str = file.readline()
		while line and len(assembly) <= self.LIMIT:
			line = self.__removeLabelComments(line)

			if line == "": 
				line = file.readline()
				continue

			self.instructions.append(line)
			assembly.append(line)

			currLen = len(line)
			if currLen > maxLen: maxLen = currLen

			line = file.readline()

		maxLine = maxLen

		# Running the execution requires an additional cycle for hlt to be processed
		self.instructions.append("hlt")


		assembly.reverse()

		return assembly, maxLine

	def __lexParseEncodeInstruction(self, line:str):
		pass

	def __removeLabelComments(self, line:str) -> str:
		new = line.strip()

		if new.endswith(":"): return ""

		return new

class InstructionMemory(MemoryBlock, Instructions):
	'''
	Specialized for creating a memory block/array for storing instructions.
	These instructions come from an assembly file.
	'''

	def __init__(self, asmfile:str, entry:int, entryAddr:Hexadecimal):
		Instructions.__init__(self, asmfile)

		widthScaling = 0.2
		heightScaling = 0.1142
		fontScaling = 10
		blockWidth = self.maxLen * widthScaling
		blockHeight = 0.64 / (self.size * heightScaling)
		fontSize = 0.1 * blockWidth * fontScaling + 32.4

		# print(f"Number of instr: {self.size}; Font size: {fontSize}; Height: {blockHeight}; Width: {blockWidth}; Max len: {self.maxLen}")

		MemoryBlock.__init__(self,
			numBlocks=self.size, layout=self.VERTICAL, 
			startAddr=Hexadecimal(hex(entry+self.size-1)), endAddr=entryAddr,
			blockWidth=blockWidth, blockHeight=blockHeight,
			start=entry+self.size-1, end=entry
		)

		self.initBytes([CodeBlock(instr, fontSize=fontSize) for instr in self.assembly])
