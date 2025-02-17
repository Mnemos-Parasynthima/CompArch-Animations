from manim import VGroup, Rectangle, RIGHT, DOWN, AnimationGroup, UP, Transform, ApplyFunction, ReplacementTransform, FadeTransform
from manim.opengl import OpenGLVGroup
from numpy import array_equal
from .hexdec import Hexadecimal
from .funcs import inttstr


class MemoryBlock(VGroup):
	HORIZONTAL = 0
	VERTICAL = 1

	def __init__(self, numBlocks=2, layout=HORIZONTAL, startAddr=Hexadecimal("0x0"), endAddr=Hexadecimal("0x1"), scale:int=-1, start:int=0x0, end:int=0x1, **kwargs):
		super().__init__(**kwargs)

		self.start = start
		self.end = end

		maxBlocks = 10
		if scale == -1: scale = min(1, maxBlocks / numBlocks)
		blockSize = 0.75 * scale

		aspectRatio = 1 if layout == self.HORIZONTAL else 1.5

		'''
		Order of this.VMobjects[]:
		0 -> blocks: VGroup
		1 -> startLabel: Hexadecimal
		2 -> endLabel: Hexadecimal
		3... -> byteData: Hexadecimal

		Order of the exact data depends on the order of this.setByte()
		'''

		self.blocks = VGroup(*[
			Rectangle(width=blockSize*aspectRatio,height=blockSize) if layout==self.VERTICAL
			else Rectangle(width=blockSize,height=blockSize) for _ in range(numBlocks)
		])
		self.layout = layout

		# byteData will hold the organized data bytes based on a provided index
		self.byteData:list[Hexadecimal] = [None] * numBlocks

		if layout == self.HORIZONTAL:
			self.blocks.arrange(RIGHT, buff=0)
			labelDir = DOWN
		elif layout == self.VERTICAL:
			self.blocks.arrange(UP, buff=0)
			labelDir = RIGHT
		
		self.add(self.blocks)

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


	def setByte(self, index:int, data:Hexadecimal) -> Hexadecimal:
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