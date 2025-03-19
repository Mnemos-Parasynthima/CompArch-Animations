from sys import path
from pathlib import Path as libPath

path.append(str(libPath(__file__).resolve().parent.parent))

from animlib.pipeline import *
from animlib.mem import Instructions
from animlib.hexdec import CodeBlock

from manim import *
from manim.typing import Point3D


class PIPEScene(MovingCameraScene):
	def __init__(self, asmfile:str):
		super().__init__()

		self.paths:dict[str, Path] = {}

		self.fetchStage:FetchElements = FetchElements()
		self.decodeStage:DecodeElements = DecodeElements()
		self.executeStage:ExecuteElements = ExecuteElements()
		self.memoryStage:MemoryElements = MemoryElements()
		self.writebackStage:WritebackElements = WritebackElements()

		self.fetchPipeline:FetchPipeline = FetchPipeline()
		self.decodePipeline:DecodePipeline = DecodePipeline()
		self.executePipeline:ExecutePipeline = ExecutePipeline()
		self.memoryPipeline:MemoryPipeline = MemoryPipeline()
		self.writebackPipeline:WritebackPipeline = WritebackPipeline()

		self.instructions:Instructions = Instructions(asmfile)

	def createGlobalPaths(self):
		# Edges of the stages
		fetchTop = self.fetchStage.get_top()
		fetchBottom = self.fetchStage.get_bottom()
		fetchRight = self.fetchStage.get_right()
		
		# Top and bottoms for the pipeline register components
		predPCTop = self.fetchPipeline.components[3].get_top()
		predPCBottom = self.fetchPipeline.components[3].get_bottom()
		seqSuccPCTop = self.decodePipeline.components[3].get_top()
		seqSuccPCBottom = self.decodePipeline.components[3].get_bottom()
		insnbitsTop = self.decodePipeline.components[1].get_top()
		insnbitsBottom = self.decodePipeline.components[1].get_bottom()
		adrpValBottom = self.decodePipeline.components[4].get_bottom()
		opTop = self.decodePipeline.components[2].get_top()
		opBottom = self.decodePipeline.components[2].get_bottom()

		# Edges of each stage's components
		selectPCBottom = self.fetchStage.selectPC.get_bottom()
		predictPCTop = self.fetchStage.predictPC.get_top()
		predictPCRight = self.fetchStage.predictPC.get_right()


		# GLOBAL PATHS FOR FETCH
		predPC_selectPC = ArrowPath(
			predPCTop, [predPCTop[0], fetchBottom[1]+0.2, 0], [selectPCBottom[0], fetchBottom[1]+0.2, 0], selectPCBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["predPC_selectPC"] = predPC_selectPC

		predictPC_predPC = ArrowPath(
			predictPCRight, [fetchRight[0]+2.1, predictPCRight[1], 0], [fetchRight[0]+2.1, predPCBottom[1]-0.25, 0],
			[predPCBottom[0], predPCBottom[1]-0.25, 0], predPCBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["predictPC_predPC"] = predictPC_predPC

		predictPC_seqSuccPC = ArrowPath(
			predictPCTop, [predictPCTop[0], fetchTop[1]-0.05, 0], [seqSuccPCBottom[0], fetchTop[1]-0.05, 0], seqSuccPCBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["predictPC_seqSuccPC"] = predictPC_seqSuccPC

		imem_insnbits = ArrowPath(
			self.fetchStage.paths["imem_extractOpcode_predictPC"].pathPoints[1], 
			[(insnbitsBottom[0]), (self.fetchStage.paths["imem_extractOpcode_predictPC"].pathPoints[1])[1], 0], insnbitsBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["imem_insnbits"] = imem_insnbits

		selectPC_adrpVal = ArrowPath(
			self.fetchStage.paths["selectPC_imem"].pathPoints[2], [(self.fetchStage.paths["selectPC_imem"].pathPoints[2])[0], fetchTop[1]+0.1, 0],
			[adrpValBottom[0], fetchTop[1]+0.1, 0], adrpValBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["selectPC_adrpVal"] = selectPC_adrpVal

		extractOpcode_op = ArrowPath(
			self.fetchStage.paths["extractOpcode_predictPC"].pathPoints[1], [opBottom[0], (self.fetchStage.paths["extractOpcode_predictPC"].pathPoints[1])[1], 0],
			opBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["extractOpcode_op"] = extractOpcode_op
		

		# Edges for stage
		decodeTop = self.decodeStage.get_top()
		decodeBottom = self.decodeStage.get_bottom()

		# Top and bottoms
		opBottom = self.executePipeline.components[2].get_bottom()
		seqSuccPCBottom = self.executePipeline.components[3].get_bottom()
		valImmBottom = self.executePipeline.components[11].get_bottom()
		aluOpTop = self.executePipeline.components[7].get_top()
		aluOpBottom = self.executePipeline.components[7].get_bottom()
		xSigsTop = self.executePipeline.components[4].get_top()
		xSigsBottom = self.executePipeline.components[4].get_bottom()
		mSigsTop = self.executePipeline.components[5].get_top()
		mSigsBottom = self.executePipeline.components[5].get_bottom()
		wSigsTop = self.executePipeline.components[6].get_top()
		wSigsBottom = self.executePipeline.components[6].get_bottom()
		valATop = self.executePipeline.components[9].get_top()
		valABottom = self.executePipeline.components[9].get_bottom()
		valBTop = self.executePipeline.components[10].get_top()
		valBBotton = self.executePipeline.components[10].get_bottom()
		dstTop = self.executePipeline.components[-1].get_top()
		dstBottom = self.executePipeline.components[-1].get_bottom()
		hwTop = self.executePipeline.components[-2].get_top()
		hwBottom = self.executePipeline.components[-2].get_bottom()
		condTop = self.executePipeline.components[8].get_top()
		condBottom = self.executePipeline.components[8].get_bottom()

		# Edges of stage comps
		extractImmvalTop = self.decodeStage.extractImmval.get_top()
		extractImmvalBottom = self.decodeStage.extractImmval.get_bottom()
		decideALUOpTop = self.decodeStage.decideALUOp.get_top()
		decideALUOpLeft = self.decodeStage.decideALUOp.get_left()
		generateControlTop = self.decodeStage.generateControl.get_top()
		generateControlLeft = self.decodeStage.generateControl.get_left()
		forwardRegTop = self.decodeStage.forwardReg.get_top()
		forwardRegRight = self.decodeStage.forwardReg.get_right()


		# GLOBAL PATHS FOR DECODE
		seqSuccPC_seqSuccPC = ArrowPath(
			seqSuccPCTop, seqSuccPCBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["seqSuccPC_seqSuccPC"] = seqSuccPC_seqSuccPC

		extractImmval_valImm = ArrowPath(
			[valImmBottom[0], extractImmvalTop[1], 0], valImmBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["extractImmval_valImm"] = extractImmval_valImm

		decideALUOp_aluOp = ArrowPath(
			[aluOpBottom[0], decideALUOpTop[1], 0], aluOpBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["decideALUOp_aluOp"] = decideALUOp_aluOp

		generateControl_xSigs = ArrowPath(
			[xSigsBottom[0], generateControlTop[1], 0], xSigsBottom,
			color=RED, strokeWidth=3
		)
		self.paths["generateControl_xSigs"] = generateControl_xSigs

		generateControl_mSigs = ArrowPath(
			[mSigsBottom[0], generateControlTop[1], 0], mSigsBottom,
			color=RED, strokeWidth=3
		)
		self.paths["generateControl_mSigs"] = generateControl_mSigs

		generateControl_wSigs = ArrowPath(
			[wSigsBottom[0], generateControlTop[1], 0], wSigsBottom,
			color=RED, strokeWidth=3
		)
		self.paths["generateControl_wSigs"] = generateControl_wSigs

		forwardReg_valA = ArrowPath(
			[valABottom[0], forwardRegTop[1], 0], valABottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["forwardReg_valA"] = forwardReg_valA

		forwardReg_valB = ArrowPath(
			[valBBotton[0], forwardRegTop[1], 0], valBBotton,
			color=BLUE, strokeWidth=3
		)
		self.paths["forwardReg_valB"] = forwardReg_valB

		op_decide_ctrl_op = ArrowPath(
			opTop, opBottom,
			color=BLUE, strokeWidth=3
		).addPaths([
			[[opTop[0], decideALUOpLeft[1], 0], decideALUOpLeft],
			[[opTop[0], generateControlLeft[1], 0], generateControlLeft]
		]).markIntersections([2, 4], RED)
		self.paths["op_decide_ctrl_op"] = op_decide_ctrl_op

		insn_ = ArrowPath(
			insnbitsTop, [insnbitsTop[0], decodeBottom[1]+0.2, 0], [dstBottom[0], decodeBottom[1]+0.2, 0], dstBottom,
			color=BLUE, strokeWidth=3
		).addPaths([
			[[condBottom[0], decodeBottom[1]+0.2, 0], condBottom],
			[[extractImmvalBottom[0], decodeBottom[1]+0.2, 0], extractImmvalBottom],
			[[hwBottom[0], decodeBottom[1]+0.2, 0], hwBottom]
		]).markIntersections([4, 6, 8], RED)
		self.paths["insn_"] = insn_

	def intro(self):
		self.fetchPipeline.to_edge(DOWN).shift(RIGHT*2)
		self.decodePipeline.shift(DOWN*1.5).shift(RIGHT*2)
		self.executePipeline.shift(RIGHT*2)
		self.memoryPipeline.shift(UP*1.5).shift(RIGHT*2)
		self.writebackPipeline.to_edge(UP).shift(RIGHT*2)

		pcu = PipelineControlUnit(
			[self.fetchPipeline.get_bottom()[1], self.decodePipeline.get_bottom()[1], self.executePipeline.get_bottom()[1], 
				self.memoryPipeline.get_bottom()[1], self.writebackPipeline.get_bottom()[1]],
			[self.fetchPipeline.get_left()[0], self.decodePipeline.get_left()[0], self.executePipeline.get_left()[0], 
				self.memoryPipeline.get_left()[0], self.writebackPipeline.get_left()[0]]
		).to_edge(LEFT, buff=0.01)

		self.camera.frame.save_state()

		self.camera.frame.scale(1.2).shift(RIGHT)

		self.play(FadeIn(self.fetchPipeline, self.decodePipeline, self.executePipeline, self.memoryPipeline, self.writebackPipeline, pcu))

		arrowPaths = [
			ArrowPath(
				self.decodePipeline.components[2].get_top(), [self.decodePipeline.components[2].get_top()[0], self.decodePipeline.components[2].get_top()[1]+0.15, 0],
				[pcu.pcu.get_right()[0], self.decodePipeline.components[2].get_top()[1]+0.15, 0],
				color=BLUE, strokeWidth=3
			),
			Arrow(
				max_tip_length_to_length_ratio=0.1,
				stroke_width=3,
				color=BLUE
			).put_start_and_end_on(
				start=[self.decodePipeline.components[1].get_left()[0], self.decodePipeline.components[2].get_top()[1]+0.25, 0], 
				end=[pcu.pcu.get_right()[0], self.decodePipeline.components[2].get_top()[1]+0.25, 0]),
			CodeBlock("src1", fontSize=16.5).move_to([self.decodePipeline.components[1].get_left()[0]+0.25, self.decodePipeline.components[2].get_top()[1]+0.25, 0]),
			Arrow(
				max_tip_length_to_length_ratio=0.1,
				stroke_width=3,
				color=BLUE
			).put_start_and_end_on(
				start=[self.decodePipeline.components[1].get_left()[0], self.decodePipeline.components[2].get_top()[1]+0.4, 0], 
				end=[pcu.pcu.get_right()[0], self.decodePipeline.components[2].get_top()[1]+0.4, 0]),
			CodeBlock("src2", fontSize=16.5).move_to([self.decodePipeline.components[1].get_left()[0]+0.25, self.decodePipeline.components[2].get_top()[1]+0.4, 0]),

			ArrowPath(
				self.executePipeline.components[2].get_top(), [self.executePipeline.components[2].get_top()[0], self.executePipeline.components[2].get_top()[1]+0.15, 0],
				[pcu.pcu.get_right()[0], self.executePipeline.components[2].get_top()[1]+0.15, 0],
				color=BLUE, strokeWidth=3
			),
			ArrowPath(
				self.executePipeline.components[-1].get_top(), [self.executePipeline.components[-1].get_top()[0], self.executePipeline.components[-1].get_top()[1]+0.25, 0],
				[pcu.pcu.get_right()[0], self.executePipeline.components[-1].get_top()[1]+0.25, 0],
				color=BLUE, strokeWidth=3
			),
			ArrowPath(
				self.memoryPipeline.components[1].get_bottom(), [self.memoryPipeline.components[1].get_bottom()[0], self.memoryPipeline.components[1].get_bottom()[1]-0.15, 0],
				[pcu.pcu.get_right()[0], self.memoryPipeline.components[1].get_bottom()[1]-0.15, 0],
				color=BLUE, strokeWidth=3
			)
		]

		self.play(FadeIn(*arrowPaths))

		self.wait(1)

		self.play(FadeOut(*arrowPaths, pcu, self.fetchPipeline, self.decodePipeline, self.executePipeline, self.memoryPipeline, self.writebackPipeline))
		self.camera.frame.restore()

	def pipeline(self):
		self.fetchPipeline.to_edge(DOWN).shift(LEFT*2)
		self.decodePipeline.to_edge(UP).shift(LEFT*2)
		self.decodeStage.move_to(self.decodePipeline).shift(UP*3)
		self.executePipeline.move_to(self.decodeStage).shift(UP*3)
		self.executeStage.move_to(self.executePipeline).shift(UP*3)
		self.memoryPipeline.move_to(self.executeStage).shift(UP*2.75)
		self.memoryStage.move_to(self.memoryPipeline).shift(UP*2.25)
		self.writebackPipeline.move_to(self.memoryStage).shift(UP*2.2)
		self.writebackStage.move_to(self.writebackPipeline).shift(UP*1.45)

		self.createGlobalPaths()

		self.play(FadeIn(
			self.fetchPipeline, self.fetchStage, 
			self.decodePipeline, self.decodeStage,
			self.executePipeline, self.executeStage,
			self.memoryPipeline, self.memoryStage,
			self.writebackPipeline, self.writebackStage
		))

		self.play(self.camera.frame.animate.move_to(self.decodeStage))
		self.play(self.camera.frame.animate.move_to(self.executeStage))
		self.play(self.camera.frame.animate.move_to(self.memoryStage).shift(UP))

	def construct(self):
		self.intro()

		self.wait(1)

		self.pipeline()

		self.wait(2)