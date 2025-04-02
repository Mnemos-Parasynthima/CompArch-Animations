from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, Text, Rectangle, DL, Arrow, Succession, FadeIn, Animation, AnimationGroup, BLUE, FadeOut
from .core import Stage, Register
from .RegFile import RegFile
from .logic import Mux
from .Path import Path
from ..hexdec import CodeBlock, Hexadecimal


class DecodeStage(Stage): 
	def __init__(self):
		super().__init__(10, 5)

		self.regfile = RegFile().shift(RIGHT*3)
		self.dstmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*0.5 + UP*0.34)
		self.dstmux.addSignal(CodeBlock("dst_sel", fontSize=23), Mux.TOP)
		self.src2mux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*0.5 + DOWN)
		self.src2mux.addSignal(CodeBlock("src2_sel", fontSize=23), Mux.BOTTOM)
		self.decodeLogic = RoundedRectangle(corner_radius=0.4, width=2, height=3).shift(LEFT*3.5)
		self.decodeLogicLabel = Text("Decode\n  Logic", font_size=28).move_to(self.decodeLogic.get_center())

		self.add(self.regfile, self.dstmux, self.src2mux, self.decodeLogic, self.decodeLogicLabel)

		dstmux_regfile = Path(self.dstmux.outputArrows[0].get_right(), self.regfile.dstArrow.get_left(), color=RED, strokeWidth=2)
		self.paths["dstmux_regfile"] = dstmux_regfile

		src2mux_regfile = Path(self.src2mux.outputArrows[0].get_right(), self.regfile.src2Arrow.get_left(), color=RED, strokeWidth=2)
		self.paths["src2mux_regfile"] = src2mux_regfile

		self.add(*list(self.paths.values()))

	def animateMuxs(self, dst:str, src2_1:str, src2_2:str, dstSel:bool, src2Sel:bool) -> Succession:
		anims:list[Animation|AnimationGroup] = []

		if self.dstmux.inputText[0]:
			anims.append(
				FadeOut(
					*self.dstmux.inputText, *self.src2mux.inputText, self.dstmux.outputText[0], self.src2mux.outputText[0],
					shift=RIGHT
				)
			)

		anims.append(
			FadeIn(
				*self.dstmux.setArrowInfoList([Hexadecimal(dst), Hexadecimal("30")], []),
				*self.src2mux.setArrowInfoList([Hexadecimal(src2_1), Hexadecimal(src2_2)], []),
				shift=RIGHT
			)
		)

		anims.append(
			AnimationGroup(
				*self.dstmux.setSignal(1 if dstSel else 0),
				*self.src2mux.setSignal(1 if src2Sel else 0)
			)
		)

		anims.append(
			AnimationGroup(
				FadeIn(
					self.dstmux.setArrowInfo(Hexadecimal("30" if dstSel else dst), 0, False),
					self.src2mux.setArrowInfo(Hexadecimal(src2_2 if src2Sel else src2_1), 0, False),
					shift=RIGHT
				),
				self.highlightPath("dstmux_regfile").build(),
				self.highlightPath("src2mux_regfile").build(),
				*self.dstmux.setSignal(),
				*self.src2mux.setSignal()
			)
		)

		return Succession(*anims)

	def animateRegfileRead(self, dst:str, src1:str, src2:str, valA:str, valB:str, globalPaths:dict[str, Path]) -> Succession:
		anims:list[Animation|AnimationGroup] = []

		if self.regfile.dstText:
			anims.append(
				FadeOut(
					self.regfile.dstText, self.regfile.src1Text, self.regfile.src2Text, 
					self.regfile.valAText, self.regfile.valBText,
					shift=RIGHT
				)
			)

		anims.append(
			FadeIn(
				self.regfile.setDst(Hexadecimal(dst)),
				self.regfile.setSrc1(Hexadecimal(src1)),
				self.regfile.setSrc2(Hexadecimal(src2)),
				shift=RIGHT
			)
		)

		anims.append(
			AnimationGroup(
				self.dehighlightPath("dstmux_regfile").build(), 
				self.dehighlightPath("src2mux_regfile").build(),
				FadeIn(
					self.regfile.setValA(Hexadecimal(valA)),
					self.regfile.setValB(Hexadecimal(valB)),
					shift=RIGHT
				),
				globalPaths["regfile_alu"].highlight(BLUE, 4).build(),
				globalPaths["regfile_valbmux_dmem"].highlight(BLUE, 4).build(),
				globalPaths["regfile_nextmux"].highlight(BLUE, 4).build()
			)
		)

		return Succession(*anims)

	def animateRegfileWrite(self, wval:str, writeEnable:bool, globalPaths:dict[str, Path]) -> Succession:
		anims:list[Animation|AnimationGroup] = []

		if self.regfile.valWText: anims.append(FadeOut(self.regfile.valWText, shift=RIGHT))

		anims.append(FadeIn(self.regfile.setValW(Hexadecimal(wval)), shift=RIGHT))

		if writeEnable: anims.append(self.regfile.writeEnable().build())

		anims.append(
			AnimationGroup(
				self.regfile.writeEnable(False).build(),
				globalPaths["regfile_dstmux2"].highlight(RED, 2)
			)
		)

		return Succession(*anims)


