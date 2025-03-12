from manim import VGroup, Rectangle, Text, Arrow,  MathTex, RIGHT, DOWN, UP, LEFT, Dot, RED, BLUE

from ..hexdec import Hexadecimal, CodeBlock


class DMem(VGroup):
	def __init__(self, addr:int, wval:int, errval:int, rval:int, dmemWidth:float=1.5, dmemHeight:float=2.5):
		super().__init__()

		self.dmem = Rectangle(height=dmemHeight, width=dmemWidth)
		self.dmemLabel = Text("Data\nMem.", font_size=28).move_to(self.dmem.get_center())

		dmemGroup = VGroup(self.dmem, self.dmemLabel)

		self.addrArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.dmem.get_left()+LEFT+(DOWN*0.5), end=self.dmem.get_left()+(DOWN*0.5))
		self.addrLabel = CodeBlock("dmem_addr", fontSize=26).next_to(self.addrArrow, UP, buff=0.1).shift(LEFT*0.2)
		self.addr = addr
		self.addrText = Hexadecimal(hex(0xfffe), fontSize=26).next_to(self.addrArrow, DOWN, buff=0.1)
		addrGroup = VGroup(self.addrArrow, self.addrLabel, self.addrText)

		self.wvalArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.dmem.get_left()+LEFT+(UP*0.5), end=self.dmem.get_left()+(UP*0.5))
		self.wvalLabel = CodeBlock("dmem_wval", fontSize=26).next_to(self.wvalArrow, UP, buff=0.1).shift(LEFT*0.2)
		self.wval = wval
		self.wvalText = Hexadecimal("d3", fontSize=26).next_to(self.wvalArrow, DOWN, buff=0.1)
		wvalGroup = VGroup(self.wvalArrow, self.wvalLabel, self.wvalText)

		self.errArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.dmem.get_right()+(UP*0.95), end=self.dmem.get_right()+RIGHT+(UP*0.95))
		self.errLabel = CodeBlock("dmem_err", fontSize=26).next_to(self.errArrow, UP, buff=0.05).shift(RIGHT*0.1)
		self.err = errval
		self.errText = Hexadecimal("01", fontSize=26).next_to(self.errArrow, DOWN, buff=0.05)
		errGroup = VGroup(self.errArrow, self.errLabel, self.errText)

		self.rvalArrow = Arrow(
			max_tip_length_to_length_ratio=0.15
		).put_start_and_end_on(start=self.dmem.get_right()+(UP*0.2), end=self.dmem.get_right()+RIGHT+(UP*0.2))
		self.rvalLabel = CodeBlock("dmem_rval", fontSize=26).next_to(self.rvalArrow, UP, buff=0.05).shift(RIGHT*0.2)
		self.rval = rval
		self.rvalText = Hexadecimal("3e", fontSize=26).next_to(self.rvalArrow, DOWN, buff=0.05)
		rvalGroup = VGroup(self.rvalArrow, self.rvalLabel, self.rvalText)

		self.readArrow = Arrow(
			max_tip_length_to_length_ratio=0.13, color=RED
		).put_start_and_end_on(start=self.dmem.get_bottom()+(DOWN*0.8)+(LEFT*0.6), end=self.dmem.get_bottom()+(LEFT*0.6))
		self.readLabel = CodeBlock("dmem_read", fontSize=20).next_to(self.readArrow, DOWN, buff=0.1)
		readGroup = VGroup(self.readArrow, self.readLabel)

		self.writeArrow = Arrow(
			max_tip_length_to_length_ratio=0.13, color=RED
		).put_start_and_end_on(start=self.dmem.get_bottom()+(DOWN*0.8)+(RIGHT*0.6), end=self.dmem.get_bottom()+(RIGHT*0.6))
		self.writeLabel = CodeBlock("dmem_write", fontSize=20).next_to(self.writeArrow, DOWN, buff=0.1)
		writeGroup = VGroup(self.writeArrow, self.writeLabel)

		self.add(*dmemGroup, *wvalGroup, *addrGroup, *errGroup, *rvalGroup, *readGroup, *writeGroup)