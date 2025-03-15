from manim import VGroup, Rectangle, Polygon, Text, Arrow, Tex, MathTex, RIGHT, DOWN, UP, LEFT, RED
from ..hexdec import CodeBlock, Hexadecimal
from numpy import linspace

class Mux(VGroup):
	LR = 0 
	'''
	Flow of data is from left (input) to right (output).
	'''

	RL = 1
	'''
	Flow of data is from right (input) to left (output).
	'''

	TOP = 3
	'''
	'''

	BOTTOM = 4
	'''
	'''

	def __init__(self, inputn:int, outputn:int, width:int=1, arrowSpacing:int=0.4, direction=LR):
		super().__init__()

		maxN = max(inputn, outputn)
		height = maxN * arrowSpacing + 0.8

		self.mux = Rectangle(width=width, height=height)
		self.muxLabel = Text(f" {inputn}:{outputn}\nMux", font_size=20).move_to(self.mux.get_center())
		self.signalArrow:Arrow = None
		self.signalLabel:CodeBlock = None
		self.signalText:Hexadecimal = None
		self.signal:int = -1

		inputYPos = linspace(height/2-0.25, -height/2+0.25, inputn) if inputn != 1 else [0]
		outputYPos = linspace(height/2-0.25, -height/2+0.25, outputn) if outputn != 1 else [0]

		if direction == self.LR:
			inputSide, outputSide = self.mux.get_left(), self.mux.get_right()
			inputDir, outputDir = LEFT*0.8, RIGHT*0.8
		else:
			inputSide, outputSide = self.mux.get_right(), self.mux.get_left()
			inputDir, outputDir = RIGHT*0.8, LEFT*0.8

		self.inputArrows = [
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=inputSide+(UP*y)+inputDir, end=inputSide+(UP*y))
			for y in inputYPos
		]
		self.inputText:list[Hexadecimal] = [ None for _ in range(inputn) ]
		self.inputVal:list[int] = [ -1 for _ in range(inputn) ]

		self.outputArrows = [
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=outputSide+(UP*y), end=outputSide+(UP*y)+outputDir)
			for y in outputYPos
		]
		self.outputText:list[Hexadecimal] = [ None for _ in range(outputn) ]
		self.outputVal:list[int] = [ -1 for _ in range(outputn) ]

		self.add(self.mux, self.muxLabel, *self.inputArrows, *self.outputArrows)

	def addSignal(self, label:CodeBlock, side:int, text:Hexadecimal=None):
		if side == self.TOP:
			base = self.mux.get_top()
			baseDir = UP*0.5
			labelDir = UP
		else:
			base = self.mux.get_bottom()
			baseDir = DOWN*0.5
			labelDir = DOWN

		self.signalArrow = Arrow(
			max_tip_length_to_length_ratio=0.1, color=RED
		).put_start_and_end_on(start=base+baseDir, end=base)
		self.signalLabel = label.next_to(self.signalArrow, labelDir, buff=0.1)
		self.signalText = text

		self.add(self.signalArrow, self.signalLabel)
		if text:
			self.add(self.signalText)

	def setArrowInfoList(self, inputInfo:list[Hexadecimal], outputInfo:list[Hexadecimal]) -> list[Hexadecimal]:
		assert(self.signalLabel)
		assert(len(inputInfo) != 0 or len(outputInfo) != 0)

		anims:list[Hexadecimal] = []

		for i, _in in enumerate(inputInfo):
			self.inputVal[i] = _in.numval
			self.inputText[i] = _in.next_to(self.inputArrows[i], UP, buff=0.005)
			self.inputText[i].submobjects[0].font_size = self.signalLabel.submobjects[0].font_size

			anims.append(self.inputText[i])

		for i, _out in enumerate(outputInfo):
			self.outputVal[i] = _out.numval
			self.outputText[i] = _out.next_to(self.outputArrows[i], UP, buff=0.005)
			self.outputText[i].submobjects[0].font_size = self.signalLabel.submobjects[0].font_size

			anims.append(self.outputText[i])

		return anims

	def setArrowInfo(self, info:Hexadecimal, index:int, forInput:bool=True) -> Hexadecimal:
		assert(self.signalLabel)

		if forInput:
			self.inputVal[index] = info.numval
			self.inputText[index] = info.next_to(self.inputArrows[index], UP, buff=0.005)
			self.inputText[index].submobjects[0].font_size = self.signalLabel.submobjects[0].font_size

			return self.inputText[index]
		
		self.outputVal[index] = info.numval
		self.outputText[index] = info.next_to(self.outputArrows[index], UP, buff=0.005)
		self.outputText[index].submobjects[0].font_size = self.signalLabel.submobjects[0].font_size

		return self.outputText[index]


class Adder(VGroup):
	def __init__(self, bText:CodeBlock, b:int=-1):
		super().__init__()

		self.adder = Polygon(*[
			[-1,0,0], # bottom left
			[1,0,0], # bottom right
			[0.7,1,0], # top right
			[-0.7,1,0] # top left
		])
		self.adderLabel = Text("64-bit Adder", font_size=17.3).move_to(self.adder.get_center())

		self.aArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.adder.get_bottom()+(DOWN*0.8)+(LEFT*0.6), end=self.adder.get_bottom()+(LEFT*0.6))
		self.aText:Hexadecimal = None
		self.a = -1

		self.bArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.adder.get_bottom()+(DOWN*0.8)+(RIGHT*0.6), end=self.adder.get_bottom()+(RIGHT*0.6))
		self.bText = bText.next_to(self.bArrow, RIGHT, buff=0.2)
		self.b = b

		self.cArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.adder.get_top(), end=self.adder.get_top()+(UP*0.8))
		self.cText:Hexadecimal = None
		self.c = -1

		self.add(self.adder, self.adderLabel, self.aArrow, self.bArrow, self.bText, self.cArrow)

	def setA(self, a:Hexadecimal) -> Hexadecimal:
		self.a = a.numval
		self.aText = a.next_to(self.aArrow, LEFT, buff=-0.3).shift(DOWN*0.08)
		self.aText.submobjects[0].font_size = self.bText.submobjects[0].font_size
		# print("Font size of b text for a", self.bText.submobjects[0].font_size)

		return self.aText
	
	def setC(self, c:Hexadecimal) -> Hexadecimal:
		self.c = c.numval
		self.cText = c.next_to(self.cArrow, LEFT, buff=-0.3)
		self.cText.submobjects[0].font_size = self.bText.submobjects[0].font_size
		# print("Font size of b text for c", self.bText.submobjects[0].font_size)

		return self.cText