class DecodePipeline(Register):
	def __init__(self):
		super().__init__(Register.DECODE)

		for i in range(len(self.components)):
			if i not in (0, 1, 2, 3, 4):
				self.components[i] = None
				self.componentsText[i] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))


class DecodeElements(Stage): 
	def __init__(self):
		super().__init__(10, 4)

		stageLabel = CodeBlock("decode_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.25)
		self.add(stageLabel)

		self.regfile = Rectangle(width=1.4, height=1.2).shift(RIGHT*2 + DOWN*0.4)
		self.regfileLabel = CodeBlock("regfile", fontSize=30).move_to(self.regfile.get_center())
		regfileGroup = VGroup(self.regfile, self.regfileLabel)

		self.extractImmval = Rectangle(width=1.5, height=0.75).shift(RIGHT*3.7 + DOWN*0.4)
		self.extractImmvalLabel = CodeBlock("extract_immval", fontSize=18).move_to(self.extractImmval.get_center())
		extractImmvalGroup = VGroup(self.extractImmval, self.extractImmvalLabel)

		self.generateControl = Rectangle(width=2, height=0.9).shift(LEFT*1.6 + UP*1.25)
		self.generateControlLabel = CodeBlock("generate_DMXW_control", fontSize=16).move_to(self.generateControl.get_center())
		generateControlGroup = VGroup(self.generateControl, self.generateControlLabel)

		self.decideALUOp = Rectangle(width=1.6, height=1).shift(DOWN*0.4 + LEFT*0.35)
		self.decideALUOpLabel = CodeBlock("decide_ALU_op", fontSize=20).move_to(self.decideALUOp.get_center())
		decideALUOpGroup = VGroup(self.decideALUOp, self.decideALUOpLabel)

		self.forwardReg = Rectangle(width=1.6, height=1).shift(RIGHT*2 + UP*1.25)
		self.forwardRegLabel = CodeBlock("forward_reg", fontSize=20).move_to(self.forwardReg.get_center())
		forwardRegGroup = VGroup(self.forwardReg, self.forwardRegLabel)

		self.dSigs = Rectangle(width=0.7, height=1).move_to(self.generateControl.get_bottom() + DOWN*2)
		self.dSigsLabel = CodeBlock("D_sigs", fontSize=18).move_to(self.dSigs.get_center())
		dSigsGroup = VGroup(self.dSigs, self.dSigsLabel)

		self.add(regfileGroup, extractImmvalGroup, generateControlGroup, decideALUOpGroup, forwardRegGroup, dSigsGroup)
		
		forwardregBottom = self.forwardReg.get_bottom()
		regfileLeft = self.regfile.get_left()
		regfileRight = self.regfile.get_right()
		regfileTop = self.regfile.get_top()
		regfileBottom = self.regfile.get_bottom()
		regfileArrows = [
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=[regfileLeft[0], regfileBottom[1]-0.6, 0], end=[regfileLeft[0], regfileBottom[1], 0]),
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=[regfileLeft[0]+0.3, regfileBottom[1]-0.6, 0], end=[regfileLeft[0]+0.3, regfileBottom[1], 0]),
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=[regfileLeft[0]+0.6, regfileBottom[1]-0.6, 0], end=[regfileLeft[0]+0.6, regfileBottom[1], 0]),
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=[regfileLeft[0]+0.9, regfileBottom[1]-0.6, 0], end=[regfileLeft[0]+0.9, regfileBottom[1], 0]),
			Arrow(
				max_tip_length_to_length_ratio=0.1,
				color=RED
			).put_start_and_end_on(start=[regfileLeft[0]+1.2, regfileBottom[1]-0.6, 0], end=[regfileLeft[0]+1.2, regfileBottom[1], 0]),
		]
		self.add(*regfileArrows)

		forwardregArrows = [
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=[regfileLeft[0]+0.6, regfileTop[1], 0], end=[regfileLeft[0]+0.6, forwardregBottom[1], 0]),
			Arrow(
				max_tip_length_to_length_ratio=0.1
			).put_start_and_end_on(start=[regfileRight[0]-0.6, regfileTop[1], 0], end=[regfileRight[0]-0.6, forwardregBottom[1], 0]),
		]
		self.add(*forwardregArrows)

		dSigsArrows = [
			Arrow(
				max_tip_length_to_length_ratio=0.1,
				color=RED,
				max_stroke_width_to_length_ratio=2.5
			).put_start_and_end_on(start=self.generateControl.get_bottom(), end=self.dSigs.get_top()),
			Arrow(
				max_tip_length_to_length_ratio=0.1,
				color=RED
			).put_start_and_end_on(start=self.dSigs.get_right(), end=self.dSigs.get_right()+RIGHT*0.8)
		]
		dSigsLabel = CodeBlock("src2_sel", fontSize=16).next_to(dSigsArrows[1], UP, buff=0.03)
		self.add(*dSigsArrows, dSigsLabel)
