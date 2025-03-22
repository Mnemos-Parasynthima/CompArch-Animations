from manim import LEFT, RIGHT, UP, DOWN, RED, BLUE, Rectangle, Arrow, DL, FadeIn, AnimationGroup, Succession, Animation, FadeOut
from .core import Stage, Register
from .PC import PC
from .IMem import IMem
from .logic import Adder, Mux
from .Path import Path, ArrowPath
from ..hexdec import CodeBlock, Hexadecimal


class FetchStage(Stage): 
	def __init__(self):
		super().__init__(6, 8)

		self.pc = PC().shift(DOWN*2.4 + LEFT*1.65).scale(0.8)
		self.imem = IMem().shift(DOWN*3 + RIGHT*1.2).scale(0.8)
		self.mux = Mux(4,1, width=1.5, direction=Mux.RL).shift(LEFT*1.24 + UP*2) #2.5
		self.mux.addSignal(CodeBlock("next_PC_sel", fontSize=23), Mux.TOP)
		self.seqPCAdder = Adder(CodeBlock("4", fontSize=40), 4).shift(RIGHT*0.8 + DOWN*0.5).scale(0.5)
		label = CodeBlock("branch_offset", fontSize=40)
		self.brPCAdder = Adder(label).shift(RIGHT*1.6 + DOWN*0.5).scale(0.5)

		self.add(self.pc, self.imem, self.mux, self.seqPCAdder, self.brPCAdder)

		mux_pc = Path(self.mux.outputArrows[0].get_left(), self.pc.nextPCArrow.get_left(), color=RED, strokeWidth=2)
		self.paths["mux_pc"] = mux_pc

		pcRight = self.pc.currPCArrow.get_right()
		addrLeft = self.imem.addrArrow.get_left()
		seqDown = self.seqPCAdder.aArrow.get_bottom()
		brDown = self.brPCAdder.aArrow.get_bottom()
		pc_imem_adders = Path(
			pcRight,
			[pcRight[0], addrLeft[1], 0],
			addrLeft, [pcRight[0], addrLeft[1], 0],
			pcRight+UP, [seqDown[0], (pcRight+UP)[1], 0],
			seqDown, [seqDown[0], (pcRight+UP)[1], 0],
			[brDown[0], (pcRight+UP)[1], 0], brDown,
			color=RED, strokeWidth=2
		).markIntersections([0], RED)
		self.paths["pc_imem_adders"] = pc_imem_adders

		seqUp = self.seqPCAdder.cArrow.get_top()
		muxIn0Right = self.mux.inputArrows[0].get_right()
		muxIn1Right = self.mux.inputArrows[1].get_right()
		seqAdder_mux = Path(
			seqUp, [seqUp[0], muxIn1Right[1], 0], 
			muxIn1Right, [seqUp[0], muxIn1Right[1], 0],
			[seqUp[0], muxIn0Right[1], 0], muxIn0Right, color=RED, strokeWidth=2
		).markIntersections([1], RED)
		self.paths["seqAdder_mux"] = seqAdder_mux

		brUp = self.brPCAdder.cArrow.get_top()
		muxIn2Right = self.mux.inputArrows[2].get_right()
		brAdder_mux = Path(brUp, [brUp[0], muxIn2Right[1], 0], muxIn2Right, color=RED, strokeWidth=2)
		self.paths["brAdder_mux"] = brAdder_mux

		self.add(*list(self.paths.values()))

	def animateCurrPC(self, pc:str, insn:str, globalPaths:dict[str,Path|ArrowPath]) -> Succession:
		anims:list[AnimationGroup|Animation] = []

		# Clear out previous displays. Since all of the `set*`s are done in one group, it is implied
		# Only need to check one and clear all others
		if self.pc.currPCText: 
			anims.append(
				FadeOut(
					self.pc.currPCText, self.imem.addrText, self.seqPCAdder.aText, self.brPCAdder.aText, self.imem.rvalText
					# shift=RIGHT
				),
			)


		anims.append(
			FadeIn(self.pc.setCurrPC(Hexadecimal(pc)), shift=RIGHT)
		)

		anims.append(
			AnimationGroup(
				FadeIn(self.imem.setAddr(Hexadecimal(pc)), shift=RIGHT),
				self.highlightPath("pc_imem_adders").build(),
				FadeIn(
					self.seqPCAdder.setA(Hexadecimal(pc)),
					self.brPCAdder.setA(Hexadecimal(pc)),
					shift=UP
				)
			)
		)

		anims.append(
			self.dehighlightPath("pc_imem_adders").build()
		)

		anims.append(
			AnimationGroup(
				FadeIn(self.imem.setRVal(Hexadecimal(insn)), shift=RIGHT),
				globalPaths["imem_DecodeLogic"].highlight(BLUE, 4)
			)
		)

		return Succession(*anims)

	def animatePredPC(self, seqPC:str, brPC:str, globalPaths:dict[str,Path|ArrowPath]) -> Succession:
		anims:list[AnimationGroup|Animation] = []

		if self.seqPCAdder.cText:
			anims.append(
				FadeOut(
					self.seqPCAdder.cText, self.brPCAdder.cText, *self.mux.inputText
					# shift=RIGHT
				),
			)

		anims.append(
			AnimationGroup(
				FadeIn(self.seqPCAdder.setC(Hexadecimal(seqPC)), shift=UP),
				FadeIn(self.brPCAdder.setC(Hexadecimal(brPC)), shift=UP)
			)
		)

		anims.append(
			AnimationGroup(
				FadeIn(
					self.mux.setArrowInfo(Hexadecimal(seqPC), 0),
					self.mux.setArrowInfo(Hexadecimal(seqPC), 1),
					self.mux.setArrowInfo(Hexadecimal(brPC), 2),
					shift=LEFT
				),
				self.highlightPath("seqAdder_mux"),
				self.highlightPath("brAdder_mux"),
				globalPaths["dstmux_pcmux"].highlight(BLUE, 4),
				globalPaths["imem_DecodeLogic"].highlight(RED, 2)
			)
		)

		return Succession(*anims)
	
	def animateUpdatePC(self, valB:str, nextpc:str, globalPaths:dict[str, Path]) -> Succession:
		anims:list[Animation|AnimationGroup] = []
		
		anims.append(FadeIn(self.mux.setArrowInfo(Hexadecimal(valB), 3), shift=LEFT))

		# anims.append(self.mux.setSignal())

		if self.mux.outputText[0]: anims.append(FadeOut(self.mux.outputText[0],	shift=LEFT))

		anims.append(
			AnimationGroup(
				self.dehighlightPath("seqAdder_mux"),
				self.dehighlightPath("brAdder_mux"),
				globalPaths["dstmux_pcmux"].highlight(RED, 2),
				globalPaths["regfile_nextmux"].highlight(RED, 2),
				FadeIn(self.mux.setArrowInfo(Hexadecimal(nextpc), 0, False), shift=LEFT),
				self.highlightPath("mux_pc")
			)
		)

		return Succession(*anims)

	def animateUpdateEnd(self, nextpc:str) -> Succession:
		anims:list[AnimationGroup|Animation] = []

		if self.pc.nextPCText: anims.append(FadeOut(self.pc.nextPCText, shift=RIGHT))

		anims.append(AnimationGroup(
			FadeIn(self.pc.setNextPC(Hexadecimal(nextpc)), shift=RIGHT),
			self.dehighlightPath("mux_pc")
		))

		return Succession(*anims)

