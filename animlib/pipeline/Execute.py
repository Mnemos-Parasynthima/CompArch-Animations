from manim import RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Rectangle, DL, Succession, FadeIn, AnimationGroup, Animation, FadeOut, YELLOW, BLACK
from .core import Stage, Register
from .ALU import ALU, alu_op_t, cond_t
from .logic import Mux
from .Path import Path, ArrowPath
from ..hexdec import CodeBlock, Hexadecimal


class ExecuteStage(Stage): 
	def __init__(self):
		super().__init__(6.5, 5)

		self.alu = ALU().shift(RIGHT*1.8)
		self.valbmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*1.5)
		# valbmux has a very different configuration than the other Muxes, leading to the texts being flipped
		# Manually reorder them
		oldHex0 =	self.valbmux.inputLabels[0]
		oldHex1 = self.valbmux.inputLabels[1]
		self.valbmux.inputLabels[0] = Hexadecimal("1", fontSize=oldHex0.submobjects[0].font_size).move_to(oldHex0)
		self.valbmux.inputLabels[1] = Hexadecimal("0", fontSize=oldHex1.submobjects[0].font_size).move_to(oldHex1)
		self.valbmux.submobjects[-1] = self.valbmux.inputLabels[0]
		self.valbmux.submobjects[-2] = self.valbmux.inputLabels[1]

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

		anims.append(AnimationGroup(*self.valbmux.setSignal(1 if valbSel else 0)))

		anims.append(
			AnimationGroup(
				FadeIn(self.valbmux.setArrowInfo(Hexadecimal(valb if valbSel else imm), 0, False), shift=RIGHT),
				self.highlightPath("valbmux_alu"),
				*self.valbmux.setSignal()
			)
		)

		return Succession(*anims)

	def animateALU(self, valA:str, valB:str, valHw:str, aluOp:alu_op_t, setCC:bool, cond:cond_t, condVal:bool, valE:str, globalPaths:dict[str, Path]) -> Succession:
		anims:list[Animation|AnimationGroup] = []

		if self.alu.valAText:
			anims.append(
				AnimationGroup(
					FadeOut(
						self.alu.valAText, self.alu.valBText, self.alu.valHwText, self.alu.valEText,
						shift=RIGHT
					),
					FadeOut(
						self.alu.aluOpText, self.alu.condText,
						shift=UP
					)
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

		anims.append(
			AnimationGroup(
				FadeIn(self.alu.setALUOp(aluOp), self.alu.setCond(cond), shift=UP),
				self.alu.setCC(setCC)
			)
		)

		anims.append(
			AnimationGroup(
				self.dehighlightPath("valbmux_alu"),
				globalPaths["regfile_alu"].highlight(RED, 2),
				FadeIn(self.alu.setValE(Hexadecimal(valE)), shift=RIGHT),
				self.alu.setCondVal(condVal),
				globalPaths["alu_dmem_wvalmux"].highlight(BLUE, 4),
				self.alu.setCC(False)
			)
		)

		if condVal: anims.append(self.alu.setCondVal(False))

		return Succession(*anims)

class ExecutePipeline(Register):
	def __init__(self):
		super().__init__(Register.EXECUTE)

		self.components[1] = None
		self.componentsText[1] = None

		# Used to store state for clock transition
		self.opIn:CodeBlock = None
		self.seqSuccPCIn:Hexadecimal = None
		self.aluOpIn:CodeBlock = None
		self.condIn:CodeBlock = None
		self.valAIn:Hexadecimal = None
		self.valBIn:Hexadecimal = None
		self.valImmIn:Hexadecimal = None
		self.hwIn:Hexadecimal = None
		self.dstIn:Hexadecimal = None

		self.opOut:CodeBlock = None
		self.seqSuccPCOut:Hexadecimal = None
		self.aluOpOut:CodeBlock = None
		self.condOut:CodeBlock = None
		self.valAOut:Hexadecimal = None
		self.valBOut:Hexadecimal = None
		self.valImmOut:Hexadecimal = None
		self.hwOut:Hexadecimal = None
		self.dstOut:Hexadecimal = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

	def animateXin(self, op:str, seqSuccPC:str, aluOp:str, cond:str, valA:str, valB:str, valImm:str, hw:str, dst:str):
		self.opIn = CodeBlock(op, fontSize=20).move_to(self.components[2].get_bottom()+UP*0.2)
		self.seqSuccPCIn = Hexadecimal(seqSuccPC, fontSize=20).move_to(self.components[3].get_bottom()+UP*0.2)
		self.aluOpIn = CodeBlock(aluOp, fontSize=20).move_to(self.components[7].get_bottom()+UP*0.2)
		self.condIn = CodeBlock(cond, fontSize=20).move_to(self.components[8].get_bottom()+UP*0.2)
		self.valAIn = Hexadecimal(valA, fontSize=20).move_to(self.components[9].get_bottom()+UP*0.2)
		self.valBIn = Hexadecimal(valB, fontSize=20).move_to(self.components[10].get_bottom()+UP*0.2)
		self.valImmIn = Hexadecimal(valImm, fontSize=20).move_to(self.components[11].get_bottom()+UP*0.2)
		self.hwIn = Hexadecimal(hw, fontSize=20).move_to(self.components[12].get_bottom()+UP*0.2)
		self.dstIn = Hexadecimal(dst, fontSize=20).move_to(self.components[13].get_bottom()+UP*0.2)

		anim = FadeIn(self.opIn, self.seqSuccPCIn, self.aluOpIn, self.condIn, self.valAIn, self.valBIn, self.valImmIn, self.hwIn, self.dstIn, shift=UP)

		return anim

	def animateXout(self, op:str, seqSuccPC:str, aluOp:str, cond:str, valA:str, valB:str, valImm:str, hw:str, dst:str):
		self.opOut = CodeBlock(op, fontSize=20).move_to(self.components[2].get_top()+DOWN*0.2)
		self.seqSuccPCOut = Hexadecimal(seqSuccPC, fontSize=20).move_to(self.components[3].get_top()+DOWN*0.2)
		self.aluOpOut = CodeBlock(aluOp, fontSize=20).move_to(self.components[7].get_top()+DOWN*0.2)
		self.condOut = CodeBlock(cond, fontSize=20).move_to(self.components[8].get_top()+DOWN*0.2)
		self.valAOut = Hexadecimal(valA, fontSize=20).move_to(self.components[9].get_top()+DOWN*0.2)
		self.valBOut = Hexadecimal(valB, fontSize=20).move_to(self.components[10].get_top()+DOWN*0.2)
		self.valImmOut = Hexadecimal(valImm, fontSize=20).move_to(self.components[11].get_top()+DOWN*0.2)
		self.hwOut = Hexadecimal(hw, fontSize=20).move_to(self.components[12].get_top()+DOWN*0.2)
		self.dstOut = Hexadecimal(dst, fontSize=20).move_to(self.components[13].get_top()+DOWN*0.2)

		anim = FadeIn(self.opOut, self.seqSuccPCOut, self.aluOpOut, self.condOut, self.valAOut, self.valBOut, self.valImmOut, self.hwOut, self.dstOut, shift=UP)

		return anim

	def animateClock(self) -> Succession:
		anims:list[Animation] = []

		anims.append(AnimationGroup(self.submobjects[1].animate.set_fill(YELLOW, 1)))
		anims.append(FadeOut(self.opOut, self.seqSuccPCOut, self.aluOpOut, self.condOut, self.valAOut, self.valBOut, self.valImmOut, self.hwOut, self.dstOut, shift=UP))
		anims.append(FadeOut(self.opIn, self.seqSuccPCIn, self.aluOpIn, self.condIn, self.valAIn, self.valBIn, self.valImmIn, self.hwIn, self.dstIn, shift=UP))
		anims.append(self.animateXout(self.opIn.value, self.seqSuccPCIn.value, self.aluOpIn.value, self.condIn.value, self.valAIn.value, self.valBIn.value, self.valImmIn.value, self.hwIn.value, self.dstIn.value))
		anims.append(AnimationGroup(self.submobjects[1].animate.set_fill(BLACK, 1)))

		return Succession(*anims)

class ExecuteElements(Stage):
	def __init__(self):
		super().__init__(10, 4)

		stageLabel = CodeBlock("execute_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.3)
		self.add(stageLabel)

		self.alu = Rectangle(width=1.4, height=1.2).shift(RIGHT*1.53 + UP*0.8)
		self.aluLabel = CodeBlock("alu", fontSize=30).move_to(self.alu.get_center())

		# self.valaMux = RoundedRectangle(corner_radius=0.25, width=1.85, height=0.5).shift(RIGHT + DOWN*1.4)
		# self.valaMuxLabel = CodeBlock("2:1 mux", fontSize=20).move_to(self.valaMux.get_center())

		self.valbMux = RoundedRectangle(corner_radius=0.25, width=1.85, height=0.5).shift(RIGHT*2.75 + DOWN*0.4)
		self.valbMuxLabel = CodeBlock("2:1 mux", fontSize=20).move_to(self.valbMux.get_center())

		self.add(self.alu, self.aluLabel, self.valbMux, self.valbMuxLabel)#, self.valaMux, self.valaMuxLabel)
		
		# aluBottom = self.alu.get_bottom()
		# valaMuxTop = self.valaMux.get_top()
		# valaMuxLeft = self.valaMux.get_left()

		# valaMux_alu = ArrowPath(
		# 	valaMuxTop, aluBottom,
		# 	color=BLUE, strokeWidth=3
		# )


		aluRight = self.alu.get_right()
		valbMuxTop = self.valbMux.get_top()
		valbMuxRight = self.valbMux.get_right()

		valbMux_alu = ArrowPath(
			valbMuxTop, [valbMuxTop[0], aluRight[1], 0], aluRight,
			color=BLUE, strokeWidth=3
		)

		setCC = ArrowPath(
			[valbMuxTop[0]+0.2, (aluRight+UP*0.3)[1], 0], (aluRight+UP*0.3),
			color=RED, strokeWidth=2
		)
		setCCLabel = CodeBlock("set_CC", fontSize=16).next_to(setCC, UP, buff=0.05)

		valbSel = ArrowPath(
			valbMuxRight+RIGHT*0.8, valbMuxRight,
			color=RED, strokeWidth=2
		)
		valbSelLabel = CodeBlock("valb_sel", fontSize=16).next_to(valbSel, UP, buff=0.05)

		# valaSel = ArrowPath(
		# 	valaMuxLeft+LEFT*0.4, valaMuxLeft,
		# 	color=RED, strokeWidth=2
		# )
		# valaSelLabel = CodeBlock("op" fontSize=16).next_to(valaSel, UP, buff=0.05)

		self.add(valbMux_alu, setCC, setCCLabel, valbSel, valbSelLabel)#, valaMux_alu, valaSel, valaSelLabel)

		self.aluValBMuxText:Hexadecimal = None
		self.aluValAText:Hexadecimal = None

		self.instruction:CodeBlock = None

	def animateMux(self, valB:str, valImm:str, aluValB:str, globalPaths:dict[str,ArrowPath]):
		anims = []

		if self.aluValBMuxText:
			anims.append(FadeOut(self.valBText, self.valImmText, self.aluValBMuxText))

		self.valBText = Hexadecimal(valB, fontSize=20).next_to(globalPaths["valB_mux"].pathPoints[1], LEFT, buff=0.1, aligned_edge=RIGHT).shift(DOWN*0.2)
		self.valImmText = Hexadecimal(valImm, fontSize=20).next_to(globalPaths["valImm_mux"].pathPoints[1], LEFT, buff=0.1, aligned_edge=RIGHT).shift(DOWN*0.2)
		self.aluValBMuxText = Hexadecimal(aluValB, fontSize=20).next_to(self.valbMux.get_top(), LEFT, buff=0.08).shift(UP*0.2)

		anims.append(FadeIn(self.valBText, self.valImmText, shift=UP))
		anims.append(FadeIn(self.aluValBMuxText, shift=UP))

		return Succession(*anims)
	
	def animateALU(self, aluValA:str, aluValB:str, hw:str, aluOp:str, cond:str, condholds:str, valEx:str, globalPaths:dict[str,ArrowPath]):
		anims = []

		if self.aluValAText:
			anims.append(FadeOut(self.aluValAText, self.aluValBAluText, self.hwText, self.aluOpText, self.condText, self.condholdsText, self.valExText))

		self.aluValAText = Hexadecimal(aluValA, fontSize=20).next_to(self.alu.get_bottom(), RIGHT).shift(DOWN*0.2)
		self.aluValBAluText = Hexadecimal(aluValB, fontSize=20).next_to(self.alu.get_right(), UP, buff=0.1, aligned_edge=LEFT).shift(RIGHT*0.2)
		self.hwText = Hexadecimal(hw, fontSize=20).move_to(globalPaths["hw_alu"].pathPoints[2]).shift(RIGHT*0.2 + UP*0.2)
		self.aluOpText = CodeBlock(aluOp, fontSize=20).next_to(globalPaths["aluOp_alu"].pathPoints[3], LEFT, buff=0.2)
		self.condText = CodeBlock(cond, fontSize=20).move_to(globalPaths["cond_alu"].pathPoints[3]).shift(UP*0.1)
		self.condholdsText = CodeBlock(condholds, fontSize=20).next_to(self.alu.get_left(), UP).shift(LEFT*0.2)
		self.valExText = Hexadecimal(valEx, fontSize=20).next_to(self.alu.get_top(), LEFT).shift(UP*0.2)

		anims.append(
			AnimationGroup(
				FadeIn(self.aluOpText, self.condText, self.aluValAText, shift=UP),
				FadeIn(self.hwText, self.aluValBAluText, shift=LEFT)
			)
		)

		anims.append(
			AnimationGroup(
				FadeIn(self.valExText, shift=UP),
				FadeIn(self.condholdsText, shift=LEFT)
			)
		)

		return Succession(*anims)
	
	def animateInstruction(self, instr:str):
		anims = []

		if self.instruction:
			anims.append(FadeOut(self.instruction))

		self.instruction = CodeBlock(instr, fontSize=50).next_to(self.submobjects[0], RIGHT).shift(RIGHT*5)

		anims.append(FadeIn(self.instruction))

		return Succession(*anims)