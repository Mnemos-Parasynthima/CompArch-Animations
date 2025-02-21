from manim import VGroup, Rectangle, UP, DOWN, LEFT, RIGHT, Polygon, PURPLE


class CPU(VGroup):
	def __init__(self):
		super().__init__()

		container = Rectangle(height=4, width=4)

		regs = VGroup(*[ Rectangle(PURPLE, height=0.3, width=1) for i in range(8) ])
		regs.arrange(DOWN, buff=0.1).move_to(container, RIGHT).shift(LEFT * 0.3)

		pos = [
			[0,0,0], # center in
			[-0.5,-0.5,0], # bottom top	
			[-0.5,-1.5,0], # bottom bottom
			[0.65,-0.5,0], # right bottom
			[0.65,0.5,0], # right top
			[-0.5,1.5,0], # top top
			[-0.5,0.5,0] # top bottom
		]
		alu = Polygon(*pos).shift(LEFT*0.75)

		self.add(regs, container, alu)
		
	def getALU(self) -> Polygon:
		return self.submobjects[2]
	
	def getRegisters(self) -> VGroup:
		return self.submobjects[0]