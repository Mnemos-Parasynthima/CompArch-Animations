from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Rectangle, Arrow, ORANGE, PURPLE
from .core import Stage, Register
from .PC import PC
from .IMem import IMem
from .logic import Adder, Mux
from .Path import Path, ArrowPath
from ..hexdec import CodeBlock


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
			).put_start_and_end_on(start=[selectPCLeft[0]-1, selectPCBottom[1]+0.1, 0], end=[selectPCLeft[0], selectPCBottom[1]+0.1, 0]),
			Arrow( # M_cond_val
				max_tip_length_to_length_ratio=0.1,
				color=RED
			).put_start_and_end_on(start=[selectPCLeft[0]-1, selectPCBottom[1]+0.4, 0], end=[selectPCLeft[0], selectPCBottom[1]+0.4, 0]),
			Arrow( # seq_succ_PC
				max_tip_length_to_length_ratio=0.1,
				color=BLUE
			).put_start_and_end_on(start=[selectPCLeft[0]-1, selectPCCenter[1], 0], end=[selectPCLeft[0], selectPCCenter[1], 0]),
			Arrow( # D_opcode
				max_tip_length_to_length_ratio=0.1,
				color=RED
			).put_start_and_end_on(start=[selectPCLeft[0]-1, selectPCTop[1]-0.4, 0], end=[selectPCLeft[0], selectPCTop[1]-0.4, 0]),
			Arrow( # val_a
				max_tip_length_to_length_ratio=0.1,
				color=BLUE
			).put_start_and_end_on(start=[selectPCLeft[0]-1, selectPCTop[1]-0.1, 0], end=[selectPCLeft[0], selectPCTop[1]-0.1, 0])
		]

		self.add(*selectPCArrows)

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
				[(imemRight+RIGHT*0.6)[0],(selectPCRight+dist+DOWN*1.6)[1],0],
				[(imemRight+RIGHT*0.6)[0],predictPCBottom[1]+0.2,0],
				[predictPCLeft[0], predictPCBottom[1]+0.2, 0]
			]
		]).markIntersections([2], RED)
		self.paths["selectPC_imem"] = selectPC_imem

		extractOpcodeRight = self.extractOpcode.get_right()

		# print(imemTop, imemTop+UP*0.3, [imemTop[0], extractOpcodeRight[1], 0], extractOpcodeRight)

		imem_extractOpcode_predictPC = ArrowPath(
			imemTop, imemTop+UP*0.3, [imemTop[0], extractOpcodeRight[1], 0], extractOpcodeRight,
			color=BLUE, strokeWidth=3
		).addPaths([
			[
				[imemTop[0], extractOpcodeRight[1], 0], [(imemRight+RIGHT*0.6)[0], extractOpcodeRight[1], 0],
				[(imemRight+RIGHT*0.6)[0], predictPCLeft[1], 0], predictPCLeft
			]
		]).markIntersections([1,2], RED)
		self.paths["imem_extractOpcode_predictPC"] = imem_extractOpcode_predictPC

		# print(imem_extractOpcode_predictPC.intersections[1].get_center(), imem_extractOpcode_predictPC.pathPoints[-4])

		self.add(*list(self.paths.values()))
