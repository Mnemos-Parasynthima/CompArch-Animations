from manim import VGroup, Rectangle, Text, Arrow, RIGHT, DOWN, UP, LEFT, RED, GREEN, BLACK
from manim import RoundedRectangle

from ..hexdec import Hexadecimal, CodeBlock


class RegFile(VGroup):
	def __init__(self, regfileHeight:float=2.5, regfileWidth:float=1.8):
		super().__init__()

		self.regfile = Rectangle(height=regfileHeight, width=regfileWidth)
		self.regfileLabel = Text("Register\nFile", font_size=28).move_to(self.regfile.get_center())
		regfileGroup = VGroup(self.regfile, self.regfileLabel)

		self.wEnableArrow = Arrow(
			max_tip_length_to_length_ratio=0.1, color=RED
		).put_start_and_end_on(start=self.regfile.get_top()+UP*0.5, end=self.regfile.get_top())
		self.wEnableLabel = CodeBlock("w_enable", fontSize=30).next_to(self.wEnableArrow, RIGHT, buff=0.1)
		wEnableGroup = VGroup(self.wEnableArrow, self.wEnableLabel)

		self.valAArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.regfile.get_right()+(DOWN*0.15), end=self.regfile.get_right()+(RIGHT*0.8)+(DOWN*0.15))
		self.valALabel = CodeBlock("val_a", fontSize=26).next_to(self.valAArrow, UP, buff=0.1)
		self.valAText = None
		self.valA = -1
		valAGroup = VGroup(self.valAArrow, self.valALabel)

		self.valBArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.regfile.get_right()+(DOWN*0.8), end=self.regfile.get_right()+(RIGHT*0.8)+(DOWN*0.8))
		self.valBLabel = CodeBlock("val_b", fontSize=26).next_to(self.valBArrow, DOWN, buff=0.1)
		self.valBText = None
		self.valB = -1
		valBGroup = VGroup(self.valBArrow, self.valBLabel)

		labelTextArrowBuff = 0.02

		self.valWArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.regfile.get_left()+(LEFT*0.8)+(UP), end=self.regfile.get_left()+(UP))
		self.valWLabel = CodeBlock("val_w", fontSize=26).next_to(self.valWArrow, UP, buff=labelTextArrowBuff)
		self.valWText = None
		self.valw = -1
		valWGroup = VGroup(self.valWArrow, self.valWLabel)

		self.dstArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.regfile.get_left()+(LEFT*0.8)+(UP*0.33), end=self.regfile.get_left()+(UP*0.33))
		self.dstLabel = CodeBlock("dst", fontSize=26).next_to(self.dstArrow, UP, buff=labelTextArrowBuff)
		self.dstText = None
		self.dst = -1
		dstGroup = VGroup(self.dstArrow, self.dstLabel)

		self.src1Arrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.regfile.get_left()+(LEFT*0.8)+(DOWN*0.33), end=self.regfile.get_left()+(DOWN*0.33))
		self.src1Label = CodeBlock("src1", fontSize=26).next_to(self.src1Arrow, UP, buff=labelTextArrowBuff)
		self.src1Text = None
		self.src1 = -1
		src1Group = VGroup(self.src1Arrow, self.src1Label)

		self.src2Arrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.regfile.get_left()+(LEFT*0.8)+(DOWN), end=self.regfile.get_left()+(DOWN))
		self.src2Label = CodeBlock("src2", fontSize=26).next_to(self.src2Arrow, UP, buff=labelTextArrowBuff)
		self.src2Text = None
		self.src2 = -1
		src2Group = VGroup(self.src2Arrow, self.src2Label)


		self.add(*regfileGroup, *wEnableGroup, *valAGroup, *valBGroup, *valWGroup, *dstGroup, *src1Group, *src2Group)

	def writeEnable(self, enable:bool=True) -> Arrow:
		if enable: color = GREEN
		else: color = RED

		return self.wEnableArrow.animate.set_color(color)
	
	def setValA(self, valA:Hexadecimal) -> Hexadecimal:
		self.valA = valA.numval
		self.valAText = valA.next_to(self.valAArrow, DOWN, buff=-0.01)
		self.valAText.submobjects[0].font_size = self.valALabel.submobjects[0].font_size

		return self.valAText
	
	def setValB(self, valB:Hexadecimal) -> Hexadecimal:
		self.valB = valB.numval
		self.valBText = valB.next_to(self.valBArrow, UP, buff=-0.01)
		self.valBText.submobjects[0].font_size = self.valBLabel.submobjects[0].font_size

		return self.valBText
	
	def setValW(self, valW:Hexadecimal) -> Hexadecimal:
		self.valW = valW.numval
		self.valWText = valW.next_to(self.valWArrow, DOWN, buff=-0.01)
		self.valWText.submobjects[0].font_size = self.valWLabel.submobjects[0].font_size

		return self.valWText
	
	def setDst(self, dst:Hexadecimal) -> Hexadecimal:
		self.dst = dst.numval
		self.dstText = dst.next_to(self.dstArrow, DOWN, buff=-0.05)
		self.dstText.submobjects[0].font_size = self.dstLabel.submobjects[0].font_size

		return self.dstText
	
	def setSrc1(self, src1:Hexadecimal) -> Hexadecimal:
		self.src1 = src1.numval
		self.src1Text = src1.next_to(self.src1Arrow, DOWN, buff=-0.05)
		self.src1Text.submobjects[0].font_size = self.src1Label.submobjects[0].font_size

		return self.src1Text
	
	def setSrc2(self, src2:Hexadecimal) -> Hexadecimal:
		self.src2 = src2.numval
		self.src2Text = src2.next_to(self.src2Arrow, DOWN, buff=-0.05)
		self.src2Text.submobjects[0].font_size = self.src2Label.submobjects[0].font_size

		return self.src2Text
	
