from manim import VGroup, MathTex, RIGHT, DOWN, UP, BLACK, WHITE, Square, AnimationGroup, Transform, FadeOut, PI, AnnularSector, RED, TAU
from numpy import array as nparray
from .hexdec import Hexadecimal
from .funcs import inttstr, splithex

class Vector(VGroup):
	def __init__(self, size:int, vec:list[int], **kwargs):
		super().__init__(**kwargs)
		self.size = size
		self.vector = vec
		self.elems:list[MathTex|Hexadecimal] = None
		self.bvec:VGroup = None
		self.commas:list[MathTex] = None

		# Adding references to the brackets and the vgroup is to help refer to them later on and not lose
		# them in the list of submobjs where the type cannot be differentiated (maybe?)
		self.openBracket = MathTex("[")
		self.closeBracket = MathTex("]")

	def __end_init__(self):
		self.bvec = VGroup(self.openBracket, *self._combineElems(), self.closeBracket)
		self.bvec.arrange(RIGHT, buff=0.1)

		for comma in self.commas:
			comma.shift(DOWN * 0.2)

		self.add(self.bvec)

	def _combineElems(self) -> list[MathTex|Hexadecimal]:
		self.commas = [MathTex(",") for _ in range(self.size - 1)]

		res:list[MathTex|Hexadecimal] = []
		for i, elem in enumerate(self.elems):
			res.append(elem)
			if i < len(self.commas): res.append(self.commas[i])

		return res

class Bytesvector(Vector):
	def __init__(self, size:int = 4, vec:list[int]=[0,0,0,0], **kwargs):
		super().__init__(size, vec, **kwargs)

		self.elems:list[Hexadecimal] = []

		hexstrs:list[str] = [inttstr(val) for val in vec]
		
		for hexstr in hexstrs:
			elem = Hexadecimal(hexstr)

			self.elems.append(elem)


		super().__end_init__()

class Bitvector(Vector):
	def __init__(self, size:int = 4, vec:list[int]=[0,0,0,0], placeholder:bool=True, **kwargs):
		super().__init__(size, vec, **kwargs)
		
		self.usesPlaceholder = placeholder
		self.elems:list[MathTex|Square] = []
		self.labels:list[MathTex] = [] # The labels to be shown above each bit in the form of 2^i
		self.labelsNum:list[MathTex] = [] # The labels to be transformed to from 2^i to its actual number

		for i in range(size):
			if placeholder:
				elem = MathTex(f"b_{{{size - 1 - i}}}")
			else:
				elem = MathTex(str(vec[i]))

			self.elems.append(elem)
			self.labels.append(MathTex(f"2^{{{size - 1 - i}}}").scale(0.55))
			self.labelsNum.append(MathTex(f"{{{2 ** (size-1-i)}}}").scale(0.55))

		super().__end_init__()

	def showLabels(self) -> AnimationGroup:
		animations:list[MathTex] = []

		for i, elem in enumerate(self.elems):
			animations.append(self.labels[i].move_to(elem.get_top() + [0, 0.15, 0]).animate.next_to(elem, UP, buff=0.1))

		# self.add(VGroup(*self.labels))

		return AnimationGroup(*animations)
	
	def hideLabels(self) -> AnimationGroup:
		animations:list[MathTex] = []

		for label, labelNum in zip(self.labels, self.labelsNum):
			# animations.append(FadeOut(labelNum))
			animations.append(FadeOut(label))
		# self.remove(self.labels)

		return AnimationGroup(*animations)

	def updateLabels(self) -> AnimationGroup:
		animations:list[MathTex] = []
		
		for label, labelNum in zip(self.labels, self.labelsNum):
			animations.append(Transform(label, labelNum.move_to(label.get_center())))

		return AnimationGroup(*animations)

	def toSquares(self) -> AnimationGroup:
		assert(not self.usesPlaceholder)

		anims:list[Square] = []

		for comma in self.commas:
			anims.append(FadeOut(comma))
			self.bvec.remove(comma)
			
		self.commas.clear()
		self.commas = None

		elemsSquares:list[Square] = []

		for i, elem in enumerate(self.elems):
			color = BLACK if (self.vector[i] == 0) else WHITE
			square = Square(0.35).set_fill(color, 1).set_stroke(WHITE, 0.5).move_to(elem.get_center())

			anims.append(elem.animate.become(square))
			elemsSquares.append(square)
			# print(f"Square {square}@{hex(id(square))}; self.elems[i] {self.elems[i]}@{hex(id(self.elems[i]))}")

		# self.elems = elemsSquares

		return AnimationGroup(*anims), elemsSquares

	def toWedge(self) -> tuple[VGroup, AnimationGroup]:
		# Only for when it is in squares
		assert(not self.commas)

		anims:list[AnnularSector] = []

		wedge = VGroup()
		for i, elem in enumerate(self.elems):
			innerRad = (i / self.size) * 1.75
			outerRad = ((i + 1) / self.size) * 1.75

			startAngle = PI/2.5 # refer to the unit circle 
			angle = TAU/10 # the bigger the denum is (smaller the number), the less "width" it has

			wedgeSector = AnnularSector(
				innerRad, outerRad, 
				angle, startAngle,
				1, 1, elem.get_color(), stroke_color=RED)
			# wedgeSector.move_to(elem.get_center())
			wedgeSector.move_to(elem.get_center() + DOWN * (outerRad + innerRad) / 2)
			anims.append(Transform(elem, wedgeSector, replace_mobject_with_target_in_scene=True))
			wedge += wedgeSector

		return wedge, AnimationGroup(*anims)

	def transpose(self) -> AnimationGroup:
		spacing = self.elems[0].height * 1.2
		startY = self.elems[0].get_center()[1] - (len(self.elems) - 1) * spacing / 2 # Top square y pos
		xPos = self.elems[0].get_center()[0]

		newPositions = [ nparray([xPos, startY + i * spacing, 0]) for i in range(len(self.elems)) ]

		bracketAnim = AnimationGroup(
			self.openBracket.animate.move_to(newPositions[0] + nparray([0, -0.25, 0])).rotate(PI / 2),
			self.closeBracket.animate.move_to(newPositions[-1] + nparray([0, 0.25, 0])).rotate(PI / 2),
		)

		squareAnim = [ elem.animate.move_to(newPos) for elem, newPos in zip(self.elems, newPositions) ]

		return AnimationGroup(bracketAnim, *squareAnim)