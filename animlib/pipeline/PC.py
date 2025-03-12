from manim import VGroup, Rectangle, Text, Arrow, RIGHT, DOWN, LEFT

from ..hexdec import Hexadecimal, CodeBlock


class PC(VGroup):
	def __init__(self, pcWidth:float=1, pcHeight:float=3):
		super().__init__()

		self.pc = Rectangle(height=pcHeight, width=pcWidth)
		self.pcLabel = Text("PC").move_to(self.pc.get_center())

		pcGroup = VGroup(self.pc, self.pcLabel)

		self.currPCArrow = Arrow(max_tip_length_to_length_ratio=0.15).put_start_and_end_on(start=self.pc.get_right(), end=self.pc.get_right() + RIGHT)
		self.currPCLabel = CodeBlock("current_PC", fontSize=26).next_to(self.currPCArrow, DOWN).shift(RIGHT*0.3)
		self.currPC = -1
		self.currPCText:Hexadecimal = None

		currPCGroup = VGroup(self.currPCArrow, self.currPCLabel)

		self.nextPCArrow = Arrow(max_tip_length_to_length_ratio=0.15).put_start_and_end_on(start=self.pc.get_left()+LEFT, end=self.pc.get_left())
		self.nextPCLabel = CodeBlock("next_PC", fontSize=26).next_to(self.nextPCArrow, DOWN).shift(LEFT*0.1)
		self.nextPC = -1
		self.nextPCText:Hexadecimal = None

		nextPCGroup = VGroup(self.nextPCArrow, self.nextPCLabel)

		self.add(*pcGroup, *currPCGroup,*nextPCGroup)

	def clock(self): pass