class FetchPipeline(Register): 
	def __init__(self):
		super().__init__(Register.FETCH)

		for i in range(len(self.components)):
			if i not in (0, 3):
				self.components[i] = None
				self.componentsText[i] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))


class FetchElements(Stage):
	def __init__(self):
		super().__init__(10, 4)

		stageLabel = CodeBlock("fetch_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.25)
		self.add(stageLabel)

		self.imem = Rectangle(width=1.2, height=1.2).shift(DOWN*0.2)
		self.imemLabel = CodeBlock("imem", fontSize=30).move_to(self.imem.get_center())

		self.selectPC = Rectangle(width=1.2, height=1.35).shift(DOWN*0.2 + LEFT*2.5)
		self.selectPCLabel = CodeBlock("select_PC", fontSize=20).move_to(self.selectPC.get_center())

		self.predictPC = Rectangle(width=1.8, height=0.85).shift(UP*0.2 + RIGHT*2.75)
		self.predictPCLabel = CodeBlock("predict_PC", fontSize=28).move_to(self.predictPC.get_center())

		self.extractOpcode = Rectangle(width=1.5, height=0.75).shift(LEFT*3 + UP*1.25)
		self.extractOpcodeLabel = CodeBlock("extract_opcode", fontSize=18).move_to(self.extractOpcode.get_center())

		self.add(self.imem, self.imemLabel, self.selectPC, self.selectPCLabel, self.predictPC, self.predictPCLabel, self.extractOpcode, self.extractOpcodeLabel)

		selectPCLeft = self.selectPC.get_left()
		selectPCRight = self.selectPC.get_right()
		selectPCTop = self.selectPC.get_top()
		selectPCBottom = self.selectPC.get_bottom()
		selectPCCenter = self.selectPC.get_center()
		selectPCArrows = [
			Arrow( # M_opcode
				max_tip_length_to_length_ratio=0.1,
				color=RED
			).put_start_and_end_on(start=[selectPCLeft[0]-0.8, selectPCBottom[1]+0.1, 0], end=[selectPCLeft[0], selectPCBottom[1]+0.1, 0]),
			Arrow( # M_cond_val
				max_tip_length_to_length_ratio=0.1,
				color=RED
			).put_start_and_end_on(start=[selectPCLeft[0]-0.8, selectPCBottom[1]+0.4, 0], end=[selectPCLeft[0], selectPCBottom[1]+0.4, 0]),
			Arrow( # seq_succ_PC
				max_tip_length_to_length_ratio=0.1,
				color=BLUE
			).put_start_and_end_on(start=[selectPCLeft[0]-0.8, selectPCCenter[1], 0], end=[selectPCLeft[0], selectPCCenter[1], 0]),
			Arrow( # D_opcode
				max_tip_length_to_length_ratio=0.1,
				color=RED
			).put_start_and_end_on(start=[selectPCLeft[0]-0.8, selectPCTop[1]-0.4, 0], end=[selectPCLeft[0], selectPCTop[1]-0.4, 0]),
			Arrow( # val_a
				max_tip_length_to_length_ratio=0.1,
				color=BLUE
			).put_start_and_end_on(start=[selectPCLeft[0]-0.8, selectPCTop[1]-0.1, 0], end=[selectPCLeft[0], selectPCTop[1]-0.1, 0])
		]

		selectPCArrowsLabels = [
			CodeBlock("M_opcode", fontSize=16).next_to(selectPCArrows[0], LEFT, buff=0.08),
			CodeBlock("M_cond_val", fontSize=16).next_to(selectPCArrows[1], LEFT, buff=0.08),
			CodeBlock("seq_succ_PC", fontSize=16).next_to(selectPCArrows[2], LEFT, buff=0.08),
			CodeBlock("D_opcode", fontSize=16).next_to(selectPCArrows[3], LEFT, buff=0.08),
			CodeBlock("val_a", fontSize=16).next_to(selectPCArrows[4], LEFT, buff=0.08)
		]

		self.add(*selectPCArrows, *selectPCArrowsLabels)


		imemLeft = self.imem.get_left()
		imemRight = self.imem.get_right()
		imemTop = self.imem.get_top()

		predictPCLeft = self.predictPC.get_left()
		predictPCBottom = self.predictPC.get_bottom()

		dist = (imemLeft - selectPCRight)/2

		selectPC_imem = ArrowPath(
			selectPCRight, imemLeft,
			color=BLUE, strokeWidth=3
		).addPaths([
			[
				selectPCRight+dist, selectPCRight+dist+(DOWN*1.6), 
				[(imemRight+RIGHT*0.45)[0],(selectPCRight+dist+DOWN*1.6)[1],0],
				[(imemRight+RIGHT*0.45)[0],predictPCBottom[1]+0.15,0],
				[predictPCLeft[0], predictPCBottom[1]+0.15, 0]
			]
		]).markIntersections([2], RED)
		self.paths["selectPC_imem"] = selectPC_imem

		currPCLabel0 = CodeBlock("current_PC", fontSize=16).next_to(selectPC_imem.pathPoints[2], DOWN, buff=0.1)
		currPCLabel1 = CodeBlock("current_PC", fontSize=16).next_to(selectPC_imem.pathPoints[-1], UP, buff=0.08).shift(LEFT*0.5)
		self.add(currPCLabel0, currPCLabel1)


		extractOpcodeTop = self.extractOpcode.get_top()
		predictPCTop = self.predictPC.get_top()

		extractOpcode_predictPC = ArrowPath(
			extractOpcodeTop, extractOpcodeTop+UP*0.25,
			[(imemRight+RIGHT*0.8)[0], (extractOpcodeTop+UP*0.25)[1], 0], 
			[(imemRight+RIGHT*0.8)[0], predictPCTop[1]-0.15, 0], [predictPCLeft[0], predictPCTop[1]-0.15, 0],
			color=BLUE, strokeWidth=3
		).markIntersections([1], RED)
		self.paths["extractOpcode_predictPC"] = extractOpcode_predictPC

		opLabel = CodeBlock("op", fontSize=16).next_to(extractOpcode_predictPC.pathPoints[4], UP, buff=0.08).shift(LEFT*0.2)
		self.add(opLabel)


		extractOpcodeRight = self.extractOpcode.get_right()

		imem_extractOpcode_predictPC = ArrowPath(
			imemTop, 
			imemTop+UP*0.3, 
			[imemTop[0], extractOpcodeRight[1], 0], extractOpcodeRight,
			color=BLUE, strokeWidth=3
		).addPaths([
			[
				[imemTop[0], extractOpcodeRight[1], 0], [(imemRight+RIGHT*0.45)[0], extractOpcodeRight[1], 0],
				[(imemRight+RIGHT*0.45)[0], predictPCLeft[1], 0], [predictPCLeft[0], predictPCLeft[1]+0.01, 0]
			]
		]).markIntersections([1,2], RED)
		self.paths["imem_extractOpcode_predictPC"] = imem_extractOpcode_predictPC

		insnLabel0 = CodeBlock("insnbits", fontSize=16).next_to(imem_extractOpcode_predictPC.pathPoints[1], RIGHT, buff=0.1)
		insnLabel1 = CodeBlock("insnbits", fontSize=16).next_to(imem_extractOpcode_predictPC.pathPoints[-1], UP, buff=0.08).shift(LEFT*0.4)
		self.add(insnLabel0, insnLabel1)


		seqSuccLabel = CodeBlock("seq_succ", fontSize=16).next_to(predictPCTop, RIGHT, buff=0.1).shift(UP*0.2)
		predictedPCLabel = CodeBlock("predicted_PC", fontSize=16).next_to(self.predictPC, RIGHT, buff=0.1).shift(UP*0.2)
		self.add(seqSuccLabel, predictedPCLabel)

		self.add(*list(self.paths.values()))
