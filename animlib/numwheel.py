from manim import VGroup, TAU, AnnularSector, RED, PI, BLACK, WHITE, VMobject, ManimColor, Text
from numpy import cos, sin

class NumberWheel(VGroup):
	def __init__(self, bitn:int, color0:str = BLACK, color1:str = WHITE, signed:bool = False, **kwargs):
		super().__init__(**kwargs)

		self.size = bitn
		self.color0 = color0
		self.color1 = color1
		self.signed = signed

		totalSlices:int = 2 ** bitn # How many numbers does this number wheel represent (2^n)
		totalSectors:int = totalSlices * bitn # How many total sectors (indiv bit) are there in the wheel (nums * n)

		self.totalSlices = totalSlices
		self.totalSectors = totalSectors


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

		for i in range(totalSlices):
			angle = -(((i + 0.5) * (TAU / totalSlices)) - (PI / 2))
			rad = 1.2
			label = i if not signed else self._toSigned(i, bitn)
			text = Text(str(label), font_size=14).move_to(
				[rad * cos(angle), rad * sin(angle), 0]
			)
			self.add(text)

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
		actualIndex = self.totalSectors + index
		return self.submobjects[actualIndex].animate.set_color(color)
	
	def dehighlightSector(self, index:int) -> VMobject:
		color = self.color0 if (index % 2 == 0) else self.color1
		return self.submobjects[index].animate.set_color(color)
	
	def dehighlightNumber(self, index:int) -> VMobject:
		actualIndex = self.totalSectors + index
		return self.submobjects[actualIndex].animate.set_color(WHITE)

	def flipSignedness(self):
		self.signed = not self.signed

		for i, text in enumerate(self.submobjects[len(self.submobjects)-self.totalSlices:]):
			label = i if not self.signed else self._toSigned(i, self.size)
			text.become(Text(str(label), font_size=14).move_to(text.get_center()))

	def _toSigned(self, val:int, bitn:int) -> int:
		if val >= 2 ** (bitn - 1): return val - 2 ** bitn

		return val