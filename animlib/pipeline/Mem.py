from manim import VGroup, RoundedRectangle, UP
from .DMem import DMem


class MemoryStage(VGroup): 
	def __init__(self):
		super().__init__()

		stage = RoundedRectangle(corner_radius=0.5, width=4.5, height=4)
		self.dmem = DMem().shift(UP*0.5)

		self.add(stage, self.dmem)



class MemoryPipeline(VGroup): pass

class MemoryElements(VGroup): pass