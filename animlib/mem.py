from manim import VGroup, Square, RIGHT, DOWN, AnimationGroup, UP, Transform, ApplyFunction
from .hexdec import Hexadecimal

class MemoryBlock(VGroup):
	HORIZONTAL = 0
	VERTICAL = 1

	def __init__(self, numBlocks=2, layout=HORIZONTAL, startAddr=Hexadecimal("0x0"), endAddr=Hexadecimal("0x1"), **kwargs):
		super().__init__(**kwargs)

		'''
		Order of this.VMobjects[]:
		0 -> blocks: VGroup
		1 -> startLabel: Hexadecimal
		2 -> endLabel: Hexadecimal
		3... -> data: Hexadecimal

		Order of the exact data depends on the order of this.setByte()
		'''

		self.blocks = VGroup(*[Square(side_length=1) for _ in range(numBlocks)])
		self.layout = layout
		self.data:list[Hexadecimal] = [None] * numBlocks

		if layout == self.HORIZONTAL:
			self.blocks.arrange(RIGHT, buff=0)
			labelDir = DOWN
		elif layout == self.VERTICAL:
			self.blocks.arrange(UP, buff=0)
			labelDir = RIGHT
		
		self.add(self.blocks)

		startLabel = startAddr.next_to(self.blocks[0], labelDir, buff=0.1)
		self.add(startLabel)

		endLabel = endAddr.next_to(self.blocks[-1], labelDir, buff=0.1)
		self.add(endLabel)

	def transpose(self):
		if self.layout == self.HORIZONTAL: 
			self.layout = self.VERTICAL
			dir = UP
		else: 
			self.layout = self.HORIZONTAL
			dir = RIGHT
		
		animations:list[VGroup|Hexadecimal] = []

		animations.append(self.blocks.animate.arrange(dir, buff=0))

		# startLabel:Hexadecimal = self.submobjects[1]
		# endLabel:Hexadecimal = self.submobjects[2]

		# animations.append(startLabel.animate.next_to(self.blocks[0], RIGHT, buff=0.1))
		# animations.append(self.submobjects[2].animate.next_to(self.blocks[-1], RIGHT, buff=0.1))

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

		for block, data in zip(self.blocks, self.data):
			if data is not None:
				animations.append(data.animate.move_to(block.get_center()))
		
		return AnimationGroup(*animations)

	def setByte(self, index:int, data:Hexadecimal) -> Hexadecimal:
		self.add(data)
		self.data[index] = data

		return data.animate.move_to(self.blocks[index].get_center())

	def clearByte(self, index:int):

		pass

	def highlightByte(self, index:int, color:str):
		return self.blocks[index].animate.set_color(color)
	
	def dehighlightByte(self, index:int):
		return self.blocks[index].animate.set_color("#ffffff")
	


