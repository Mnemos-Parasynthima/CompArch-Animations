from sys import path
from pathlib import Path as libPath

path.append(str(libPath(__file__).resolve().parent.parent))

from animlib.pipeline import *
from animlib.mem import Instructions
from animlib.hexdec import CodeBlock

from manim import *
from manim.typing import Point3D


class PIPEScene(MovingCameraScene):
	def __init__(self, asmfile:str="asm-stripped.s"):
		super().__init__()

		self.paths:dict[str, ArrowPath] = {}

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
		decodeBottom = self.decodeStage.get_bottom()

		# Top and bottoms
		opBottom = self.executePipeline.components[2].get_bottom()
		seqSuccPCBottom = self.executePipeline.components[3].get_bottom()
		valImmTop = self.executePipeline.components[11].get_top()
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
		valBBottom = self.executePipeline.components[10].get_bottom()
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


		# GLOBAL PATHS FOR DECODE
		seqSuccPC_seqSuccPC = ArrowPath(
			seqSuccPCTop, seqSuccPCBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["seqSuccPC_Decode_seqSuccPC"] = seqSuccPC_seqSuccPC

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
			[valBBottom[0], forwardRegTop[1], 0], valBBottom,
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


		# Edges for stage
		executeBottom = self.executeStage.get_bottom()

		# Top and bottom
		seqSuccPCTop = self.executePipeline.components[3].get_top()
		seqSuccPCBottom = self.memoryPipeline.components[3].get_bottom()
		mSigsBottom = self.memoryPipeline.components[5].get_bottom()
		wSigsBottom = self.memoryPipeline.components[6].get_bottom()
		dstBottom = self.memoryPipeline.components[-1].get_bottom()
		valBBottom = self.memoryPipeline.components[10].get_bottom()
		valExTop = self.memoryPipeline.components[9].get_top()
		valExBottom = self.memoryPipeline.components[9].get_bottom()
		condholdsTop = self.memoryPipeline.components[1].get_top()
		condholdsBottom = self.memoryPipeline.components[1].get_bottom()

		# Edges of stage comps
		aluLeft = self.executeStage.alu.get_left()
		aluTop = self.executeStage.alu.get_top()
		aluBottom = self.executeStage.alu.get_bottom()
		muxBottom = self.executeStage.mux.get_bottom()
		muxRight = self.executeStage.mux.get_right()


		# GLOBAL PATHS FOR EXECUTE
		seqSuccPC_seqSuccPC = ArrowPath(
			seqSuccPCTop, seqSuccPCBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["seqSuccPC_Execute_seqSuccPC"] = seqSuccPC_seqSuccPC

		mSigs_mSigs = ArrowPath(
			mSigsTop, mSigsBottom,
			color=RED, strokeWidth=3
		)
		self.paths["mSigs_Execute_mSigs"] = mSigs_mSigs

		wSigs_wSigs = ArrowPath(
			wSigsTop, wSigsBottom,
			color=RED, strokeWidth=3
		)
		self.paths["wSigs_Execute_wSigs"] = wSigs_wSigs

		dst_dst = ArrowPath(
			dstTop, dstBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["dst_Execute_dst"] = dst_dst

		valA_alu = ArrowPath(
			valATop, aluBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["valuA_alu"] = valA_alu

		valB_mux = ArrowPath(
			valBTop, [valBTop[0], muxBottom[1], 0],
			color=BLUE, strokeWidth=3
		).addPaths([
			[[valBTop[0], executeBottom[1]+0.2, 0], [muxRight[0]+0.2, executeBottom[1]+0.2, 0],
				[muxRight[0]+0.2, aluTop[1]+0.2, 0], [valBBottom[0], aluTop[1]+0.2, 0], valBBottom
			]
		]).markIntersections([2], RED)
		self.paths["valB_mux"] = valB_mux

		valImm_mux = ArrowPath(
			valImmTop, [valImmTop[0], muxBottom[1], 0],
			color=BLUE, strokeWidth=3
		)
		self.paths["valImm_mux"] = valImm_mux

		hw_alu = ArrowPath(
			hwTop, [hwTop[0], aluBottom[1]+0.2, 0], [self.executeStage.alu.get_right()[0], aluBottom[1]+0.2, 0],
			color=BLUE, strokeWidth=3
		)
		self.paths["hw_alu"] = hw_alu

		alu_valEx = ArrowPath(
			aluTop, valExBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["alu_valEx"] = alu_valEx

		alu_condholds = ArrowPath(
			aluLeft, [condholdsBottom[0], aluLeft[1], 0], condholdsBottom,
			color=RED, strokeWidth=3
		)
		self.paths["alu_condholds"] = alu_condholds

		cond_alu = ArrowPath(
			condTop, [condTop[0], muxBottom[1]-0.4, 0], [aluLeft[0]+0.4, muxBottom[1]-0.4, 0], [aluLeft[0]+0.4, aluBottom[1], 0],
			color=RED, strokeWidth=3
		)
		self.paths["cond_alu"] = cond_alu

		aluOp_alu = ArrowPath(
			aluOpTop, [aluOpTop[0], muxBottom[1], 0], [aluLeft[0]+0.2, muxBottom[1], 0], [aluLeft[0]+0.2, aluBottom[1], 0],
			color=RED, strokeWidth=3
		)
		self.paths["aluOp_alu"] = aluOp_alu

		xSigsArrow1 = ArrowPath(xSigsTop+LEFT*0.2, xSigsTop+UP*0.8+LEFT*0.2, color=RED, strokeWidth=3)
		self.paths["xSigsArrow1"] = xSigsArrow1

		xSigsArrow2 = ArrowPath(xSigsTop+RIGHT*0.2, xSigsTop+UP*0.8+RIGHT*0.2, color=RED, strokeWidth=3)
		self.paths["xSigsArrow2"] = xSigsArrow2


		# Edges for stage
		memoryBottom = self.memoryStage.get_bottom()

		# Top and bottom
		dstTop = self.memoryPipeline.components[-1].get_top()
		wSigsTop = self.memoryPipeline.components[6].get_top()
		valBTop = self.memoryPipeline.components[10].get_top()
		mSigsTop = self.memoryPipeline.components[5].get_top()
		wSigsBottom = self.writebackPipeline.components[6].get_bottom()
		dstBottom = self.writebackPipeline.components[-1].get_bottom()
		valExBottom = self.writebackPipeline.components[9].get_bottom()
		valMemTop = self.writebackPipeline.components[11].get_top()
		valMemBottom = self.writebackPipeline.components[11].get_bottom()

		# Edges of stage comps
		dmemLeft = self.memoryStage.dmem.get_left()
		dmemTop = self.memoryStage.dmem.get_top()
		dmemBottom = self.memoryStage.dmem.get_bottom()


		# GLOBAL PATHS FOR MEMORY
		dst_dst = ArrowPath(
			dstTop, dstBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["dst_Memory_dst"] = dst_dst

		valEx_valEx = ArrowPath(
			valExTop, valExBottom,
			color=BLUE, strokeWidth=3
		).addPaths([
			[[valExTop[0], dmemLeft[1], 0], dmemLeft]
		]).markIntersections([2], RED)
		self.paths["valEx_valEx"] = valEx_valEx

		wSigs_wSigs = ArrowPath(
			wSigsTop, wSigsBottom,
			color=RED, strokeWidth=3
		)
		self.paths["wSigs_Memory_wSigs"] = wSigs_wSigs

		valB_dmem = ArrowPath(
			valBTop, [valBTop[0], memoryBottom[1]+0.4, 0], [dmemBottom[0], memoryBottom[1]+0.4, 0], dmemBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["valB_dmem"] = valB_dmem

		dmem_valMem = ArrowPath(
			dmemTop, valMemBottom,
			color=BLUE, strokeWidth=3
		)
		self.paths["dmem_valMem"] = dmem_valMem

		mSigsArrow1 = ArrowPath([mSigsTop[0]-0.2, mSigsTop[1], 0], [mSigsTop[0]-0.2, memoryBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["mSigsArrow1"] = mSigsArrow1

		mSigsArrow2 = ArrowPath([mSigsTop[0]+0.2, mSigsTop[1], 0], [mSigsTop[0]+0.2, memoryBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["mSigsArrow2"] = mSigsArrow2


		# Edges for stage
		writebackBottom = self.writebackStage.get_bottom()

		# Top and bottom
		wSigsTop = self.writebackPipeline.components[6].get_top()
		valExTop = self.writebackPipeline.components[9].get_top()

		# Edges of stage comps
		muxBottom = self.writebackStage.mux.get_bottom()


		# GLOBAL PATHS FOR WRITEBACK
		valEx_mux = ArrowPath(
			valExTop, [valExTop[0], muxBottom[1], 0],
			color=BLUE, strokeWidth=3
		)
		self.paths["valEx_mux"] = valEx_mux

		valMem_mux = ArrowPath(
			valMemTop, [valMemTop[0], muxBottom[1], 0],
			color=BLUE, strokeWidth=3
		)
		self.paths["valMem_mux"] = valMem_mux

		wSigsArrow1 = ArrowPath([wSigsTop[0]-0.2, wSigsTop[1], 0], [wSigsTop[0]-0.2, writebackBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["wSigsArrow1"] = wSigsArrow1

		wSigsArrow2 = ArrowPath([wSigsTop[0], wSigsTop[1], 0], [wSigsTop[0], writebackBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["wSigsArrow2"] = wSigsArrow2

		wSigsArrow3 = ArrowPath([wSigsTop[0]+0.2, wSigsTop[1], 0], [wSigsTop[0]+0.2, writebackBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["wSigsArrow3"] = wSigsArrow3



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
		self.fetchPipeline.to_edge(DOWN)#.shift(LEFT*2)
		self.decodePipeline.to_edge(UP)#.shift(LEFT*2)
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
			self.writebackPipeline, self.writebackStage,
			*list(self.paths.values())
		))

		# self.play(self.camera.frame.animate.move_to(self.decodeStage))
		# self.play(self.camera.frame.animate.move_to(self.executeStage))
		self.play(self.camera.frame.animate.move_to(self.memoryStage).shift(UP))

	def construct(self):
		# self.intro()

		# self.wait(1)

		self.pipeline()

		self.wait(2)