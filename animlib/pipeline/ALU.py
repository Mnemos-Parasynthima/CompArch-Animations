from manim import VGroup, Polygon, Text, Arrow, RIGHT, DOWN, UP, LEFT, RED, GREEN
from enum import Enum

from ..hexdec import Hexadecimal, CodeBlock


class ALU_OP(Enum):
	PLUS_OP = "0"
	MINUS_OP = "1"
	INV_OP = "2"
	OR_OP = "3"
	EOR_OP = "4"
	AND_OP = "5"
	MOV_OP = "6"
	LSL_OP = "7"
	LSR_OP = "8"
	ASR_OP = "9"
	PASS_A_OP = "10"
	CSEL_OP = "11"
	CSINV_OP = "12"
	CSINC_OP = "13"
	CSNEG_OP = "14"
	CBZ_OP = "15"
	CBNZ_OP = "16"

class ALU(VGroup):
	def __init__(self):
		super().__init__()

		self.alu = Polygon(*[
			[-0.6, 1.5, 0], # top left
			[-0.6, -1.5, 0], # bottom left
			[0.6, -0.95, 0], # bottom right
			[0.6, 0.95, 0] # top right
		])
		self.aluLabel = Text("ALU", font_size=28).move_to(self.alu.get_center())
		aluGroup = VGroup(self.alu, self.aluLabel)

		self.valAArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.alu.get_left()+(LEFT*0.8)+UP, end=self.alu.get_left()+UP)
		self.valALabel = CodeBlock("alu_vala", fontSize=26).next_to(self.valAArrow, UP, buff=0.1).shift(LEFT*0.25)
		self.valAText:Hexadecimal = None
		self.valA = -1
		valAGroup = VGroup(self.valAArrow, self.valALabel)

		self.valBArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.alu.get_left()+(LEFT*0.8), end=self.alu.get_left())
		self.valBLabel = CodeBlock("alu_valb", fontSize=26).next_to(self.valBArrow, UP, buff=0.1).shift(LEFT*0.25)
		self.valBText:Hexadecimal = None
		self.valB = -1
		valBGroup = VGroup(self.valBArrow, self.valBLabel)

		self.valHwArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.alu.get_left()+DOWN+(LEFT*0.8), end=self.alu.get_left()+DOWN)
		self.valHwLabel = CodeBlock("alu_valhw", fontSize=26).next_to(self.valHwArrow, UP, buff=0.1).shift(LEFT*0.3)
		self.valHwText:Hexadecimal = None
		self.valHw = -1
		valHwGroup = VGroup(self.valHwArrow, self.valHwLabel)

		self.valEArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=self.alu.get_right(), end=self.alu.get_right()+(RIGHT*0.8))
		self.valELabel = CodeBlock("val_e", fontSize=26).next_to(self.valEArrow, UP, buff=0.1)
		self.valEText = None
		self.valE = -1
		valEGroup = VGroup(self.valEArrow, self.valELabel)

		vertices = self.alu.get_vertices()

		midTop = self._lininterpol(vertices[0], (vertices[3]-vertices[0]), 0.5)
		midBottom = self._lininterpol(vertices[1], (vertices[2]-vertices[1]), 0.5)
		bottomLeft = self._lininterpol(vertices[1], (vertices[2]-vertices[1]), 0.25)
		bottomRight = self._lininterpol(vertices[1], (vertices[2]-vertices[1]), 0.8)

		self.condvalArrow = Arrow(
			max_tip_length_to_length_ratio=0.1
		).put_start_and_end_on(start=midTop, end=midTop+(UP*0.7))
		self.condvalLabel = CodeBlock("cond_val", fontSize=26).next_to(self.condvalArrow, RIGHT, buff=0.1)
		self.condvalText = None
		self.condval = -1
		condvalGroup = VGroup(self.condvalArrow, self.condvalLabel)

		self.condArrow = Arrow(
			max_tip_length_to_length_ratio=0.1, color=RED
		).put_start_and_end_on(start=bottomRight+(DOWN*0.5), end=bottomRight)
		self.condLabel = CodeBlock("cond", fontSize=26).next_to(self.condArrow, RIGHT, buff=0.1)
		self.condvalText = None
		self.cond = -1
		condGroup = VGroup(self.condArrow, self.condLabel)

		self.setCCArrow = Arrow(
			max_tip_length_to_length_ratio=0.1, color=RED
		).put_start_and_end_on(start=midBottom+(DOWN*0.8), end=midBottom)
		self.setCCLabel = CodeBlock("set_CC", fontSize=26).next_to(self.setCCArrow, RIGHT, buff=0.1).shift(DOWN*0.2)
		self.setCCText = None
		self.setCC = -1
		setCCGroup = VGroup(self.setCCArrow, self.setCCLabel)

		self.aluOpArrow = Arrow(
			max_tip_length_to_length_ratio=0.1, color=RED
		).put_start_and_end_on(start=bottomLeft+(DOWN*0.5), end=bottomLeft)
		self.aluOpLabel = CodeBlock("ALUop", fontSize=26).next_to(self.aluOpArrow, LEFT, buff=0.1)
		self.aluOpvalText = None
		self.aluOp = -1
		aluOpGroup = VGroup(self.aluOpArrow, self.aluOpLabel)

		self.add(*aluGroup, *valAGroup, *valBGroup, *valHwGroup, *valEGroup, *condvalGroup, *condGroup, *setCCGroup, *aluOpGroup)

	def setValA(self, valA:Hexadecimal) -> Hexadecimal:
		self.valA = valA.numval
		self.valAText = valA.next_to(self.valAArrow, DOWN, buff=0.005)
		self.valAText.submobjects[0].font_size = self.valALabel.submobjects[0].font_size

		return self.valAText
	
	def setValB(self, valB:Hexadecimal) -> Hexadecimal:
		self.valB = valB.numval
		self.valBText = valB.next_to(self.valBArrow, DOWN, buff=0.005)
		self.valBText.submobjects[0].font_size = self.valBLabel.submobjects[0].font_size

		return self.valBText
	
	def setValHw(self, valHw:Hexadecimal) -> Hexadecimal:
		self.valHw = valHw.numval
		self.valHwText = valHw.next_to(self.valHwArrow, DOWN, buff=0.005)
		self.valHwText.submobjects[0].font_size = self.valHwLabel.submobjects[0].font_size

		return self.valHwText

	def setValE(self, valE:Hexadecimal) -> Hexadecimal:
		self.valE = valE.numval
		self.valEText = valE.next_to(self.valEArrow, DOWN, buff=0.005)
		self.valEText.submobjects[0].font_size = self.valELabel.submobjects[0].font_size

		return self.valEText

	def setCC(self, setcc:bool=True) -> Arrow:
		if setcc: color = GREEN
		else: color = RED

		return self.setCCArrow.animate.set_color(color)

	def setALUOp(self, aluOp:Hexadecimal) -> Hexadecimal:
		self.aluOp = aluOp.numval
		self.aluOpText = aluOp.next_to(self.aluOpLabel, DOWN, buff=0.05)
		self.aluOpText.submobjects[0].font_size = self.aluOpLabel.submobjects[0].font_size

		return self.aluOpText

	def setCond(self, cond:Hexadecimal) -> Hexadecimal:
		self.cond = cond.numval
		self.condText = cond.next_to(self.condLabel, DOWN, buff=0.05)
		self.condText.submobjects[0].font_size = self.condLabel.submobjects[0].font_size

		return self.condText

	def setCondVal(self, condval:Hexadecimal) -> Hexadecimal:
		self.condval = condval.numval
		self.condvalText = condval.next_to(self.condvalLabel, UP, buff=0.05)
		self.condvalText.submobjects[0].font_size = self.condvalLabel.submobjects[0].font_size

		return self.condvalText

	def _lininterpol(self, A, B, t):
		return A + t * (B)