from manim import RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Rectangle, DL, Succession, FadeIn, AnimationGroup, Animation, FadeOut
from .core import Stage, Register
from .ALU import ALU
from .logic import Mux
from .Path import Path, ArrowPath
from ..hexdec import CodeBlock, Hexadecimal


class ExecuteStage(Stage): 
	def __init__(self):
		super().__init__(6.5, 5)

		self.alu = ALU().shift(RIGHT*1.8)
		self.valbmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*1.5)
		self.valbmux.addSignal(CodeBlock("valb_sel", fontSize=23), Mux.BOTTOM)

		self.add(self.alu, self.valbmux)

		valbmux_alu = Path(self.valbmux.outputArrows[0].get_right(), self.alu.valBArrow.get_left(), color=RED, strokeWidth=2)
		self.paths["valbmux_alu"] = valbmux_alu

		self.add(*list(self.paths.values()))

	def animateMux(self, valb:str, imm:str, valbSel:bool) -> Succession:
		anims:list[Animation|AnimationGroup] = []
		
		if self.valbmux.inputText[0]:
			anims.append(
				FadeOut(
					*self.valbmux.inputText, *self.valbmux.outputText,
					shift=RIGHT
				)
			)

		anims.append(
			FadeIn(
				*self.valbmux.setArrowInfoList([Hexadecimal(valb), Hexadecimal(imm)], []),
				shift=RIGHT
			)
		)

		# anims.append(
		# 	self.valbmux.setSignal()
		# )

		anims.append(
			AnimationGroup(
				FadeIn(self.valbmux.setArrowInfo(Hexadecimal(valb if valbSel else imm), 0, False), shift=RIGHT),
				self.highlightPath("valbmux_alu")
			)
		)

		return Succession(*anims)

	def animateALU(self, valA:str, valB:str, valHw:str, valE:str, globalPaths:dict[str, Path]) -> Succession:
		anims = []

		if self.alu.valAText:
			anims.append(
				FadeOut(
					self.alu.valAText, self.alu.valBText, self.alu.valHwText, self.alu.valEText,
					shift=RIGHT
				)
			)

		anims.append(
			FadeIn(
				self.alu.setValA(Hexadecimal(valA)),
				self.alu.setValB(Hexadecimal(valB)),
				self.alu.setValHw(Hexadecimal(valHw)),
				shift=RIGHT
			)
		)

		# anims.append(
			# For setting conditions
		# )

		anims.append(
			AnimationGroup(
				self.dehighlightPath("valbmux_alu"),
				globalPaths["regfile_alu"].highlight(RED, 2),
				FadeIn(self.alu.setValE(Hexadecimal(valE)), shift=RIGHT),
				# setting condval
				globalPaths["alu_dmem_wvalmux"].highlight(BLUE, 4)
			)
		)

		return Succession(*anims)

class ExecutePipeline(Register):
	def __init__(self):
		super().__init__(Register.EXECUTE)

		self.components[1] = None
		self.componentsText[1] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

class ExecuteElements(Stage):
	def __init__(self):
		super().__init__(10, 4)

		stageLabel = CodeBlock("execute_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.3)
		self.add(stageLabel)

		self.alu = Rectangle(width=1.4, height=1.2).shift(RIGHT*1.53 + UP*0.4)
		self.aluLabel = CodeBlock("alu", fontSize=30).move_to(self.alu.get_center())

		self.mux = RoundedRectangle(corner_radius=0.25, width=1.85, height=0.5).shift(RIGHT*2.75 + DOWN)
		self.muxLabel = CodeBlock("2:1 mux", fontSize=20).move_to(self.mux.get_center())

		self.add(self.alu, self.aluLabel, self.mux, self.muxLabel)
		
		aluRight = self.alu.get_right()
		muxTop = self.mux.get_top()

		mux_alu = ArrowPath(
			muxTop, [muxTop[0], aluRight[1], 0], aluRight,
			color=BLUE, strokeWidth=3
		)

		self.add(mux_alu)