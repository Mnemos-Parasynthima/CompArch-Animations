from manim import VGroup, RoundedRectangle, UP
from .core import Stage
from .DMem import DMem


class MemoryStage(Stage): 
	def __init__(self):
		super().__init__(4.5, 4)

		self.dmem = DMem().shift(UP*0.5)

		self.add(self.dmem)


class MemoryPipeline(VGroup): pass

class MemoryElements(VGroup): pass