from manim import VGroup, Rectangle, Text, Arrow, RIGHT, DOWN, UP, LEFT

from ..hexdec import Hexadecimal, CodeBlock


class IMem(VGroup):
	def __init__(self, imemWidth:float=1.5, imemHeight:float=2):
		super().__init__()

		self.imem = Rectangle(height=imemHeight, width=imemWidth)
		self.imemLabel = Text("Instr.\nMem.", font_size=28).move_to(self.imem.get_center())

		imemGroup = VGroup(self.imem, self.imemLabel)

		self.addrArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.imem.get_left()+LEFT, end=self.imem.get_left())
		self.addrLabel = CodeBlock("imem_addr", fontSize=26).next_to(self.addrArrow, DOWN, buff=0.1).shift(LEFT*0.2)
		self.addr = -1
		self.addrText:Hexadecimal = None

		addrGroup = VGroup(self.addrArrow, self.addrLabel)

		self.errArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.imem.get_right()+(UP*0.5), end=self.imem.get_right()+RIGHT+(UP*0.5))
		self.errLabel = CodeBlock("imem_err", fontSize=26).next_to(self.errArrow, UP, buff=0.1).shift(RIGHT*0.1)
		self.err = -1
		self.errText:Hexadecimal = None

		errGroup = VGroup(self.errArrow, self.errLabel)

		self.rvalArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.imem.get_right()+(DOWN*0.5), end=self.imem.get_right()+RIGHT+(DOWN*0.5))
		self.rvalLabel = CodeBlock("imem_rval", fontSize=26).next_to(self.rvalArrow, DOWN, buff=0.1).shift(RIGHT*0.2)
		self.rval = -1
		self.rvalText:Hexadecimal = None

		rvalGroup = VGroup(self.rvalArrow, self.rvalLabel)

		self.add(*imemGroup, *addrGroup, *errGroup, *rvalGroup)