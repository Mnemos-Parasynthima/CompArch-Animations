from manim import VGroup, Rectangle, Text, Arrow, RIGHT, DOWN, LEFT, UP

from ..hexdec import Hexadecimal, CodeBlock


class PC(VGroup):
	def __init__(self, pcWidth:float=1, pcHeight:float=3):
		super().__init__()

		self.pc = Rectangle(height=pcHeight, width=pcWidth)
		self.pcLabel = Text("PC").move_to(self.pc.get_center())

		pcGroup = VGroup(self.pc, self.pcLabel)

		self.currPCArrow = Arrow(max_tip_length_to_length_ratio=0.15).put_start_and_end_on(start=self.pc.get_right(), end=self.pc.get_right() + RIGHT)
		self.currPCLabel = CodeBlock("current_PC", fontSize=26).next_to(self.currPCArrow, DOWN, buff=0.05).shift(RIGHT*0.3)
		self.currPC = -1
		self.currPCText:Hexadecimal = None

		currPCGroup = VGroup(self.currPCArrow, self.currPCLabel)

		self.nextPCArrow = Arrow(max_tip_length_to_length_ratio=0.15).put_start_and_end_on(start=self.pc.get_left()+LEFT, end=self.pc.get_left())
		self.nextPCLabel = CodeBlock("next_PC", fontSize=26).next_to(self.nextPCArrow, DOWN, buff=0.05).shift(LEFT*0.1)
		self.nextPC = -1
		self.nextPCText:Hexadecimal = None

		nextPCGroup = VGroup(self.nextPCArrow, self.nextPCLabel)

		self.add(*pcGroup, *currPCGroup,*nextPCGroup)

	def setNextPC(self, pc:Hexadecimal) -> Hexadecimal:
		self.nextPC = pc.numval
		self.nextPCText = pc.next_to(self.nextPCArrow, UP, buff=0.05)
		self.nextPCText.submobjects[0].font_size = self.nextPCLabel.submobjects[0].font_size

		return self.nextPCText
	
	def setCurrPC(self, pc:Hexadecimal) -> Hexadecimal:
		self.currPC = pc.numval
		self.currPCText = pc.next_to(self.currPCArrow, UP, buff=0.05)
		self.currPCText.submobjects[0].font_size = self.currPCLabel.submobjects[0].font_size

		return self.currPCText

	def clock(self): pass