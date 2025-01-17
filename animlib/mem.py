from manim import VGroup, Square, RIGHT, DOWN
from .hexdec import Hexadecimal

class MemoryBlock(VGroup):
	HORIZONTAL = 0
	VERTICAL = 1

	def __init__(self, numBlocks=2, layout=HORIZONTAL, startAddr=Hexadecimal("0x0"), endAddr=Hexadecimal("0x1"), **kwargs):
		super().__init__(**kwargs)

		self.blocks = VGroup(*[Square(side_length=1) for _ in range(numBlocks)])

		if layout == self.HORIZONTAL:
			self.blocks.arrange(RIGHT, buff=0)
		elif layout == self.VERTICAL:
			self.blocks.arrange(DOWN, buff=0)
		
		self.add(self.blocks)

		startLabel = startAddr.next_to(self.blocks[0], DOWN, buff=0.1)
		self.add(startLabel)

		endLabel = endAddr.next_to(self.blocks[-1], DOWN, buff=0.1)
		self.add(endLabel)

	def transpose(self):
		'''
		Transposes the memory block. If it is horizontal, it flips to vertical and vice versa.
		'''
		pass

	def setByte(self, index:int, data:Hexadecimal) -> Hexadecimal:
		self.add(data)
		return data.animate.move_to(self.blocks[index].get_center())

	def clearByte(self, index:int):

		pass

	def highlightByte(self, index:int, color:str):
		return self.blocks[index].animate.set_color(color)
	
	


