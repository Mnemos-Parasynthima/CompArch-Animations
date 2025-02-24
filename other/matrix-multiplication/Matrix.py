from manim import VGroup, Rectangle, RIGHT, DOWN, ManimColor, Tex, LEFT, UP, BLACK, YELLOW, AnimationGroup, WHITE

class Matrix(VGroup):
	COLUMN = 0
	ROW = 1

	def __init__(self, m:int, n:int, mstep:str, nstep:str, ms:float, ns:float, color:ManimColor=WHITE):
		'''
		Parameters
		----------
		m 
			m dimension to be used in generating the proper amount of rectangles.
		n
			n dimension to be used in generating the proper amount of rectangles.
		mstep
			m dimension of the problem (not used in object generation).
		nstep
			n dimension of the problem (not used in object generation).
		ms
			How much should each rectangle in the m dimension be. m * ms = total height
		ns
			How much should each rectangle in the n dimension be. n * ns = total width
		color
			Color of the matrix.
		'''
		super().__init__()

		self.m = mstep
		self.n = nstep
		self.mLabel = None
		self.nLabel = None
		self.color = color

		elems:list[Rectangle] = []

		if m == 1:
			orientation = RIGHT
		elif n == 1:
			orientation = DOWN

		for i in range(m):
			for j in range(n):
				elems.append(Rectangle(color, ms, ns))

		self.add(*elems)
		self.arrange(orientation, buff=0.01)
	
	def showLabel(self, dim:int) -> Tex:
		if dim == self.COLUMN:
			label = Tex(f"${self.m}$")
			label.next_to(self, LEFT)
			self.mLabel = label
			return self.mLabel
		elif dim == self.ROW:
			label = Tex(f"${self.n}$")
			label.next_to(self, UP)
			self.nLabel = label
			return self.nLabel

	def showLabels(self) -> tuple[Tex, Tex]:
		return self.showLabel(self.COLUMN), self.showLabel(self.ROW)

	def hideLabel(self, dim:int) -> Tex:
		if dim == self.COLUMN:
			return self.mLabel.animate.fade(1)
		elif dim == self.ROW:
			return self.nLabel.animate.fade(1)
		
	def hideLabels(self) -> AnimationGroup:
		return AnimationGroup(self.hideLabel(self.COLUMN).build(), self.hideLabel(self.ROW).build())

	def getVector(self, index:int) -> Rectangle:
		return self.submobjects[index]

	def highlightRowCol(self, index:int) -> Rectangle:
		return self.getVector(index).animate.set_fill(YELLOW, 1)
	
	def dehighlightRowCol(self, index:int) -> Rectangle:
		return self.getVector(index).animate.set_fill(BLACK, 1)