from manim import VGroup, RoundedRectangle, UP
from .core import Stage, Register
from .DMem import DMem


class MemoryStage(Stage): 
	def __init__(self):
		super().__init__(4.5, 4)

		self.dmem = DMem().shift(UP*0.5)

		self.add(self.dmem)


class MemoryPipeline(Register):
	def __init__(self):
		super().__init__(Register.MEMORY)

		for i in range(4, len(self.components)):
			if i in (4, 7, 8, 10, 11, 12):
				self.components[i] = None
				self.componentsText[i] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

class MemoryElements(VGroup): pass