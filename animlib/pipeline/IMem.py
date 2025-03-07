from manim import VGroup, Rectangle, Text, Arrow, Tex, MathTex, RIGHT, DOWN, UP, LEFT, Dot, RED, BLUE

from ..hexdec import Hexadecimal


class IMem(VGroup):
	def __init__(self, addr:int, errval:int, rval:int, imemWidth:float=1.5, imemHeight:float=2):
		super().__init__()

		self.imem = Rectangle(height=imemHeight, width=imemWidth)
		self.imemLabel = Text("Instr.\nMem.", font_size=28).move_to(self.imem.get_center())

		imemGroup = VGroup(self.imem, self.imemLabel)

		self.addrArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.imem.get_left()+LEFT, end=self.imem.get_left())
		self.addrLabel = Tex("\\verb|imem_addr|", font_size=26).next_to(self.addrArrow, DOWN, buff=0.1).shift(LEFT*0.2)
		self.addrBits = MathTex("64", font_size=35).next_to(self.addrArrow, UP, buff=0.025)
		self.addr = addr
		self.addrText = Hexadecimal(hex(0), fontSize=40).next_to(self.addrLabel, DOWN, buff=0.1)

		addrGroup = VGroup(self.addrArrow, self.addrLabel, self.addrBits, self.addrText)

		self.errArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.imem.get_right()+(UP*0.5), end=self.imem.get_right()+RIGHT+(UP*0.5))
		self.errLabel = Tex("\\verb|imem_err|", font_size=26).next_to(self.errArrow, UP, buff=0.1).shift(RIGHT*0.1)
		self.err = errval
		self.errText = Hexadecimal(hex(0), fontSize=40).next_to(self.errLabel, UP, buff=0.1)

		errGroup = VGroup(self.errArrow, self.errLabel, self.errText)

		self.rvalArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.imem.get_right()+(DOWN*0.5), end=self.imem.get_right()+RIGHT+(DOWN*0.5))
		self.rvalLabel = Tex("\\verb|imem_rval|", font_size=26).next_to(self.rvalArrow, DOWN, buff=0.1).shift(RIGHT*0.2)
		self.rvalBits = MathTex("32", font_size=35).next_to(self.rvalArrow, UP, buff=0.025)
		self.rval = rval
		self.rvalText = Hexadecimal(hex(0), fontSize=40).next_to(self.rvalLabel, DOWN, buff=0.1)

		rvalGroup = VGroup(self.rvalArrow, self.rvalLabel, self.rvalBits, self.rvalText)

		self.add(*imemGroup, *addrGroup, *errGroup, *rvalGroup)