class RegistersState(VGroup):
	def __init__(self, gprs:list[int], sp:int, pc:int, nzcv:int):
		super().__init__()

		stage = RoundedRectangle(width=6.2, height=7, fill_color=BLACK, color=RED, fill_opacity=1)
		self.add(stage)
		
		gprLabels = [f"X{i}" for i in range(31)]

		gprPos:list[list[float]] = []
		for i in range(15): gprPos.append([-1.2, 3 - i * 0.35, 0])
		for i in range(16): gprPos.append([1.8, 3 - i * 0.35, 0])

		for label, pos, val in zip(gprLabels, gprPos, gprs):
			label = CodeBlock(label, fontSize=24).move_to([pos[0] - 1.28, pos[1], 0])
			rect = Rectangle(width=2, height=0.3).move_to(pos)
			text = Hexadecimal(hex(val), fontSize=20).move_to(pos)
			self.add(label, rect, text)

		pos = [[-1.2, -2.65, 0], [1.8, -2.65, 0], [0, -3.2, 0]]

		pcLabel = CodeBlock("PC", fontSize=24).move_to([pos[0][0]-1.28, pos[0][1], 0])
		pcRect = Rectangle(width=2, height=0.3).move_to(pos[0])
		pcText = Hexadecimal(hex(pc), fontSize=24).move_to(pos[0])
		self.add(pcLabel, pcRect, pcText)

		spLabel = CodeBlock("SP", fontSize=24).move_to([pos[1][0]-1.28, pos[1][1], 0])
		spRect = Rectangle(width=2, height=0.3).move_to(pos[1])
		spText = Hexadecimal(hex(sp), fontSize=24).move_to(pos[1])
		self.add(spLabel, spRect, spText)

		nzcvLabel = CodeBlock("NZCV", fontSize=24).move_to([pos[2][0]-0.9, pos[2][1], 0])
		nzcvRect = Rectangle(width=1, height=0.3).move_to(pos[2])
		nzcvText = Hexadecimal(format(nzcv, '04b'), fontSize=24).move_to(pos[2])
		self.add(nzcvLabel, nzcvRect, nzcvText)