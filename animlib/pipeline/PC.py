from manim import VGroup, Rectangle, Text, Arrow, Tex, MathTex, RIGHT, DOWN, UP, LEFT

from ..hexdec import Hexadecimal


class PC(VGroup):
	def __init__(self, pcWidth:float, pcHeight:float, currPC:int, nextPC:int):
		super().__init__()

		self.pc = Rectangle(height=3, width=1)
		self.pcLabel = Text("PC").move_to(self.pc.get_center())

		pcGroup = VGroup(self.pc, self.pcLabel)

		self.currPCArrow = Arrow(max_tip_length_to_length_ratio=0.15).put_start_and_end_on(start=self.pc.get_right(), end=self.pc.get_right() + RIGHT)
		self.currPCLabel = Tex("\\verb|current_PC|", font_size=26).next_to(self.currPCArrow, DOWN).shift(RIGHT*0.3)
		self.currPCBits = MathTex("64", font_size=35).next_to(self.currPCArrow, UP)
		self.currPC = currPC
		self.currPCText = Hexadecimal(hex(currPC), fontSize=40).next_to(self.currPCLabel, DOWN)

		currPCGroup = VGroup(self.currPCArrow, self.currPCLabel, self.currPCBits, self.currPCText)

		self.nextPCArrow = Arrow(max_tip_length_to_length_ratio=0.15).put_start_and_end_on(start=self.pc.get_left()+LEFT, end=self.pc.get_left())
		self.nextPCLabel = Tex("\\verb|next_PC|", font_size=26).next_to(self.nextPCArrow, DOWN).shift(LEFT*0.1)
		self.nextPCBits = MathTex("64", font_size=35).next_to(self.nextPCArrow, UP)
		self.nextPC = nextPC
		self.nextPCText = Hexadecimal(hex(nextPC), fontSize=40).next_to(self.nextPCLabel, DOWN)

		nextPCGroup = VGroup(self.nextPCArrow, self.nextPCLabel, self.nextPCBits, self.nextPCText)

		self.add(*pcGroup, *currPCGroup,*nextPCGroup)

	def clock(self): pass