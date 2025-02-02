from manim import VGroup, TAU, AnnularSector, RED, PI, BLACK, WHITE, VMobject, ManimColor, Text, AnimationGroup
from numpy import cos, sin

class NumberWheel(VGroup):
	def __init__(self, bitn:int, color0:str = BLACK, color1:str = WHITE, signed:bool = False, **kwargs):
		super().__init__(**kwargs)

		self.size = bitn
		self.color0 = color0
		self.color1 = color1
		self.signed = signed

		self.totalSlices:int = 2 ** bitn # How many numbers does this number wheel represent (2^n)
		self.totalSectors = 0 # How many total sectors (indiv bit) are there in the wheel (nums * n)

		for bit in range(bitn):
			innerRad = bit / bitn
			outerRad = (bit + 1) / bitn
			subSectors = 2 ** (bit + 1)

			for i in range(subSectors):
				startAngle = (i * TAU / subSectors) + (PI / 2)
				endAngle = ((i + 1) * TAU / subSectors) + (PI / 2)
				color = color1 if (i % 2 == 0) else color0

				sector = AnnularSector(
					innerRad, outerRad,
					(endAngle - startAngle), startAngle, 
					1, 1, color, stroke_color=RED
				)
				
				self.add(sector)

		# self.submobjects[] has only the added sectors
		self.totalSectors = len(self.submobjects)
		
		self.scale(2)

		# wrap around
		for i in range(self.totalSlices):
			angle = -(((i + 0.5) * (TAU / self.totalSlices)) - (PI / 2))
			rad = 1.1 * 2
			label = i if not signed else self._toSigned(i, bitn)
			text = Text(str(label), font_size=14).move_to(
				[rad * cos(angle), rad * sin(angle), 0]
			)
			self.add(text)

	def getNumber(self, index:int) -> VMobject:
		actualIndex = self.totalSectors + (index % 2**self.size)
		return self.submobjects[actualIndex]

	def highlightSector(self, index:int, color:ManimColor) -> VMobject:
		return self.submobjects[index].animate.set_color(color)
	
	def highlightNumber(self, index:int, color:ManimColor) -> VMobject:
		# The given index is the index based off on totalSlices
		# That is, index 0 means slice 0, which has number 0
		# Index 1, slice 1, number 1, etc
		# But to index on submobject (contains all mobj), must map it to use the index
		# based off on submobjects[]
		# That is, index 0 -> index right after last sector (totalSectors)
		# Index 1 -> index two after last sector (totalSectors+1)
		# HOWEVER, there is a chance the given index is past the "appropriate" values in the wheel
		# That is, overflow
		# To map to the proper index, do index mod 2^n
		actualIndex = self.totalSectors + (index % 2**self.size)
		return self.submobjects[actualIndex].animate.set_color(color).scale(2)
	
	def dehighlightSector(self, index:int) -> VMobject:
		color = self.color0 if (index % 2 == 0) else self.color1
		return self.submobjects[index].animate.set_color(color)
	
	def dehighlightNumber(self, index:int) -> VMobject:
		actualIndex = self.totalSectors + (index % 2**self.size)
		return self.submobjects[actualIndex].animate.set_color(WHITE).scale(0.5)

	def flipSignedness(self) -> AnimationGroup:
		self.signed = not self.signed

		animations:list[Text] = []

		for i, text in enumerate(self.submobjects[len(self.submobjects)-self.totalSlices:]):
			label = i if not self.signed else self._toSigned(i, self.size)
			animations.append(text.animate.become(Text(str(label), font_size=14).move_to(text.get_center())))

		return AnimationGroup(*animations)

	def _toSigned(self, val:int, bitn:int) -> int:
		if val >= 2 ** (bitn - 1): return val - 2 ** bitn

		return val