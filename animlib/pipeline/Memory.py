from manim import VGroup, UP, Rectangle, DL, RIGHT
from .core import Stage, Register
from .DMem import DMem
from ..hexdec import CodeBlock


class MemoryStage(Stage): 
	def __init__(self):
		super().__init__(4.5, 4)

		self.dmem = DMem().shift(UP*0.5)

		self.add(self.dmem)


class MemoryPipeline(Register):
	def __init__(self):
		super().__init__(Register.MEMORY)

		for i in range(4, len(self.components)):
			if i in (4, 7, 8, 11, 12):
				self.components[i] = None
				self.componentsText[i] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

class MemoryElements(Stage):
	def __init__(self):
		super().__init__(10, 3)

		stageLabel = CodeBlock("memory_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.3)
		self.add(stageLabel)

		self.dmem = Rectangle(width=2, height=1.5).shift(RIGHT*3.3 + UP*0.5)
		self.dmemLabel = CodeBlock("dmem", fontSize=38).move_to(self.dmem.get_center())

		self.add(self.dmem, self.dmemLabel)