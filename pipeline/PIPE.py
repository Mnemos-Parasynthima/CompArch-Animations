from sys import path
from pathlib import Path as libPath

path.append(str(libPath(__file__).resolve().parent.parent))

from animlib.pipeline import *
# from animlib.mem import Instructions
from animlib.hexdec import CodeBlock

from manim import *


class PIPEScene(MovingCameraScene):
	CLOCK_RUNTIME = 0.75
	STAGE_RUNTIME = 0.5
	STAGE_SLOW_RUNTIME = 0.7

	def __init__(self, asmfile:str="add.s"):
		super().__init__()

		self.paths:dict[str, ArrowPath] = {}
		self.pathLabels:dict[str, CodeBlock] = {}

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

		# Considering the difficulty of incorporating SE into this, add.s is very much hardcoded
		# TODO: Incorporate SE
		# Thinking about it, it may not be that difficult, regarding the api and its calls
		# Maybe just run all 5 stages first then interact with the outputs
		# However, the structure may need to be different than what libse and libapi offers
		# Considering the many different inputs needed to animate, the api would need to expose more data
		# The api would also need to work with the pipeline control register
		# And hazards/forwarding is also a thing now
		# asmfile = "./assembly/" + asmfile
		# self.instructions:Instructions = Instructions(asmfile)

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

		forwardRegRight = self.decodeStage.forwardReg.get_right()

		forwardRegInputsArrow = ArrowPath(
			[self.decodeStage.submobjects[0].get_right()[0]+1.5, forwardRegRight[1], 0], forwardRegRight,
			strokeWidth=16, color=WHITE
		)
		self.paths["forwardRegInputs"] = forwardRegInputsArrow


		# Edges for stage
		executeBottom = self.executeStage.get_bottom()

		# Top and bottom
		opTop = self.executePipeline.components[2].get_top()
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
		self.paths["valA_alu"] = valA_alu

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

		DopcodeArrow = ArrowPath(opTop, opTop+UP*0.8, color=RED, strokeWidth=3)
		self.paths["DopcodeArrow"] = DopcodeArrow
		DopcodeLabel = CodeBlock("Dopcode", fontSize=16).next_to(DopcodeArrow, RIGHT, buff=0.1)
		self.pathLabels["Dopcode"] = DopcodeLabel

		xSigsArrow1 = ArrowPath(xSigsTop+LEFT*0.2, xSigsTop+UP*0.8+LEFT*0.2, color=RED, strokeWidth=3)
		self.paths["xSigsArrow1"] = xSigsArrow1
		valbSelLabel = CodeBlock("valb_sel", fontSize=16).next_to(xSigsArrow1, LEFT, buff=0.0)#.rotate(PI/2)
		self.pathLabels["valbSel"] = valbSelLabel

		xSigsArrow2 = ArrowPath(xSigsTop+RIGHT*0.2, xSigsTop+UP*0.8+RIGHT*0.2, color=RED, strokeWidth=3)
		self.paths["xSigsArrow2"] = xSigsArrow2
		setCCLabel = CodeBlock("set_CC", fontSize=16).next_to(xSigsArrow2, RIGHT, buff=0.0)#.rotate(-PI/2)
		self.pathLabels["setCC"] = setCCLabel


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

		condholdsArrow = ArrowPath(condholdsTop, [condholdsTop[0], memoryBottom[1]+0.4, 0], color=BLUE, strokeWidth=3)
		self.paths["condholdsArrow"] = condholdsArrow
		condholdsLabel = CodeBlock("M_cond_val", fontSize=16).next_to(condholdsArrow, UP, buff=0.1)
		self.pathLabels["condholds"] = condholdsLabel

		mSigsArrow1 = ArrowPath([mSigsTop[0]-0.2, mSigsTop[1], 0], [mSigsTop[0]-0.2, memoryBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["mSigsArrow1"] = mSigsArrow1
		dmemWriteLabel = CodeBlock("dmem_write", fontSize=16).next_to(mSigsArrow1, LEFT, buff=0.1)
		self.pathLabels["dmemWrite"] = dmemWriteLabel

		mSigsArrow2 = ArrowPath([mSigsTop[0]+0.2, mSigsTop[1], 0], [mSigsTop[0]+0.2, memoryBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["mSigsArrow2"] = mSigsArrow2
		dmemReadLabel = CodeBlock("dmem_read", fontSize=16).next_to(mSigsArrow2, RIGHT, buff=0.1)
		self.pathLabels["dmemRead"] = dmemReadLabel


		# Edges for stage
		writebackBottom = self.writebackStage.get_bottom()

		# Top and bottom
		wSigsTop = self.writebackPipeline.components[6].get_top()
		valExTop = self.writebackPipeline.components[9].get_top()
		dstTop = self.writebackPipeline.components[-1].get_top()

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
		# dstSelLabel = CodeBlock("dst_sel")

		wSigsArrow2 = ArrowPath([wSigsTop[0], wSigsTop[1], 0], [wSigsTop[0], writebackBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["wSigsArrow2"] = wSigsArrow2
		wvalSelLabel = CodeBlock("wval_sel", fontSize=16).next_to(wSigsArrow2, UP, buff=0.1)
		self.pathLabels["wvalSel"] = wvalSelLabel

		wSigsArrow3 = ArrowPath([wSigsTop[0]+0.2, wSigsTop[1], 0], [wSigsTop[0]+0.2, writebackBottom[1]+0.4, 0], color=RED, strokeWidth=3)
		self.paths["wSigsArrow3"] = wSigsArrow3
		WwenableLabel = CodeBlock("W_w_enable", fontSize=16).next_to(wSigsArrow3, RIGHT, buff=0.1)
		self.pathLabels["Wwenable"] = WwenableLabel

		dst = ArrowPath(dstTop, [dstTop[0], writebackBottom[1], 0], [dstTop[0]+2, writebackBottom[1], 0], color=BLUE, strokeWidth=3)
		self.paths["dst"] = dst
		WdstLabel = CodeBlock("W_dst", fontSize=16).next_to(dst, UP, buff=0.1)
		self.pathLabels["Wdst"] = WdstLabel

	def intro(self):
		self.fetchPipeline.to_edge(DOWN).shift(RIGHT*2)
		self.decodePipeline.shift(DOWN*1.5).shift(RIGHT*2)
		self.executePipeline.shift(RIGHT*2)
		self.memoryPipeline.shift(UP*1.5).shift(RIGHT*2)
		self.writebackPipeline.to_edge(UP).shift(RIGHT*2)

		self.pcu = PipelineControlUnit().to_edge(LEFT, buff=0.01)
		self.pcu.addArrows(
			[self.fetchPipeline.get_bottom()[1], self.decodePipeline.get_bottom()[1], self.executePipeline.get_bottom()[1], 
				self.memoryPipeline.get_bottom()[1], self.writebackPipeline.get_bottom()[1]],
			[self.fetchPipeline.get_left()[0], self.decodePipeline.get_left()[0], self.executePipeline.get_left()[0], 
				self.memoryPipeline.get_left()[0], self.writebackPipeline.get_left()[0]]
		)

		self.camera.frame.save_state()

		self.camera.frame.scale(1.2).shift(RIGHT)

		self.play(FadeIn(self.fetchPipeline, self.decodePipeline, self.executePipeline, self.memoryPipeline, self.writebackPipeline, self.pcu))

		arrowPaths = [
			ArrowPath(
				self.decodePipeline.components[2].get_top(), [self.decodePipeline.components[2].get_top()[0], self.decodePipeline.components[2].get_top()[1]+0.15, 0],
				[self.pcu.pcu.get_right()[0], self.decodePipeline.components[2].get_top()[1]+0.15, 0],
				color=BLUE, strokeWidth=3
			),
			Arrow(
				max_tip_length_to_length_ratio=0.1,
				stroke_width=3,
				color=BLUE
			).put_start_and_end_on(
				start=[self.decodePipeline.components[1].get_left()[0], self.decodePipeline.components[2].get_top()[1]+0.25, 0], 
				end=[self.pcu.pcu.get_right()[0], self.decodePipeline.components[2].get_top()[1]+0.25, 0]),
			CodeBlock("src1", fontSize=16.5).move_to([self.decodePipeline.components[1].get_left()[0]+0.25, self.decodePipeline.components[2].get_top()[1]+0.25, 0]),
			Arrow(
				max_tip_length_to_length_ratio=0.1,
				stroke_width=3,
				color=BLUE
			).put_start_and_end_on(
				start=[self.decodePipeline.components[1].get_left()[0], self.decodePipeline.components[2].get_top()[1]+0.4, 0], 
				end=[self.pcu.pcu.get_right()[0], self.decodePipeline.components[2].get_top()[1]+0.4, 0]),
			CodeBlock("src2", fontSize=16.5).move_to([self.decodePipeline.components[1].get_left()[0]+0.25, self.decodePipeline.components[2].get_top()[1]+0.4, 0]),

			ArrowPath(
				self.executePipeline.components[2].get_top(), [self.executePipeline.components[2].get_top()[0], self.executePipeline.components[2].get_top()[1]+0.15, 0],
				[self.pcu.pcu.get_right()[0], self.executePipeline.components[2].get_top()[1]+0.15, 0],
				color=BLUE, strokeWidth=3
			),
			ArrowPath(
				self.executePipeline.components[-1].get_top(), [self.executePipeline.components[-1].get_top()[0], self.executePipeline.components[-1].get_top()[1]+0.25, 0],
				[self.pcu.pcu.get_right()[0], self.executePipeline.components[-1].get_top()[1]+0.25, 0],
				color=BLUE, strokeWidth=3
			),
			ArrowPath(
				self.memoryPipeline.components[1].get_bottom(), [self.memoryPipeline.components[1].get_bottom()[0], self.memoryPipeline.components[1].get_bottom()[1]-0.15, 0],
				[self.pcu.pcu.get_right()[0], self.memoryPipeline.components[1].get_bottom()[1]-0.15, 0],
				color=BLUE, strokeWidth=3
			)
		]

		self.play(FadeIn(*arrowPaths))

		self.wait(1)

		self.play(FadeOut(*arrowPaths, self.pcu, self.fetchPipeline, self.decodePipeline, self.executePipeline, self.memoryPipeline, self.writebackPipeline))
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

		self.pcu = PipelineControlUnit(
			height=25
		).to_edge(LEFT).shift(LEFT*3.5 + UP*8.5)
		self.pcu.addArrows(
			[self.fetchPipeline.get_bottom()[1], self.decodePipeline.get_bottom()[1], self.executePipeline.get_bottom()[1], 
				self.memoryPipeline.get_bottom()[1], self.writebackPipeline.get_bottom()[1]],
			[self.fetchPipeline.get_left()[0], self.decodePipeline.get_left()[0], self.executePipeline.get_left()[0], 
				self.memoryPipeline.get_left()[0], self.writebackPipeline.get_left()[0]]
		)

		self.camera.frame.save_state()
		self.play(self.camera.frame.animate.move_to(self.decodeStage).scale(3.2).shift(UP*2.75))

		self.play(FadeIn(
			self.fetchPipeline, self.fetchStage,
			self.decodePipeline, self.decodeStage,
			self.executePipeline, self.executeStage,
			self.memoryPipeline, self.memoryStage,
			self.writebackPipeline, self.writebackStage,
			self.pcu,
			*list(self.paths.values()),
			*list(self.pathLabels.values())
		))

		self.play(
			self.fetchStage.animateInstruction("add x0, x0, #1"),
			self.decodeStage.animateInstruction("-"),
			self.executeStage.animateInstruction("-"),
			self.memoryStage.animateInstruction("-"),
			self.writebackStage.animateInstruction("-")
		)

		self.play(self.camera.frame.animate.restore())

		# Cycle 0
		self.play(self.fetchPipeline.animateFout("0x400110"))

		# Fetch Ops
		self.play(self.fetchStage.animateSelectPC("0x0", "OP_NOP", "0x0", "F", "OP_NOP", "0x400110"))
		self.play(self.fetchStage.animateImemExtract("0x91000400", "OP_ADD"))
		self.play(self.fetchStage.animatePredictPC("OP_ADD", "0x400110", "0x400114", "0x400114"))

		self.play(self.decodePipeline.animateDin("0x91000400", "OP_ADD", "0x400114", "0x0"))
		self.play(self.camera.frame.animate.move_to(self.decodeStage))
		# Dout vals are different than Din (after the initial cycle)
		self.play(self.decodePipeline.animateDout("0x0", "OP_NOP", "0x0", "0x0"))

		# Decode Ops
		self.play(self.decodeStage.animateGenerateSigs("OP_NOP"))
		self.play(self.decodeStage.animateExtract("0x0", "0x0"))
		self.play(self.decodeStage.animateDecideALU("OP_NOP", "PASS_OP"))
		self.play(self.decodeStage.animateRegfile("0", "0", "0", "0x0", False, "0x0", "0x0"))
		self.play(self.decodeStage.animateForward("0x0", "0x0", self.paths))

		self.play(self.executePipeline.animateXin("OP_NOP", "0x0", "PASS_OP", "EQ", "0x0", "0x0", "0x0", "0x0", "0"))
		self.play(self.camera.frame.animate.move_to(self.executeStage))
		# Xout vals are different than Xin (after the initial cycle)
		self.play(self.executePipeline.animateXout("OP_NOP", "0x0", "PLUS_OP", "EQ", "0x0", "0x0", "0x0", "0x0", "0"))

		# Execute Ops
		self.play(self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths))
		self.play(self.executeStage.animateALU("0x0", "0x0", "0x0", "PLUS_OP", "EQ", "T", "0x0", self.paths))

		self.play(self.memoryPipeline.animateMin("T", "0x0", "0x0", "0x0", "0"))
		self.play(self.camera.frame.animate.move_to(self.memoryStage).shift(UP))
		# Mout vals are different than Min (after the initial cycle)
		self.play(self.memoryPipeline.animateMout("F", "0x0", "0x0", "0x0", "0"))

		# Memory Ops
		self.play(self.memoryStage.animateDmem("0x0", "0x0", "0x0"))

		self.play(self.writebackPipeline.animateWin("0x0", "0x0", "0"))
		# Wout vals are different than Win (after the initial cycle)
		self.play(self.writebackPipeline.animateWout("0x0", "0x0", "0"))

		# Writeback Ops
		self.play(self.writebackStage.animateMux("0x0", "0x0", "0x0", self.paths))

		# Zoom out for Pipe clocks
		self.play(self.camera.frame.animate.move_to(self.decodeStage).scale(3.2).shift(UP*2.75))


		self.play(self.fetchPipeline.animateFin("0x400114"))


		self.play(self.fetchPipeline.animateClock(), run_time=self.CLOCK_RUNTIME)
		self.play(self.decodePipeline.animateClock(), run_time=self.CLOCK_RUNTIME)
		self.play(self.executePipeline.animateClock(), run_time=self.CLOCK_RUNTIME)
		self.play(self.memoryPipeline.animateClock(), run_time=self.CLOCK_RUNTIME)
		self.play(self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME)
		# End of cycle

		self.play(
			self.fetchStage.animateInstruction("add x1, x1, #0xfff"),
			self.decodeStage.animateInstruction("add x0, x0, #1"),
			self.executeStage.animateInstruction("-"),
			self.memoryStage.animateInstruction("-"),
			self.writebackStage.animateInstruction("-")
		)
		self.play(self.camera.frame.animate.restore())
		self.cycle1()
		self.play(
			self.fetchStage.animateInstruction("nop"),
			self.decodeStage.animateInstruction("add x1, x1, #0xfff"),
			self.executeStage.animateInstruction("add x0, x0, #1"),
			self.memoryStage.animateInstruction("-"),
			self.writebackStage.animateInstruction("-")
		)
		self.play(self.camera.frame.animate.restore())
		self.cycle2()
		# Starting from cycle3, it will be kept in a global view
		self.cycle3()
		self.cycle4()
		self.cycle5()
		self.cycle6()
		self.cycle7()
		self.cycle8()
		self.cycle9()
		self.cycle10()
		self.cycle11()
		self.cycle12()

	def cycle1(self):
		# Fetch Ops
		self.play(
			self.fetchStage.animateSelectPC("0x0", "OP_NOP", "0x0", "T", "OP_NOP", "0x400114"),
			self.fetchStage.animateImemExtract("0x913ffc21", "OP_ADD"),
			self.fetchStage.animatePredictPC("OP_ADD", "0x400114", "0x400118", "0x400118"), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		self.play(
			self.decodePipeline.animateDin("0x91000400", "OP_ADD", "0x400114", "0x0"),
			self.camera.frame.animate.move_to(self.decodeStage), 
			run_time=self.STAGE_SLOW_RUNTIME
		)
		# animateDout is already taken care of in Clock()

		# Decode Ops
		self.play(self.decodeStage.animateGenerateSigs("OP_ADD"),
			self.decodeStage.animateExtract("0x91000400", "0x1"),
			self.decodeStage.animateDecideALU("OP_ADD", "PLUS_OP"),
			self.decodeStage.animateRegfile("0", "0", "0", "0x0", False, "0x0", "0x0"),
			self.decodeStage.animateForward("0x0", "0x0", self.paths), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		self.play(
			self.executePipeline.animateXin("OP_ADD", "0x400114", "PLUS_OP", "EQ", "0x0", "0x0", "0x1", "0x0", "0"),
			self.camera.frame.animate.move_to(self.executeStage), 
			run_time=self.STAGE_SLOW_RUNTIME
		)
		# animateXout is already taken care of in Clock()

		# Execute Ops
		self.play(
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x0", "0x0", "0x0", "PASS_OP", "EQ", "T", "0x0", self.paths), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		self.play(
			self.memoryPipeline.animateMin("T", "0x0", "0x0", "0x0", "0"),
			self.camera.frame.animate.move_to(self.memoryStage).shift(UP), 
			run_time=self.STAGE_SLOW_RUNTIME
		)
		# animateMout 0xis already taken 0xcare of in Clock()

		# Memory Ops
		self.play(self.memoryStage.animateDmem("0x0", "0x0", "0x0"), run_time=self.STAGE_SLOW_RUNTIME)

		self.play(self.writebackPipeline.animateWin("0x0", "0x0", "0"), run_time=self.STAGE_SLOW_RUNTIME)
		# animateWout is already taken care of in Clock()

		# Writeback Ops
		self.play(self.writebackStage.animateMux("0x0", "0x0", "0x0", self.paths), run_time=self.STAGE_SLOW_RUNTIME)

		# Zoom out for Pipe clocks
		self.play(self.camera.frame.animate.move_to(self.decodeStage).scale(3.2).shift(UP*2.75), run_time=self.STAGE_SLOW_RUNTIME)


		self.play(self.fetchPipeline.animateFin("0x400118"), run_time=self.STAGE_SLOW_RUNTIME)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle2(self):
		# Fetch Ops
		self.play(
			self.fetchStage.animateSelectPC("0x0", "OP_ADD", "0x0", "T", "OP_NOP", "0x400118"),
			self.fetchStage.animateImemExtract("0xd503201f", "OP_NOP"),
			self.fetchStage.animatePredictPC("OP_NOP", "0x400118", "0x40011c", "0x40011c"), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		self.play(
			self.decodePipeline.animateDin("0xd503201f", "OP_NOP", "0x40011c", "0x0"),
			self.camera.frame.animate.move_to(self.decodeStage), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		# Decode Ops
		self.play(
			self.decodeStage.animateGenerateSigs("OP_ADD"),
			self.decodeStage.animateExtract("0x913ffc21", "0xfff"),
			self.decodeStage.animateDecideALU("OP_ADD", "PLUS_OP"),
			self.decodeStage.animateRegfile("1", "1", "0", "0x0", False, "0x0", "0x0"),
			self.decodeStage.animateForward("0x0", "0x0", self.paths), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		self.play(
			self.executePipeline.animateXin("OP_ADD", "0x400118", "PLUS_OP", "EQ", "0x0", "0x0", "0xfff", "0x0", "1"),
			self.camera.frame.animate.move_to(self.executeStage), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		# Execute Ops
		self.play(
			self.executeStage.animateMux("0x0", "0x1", "0x1", self.paths),
			self.executeStage.animateALU("0x0", "0x1", "0x0", "PLUS_OP", "EQ", "T", "0x1", self.paths), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		self.play(
			self.memoryPipeline.animateMin("T", "0x400114", "0x1", "0x0", "0"),
			self.camera.frame.animate.move_to(self.memoryStage).shift(UP), 
			run_time=self.STAGE_SLOW_RUNTIME
		)

		# Memory Ops
		self.play(self.memoryStage.animateDmem("0x0", "0x0", "0x0"), run_time=self.STAGE_SLOW_RUNTIME)

		self.play(self.writebackPipeline.animateWin("0x0", "0x0", "0"), run_time=self.STAGE_SLOW_RUNTIME)

		# Writeback Ops
		self.play(self.writebackStage.animateMux("0x0", "0x0", "0x0", self.paths), run_time=self.STAGE_SLOW_RUNTIME)

		# Zoom out for Pipe clocks
		self.play(self.camera.frame.animate.move_to(self.decodeStage).scale(3.2).shift(UP*2.75), run_time=self.STAGE_SLOW_RUNTIME)


		self.play(self.fetchPipeline.animateFin("0x400118"), run_time=self.STAGE_SLOW_RUNTIME)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle3(self):
		self.play(
			self.fetchStage.animateInstruction("nop"),
			self.decodeStage.animateInstruction("nop"),
			self.executeStage.animateInstruction("add x1, x1, #0xfff"),
			self.memoryStage.animateInstruction("add x0, x0, #1"),
			self.writebackStage.animateInstruction("-")
		)

		self.play(
			# Fetch Ops
			self.fetchStage.animateSelectPC("0x0", "OP_ADD", "0x400114", "T", "OP_ADD", "0x40011c"),
			self.fetchStage.animateImemExtract("0xd503201f", "OP_NOP"),
			self.fetchStage.animatePredictPC("OP_NOP", "0x40011c", "0x400120", "0x400120"),

			self.decodePipeline.animateDin("0x91000400", "OP_NOP", "0x400114", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_NOP"),
			self.decodeStage.animateExtract("0xd503201f", "0x0"),
			self.decodeStage.animateDecideALU("OP_NOP", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "0", "0x0", False, "0x0", "0x0"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_NOP", "0x40011c", "PASS_OP", "EQ", "0x1", "0x0", "0x0", "0x0", "32"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0xfff", "0xfff", self.paths),
			self.executeStage.animateALU("0x0", "0xfff", "0x0", "PLUS_OP", "EQ", "T", "0xfff", self.paths),

			self.memoryPipeline.animateMin("T", "0x400118", "0xfff", "0x0", "1"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x1", "0x0"),

			self.writebackPipeline.animateWin("0x1", "0x0", "0"),

			# Writeback Ops
			self.writebackStage.animateMux("0x0", "0x0", "0x0", self.paths),


			self.fetchPipeline.animateFin("0x400120"), 
						
			run_time=self.STAGE_RUNTIME
		)

		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle4(self):
		self.play(
			self.fetchStage.animateInstruction("nop"),
			self.decodeStage.animateInstruction("nop"),
			self.executeStage.animateInstruction("nop"),
			self.memoryStage.animateInstruction("add x1, x1, #0xfff"),
			self.writebackStage.animateInstruction("add x0, x0, #1")
		)

		self.play(
			# Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_NOP", "0x400118", "T", "OP_ADD", "0x400120"),
			self.fetchStage.animateImemExtract("0xd503201f", "OP_NOP"),
			self.fetchStage.animatePredictPC("OP_NOP", "0x400120", "0x400124", "0x400124"),

			self.decodePipeline.animateDin("0xd503201f", "OP_NOP", "0x400124", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_NOP"),
			self.decodeStage.animateExtract("0xd503201f", "0x0"),
			self.decodeStage.animateDecideALU("OP_NOP", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "0", "0x1", True, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_NOP", "0x400120", "PASS_OP", "F", "0x1", "0x0", "0x0", "0x0", "32"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x1", "0x0", "0x0", "PASS_OP", "0", "T", "0x1", self.paths),

			self.memoryPipeline.animateMin("T", "0x40011c", "0x1", "0x0", "32"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0xfff", "0x0"),

			self.writebackPipeline.animateWin("0xfff", "0x0", "1"),

			# Writeback Ops
			self.writebackStage.animateMux("0x1", "0x0", "0x1", self.paths),


			self.fetchPipeline.animateFin("0x400124"), 
			
			run_time=self.STAGE_RUNTIME
		)

		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle5(self):
		self.play(
			self.fetchStage.animateInstruction("add x4, x0, #1"),
			self.decodeStage.animateInstruction("nop"),
			self.executeStage.animateInstruction("nop"),
			self.memoryStage.animateInstruction("nop"),
			self.writebackStage.animateInstruction("add x1, x1, #0xfff")
		)

		self.play(
			# Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_NOP", "0x40011c", "T", "OP_NOP", "0x400124"),
			self.fetchStage.animateImemExtract("0x91000404", "OP_ADD"),
			self.fetchStage.animatePredictPC("OP_ADD", "0x400124", "0x400128", "0x400128"),

			self.decodePipeline.animateDin("0x91000404", "OP_ADD", "0x400128", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_NOP"),
			self.decodeStage.animateExtract("0xd503201f", "0x0"),
			self.decodeStage.animateDecideALU("OP_NOP", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "1", "0xfff", True, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_NOP", "0x400124", "PASS_OP", "F", "0x1", "0x0", "0x0", "0x0", "32"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x1", "0x0", "0x0", "PASS_OP", "0", "T", "0x1", self.paths),

			self.memoryPipeline.animateMin("T", "0x400120", "0x1", "0x0", "32"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x1", "0x0"),

			self.writebackPipeline.animateWin("0x1", "0x0", "32"),

			# Writeback Ops
			self.writebackStage.animateMux("0xfff", "0x0", "0xfff", self.paths),


			self.fetchPipeline.animateFin("0x400128"), 
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle6(self):
		self.play(
			self.fetchStage.animateInstruction("ret"),
			self.decodeStage.animateInstruction("add x4, x0, #1"),
			self.executeStage.animateInstruction("nop"),
			self.memoryStage.animateInstruction("nop"),
			self.writebackStage.animateInstruction("nop")
		)

		self.play(
			# Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_NOP", "0x400120", "T", "OP_NOP", "0x400128"),
			self.fetchStage.animateImemExtract("0xd65f03c0", "OP_RET"),
			self.fetchStage.animatePredictPC("OP_RET", "0x400128", "0x40012c", "0x40012c"),

			self.decodePipeline.animateDin("0xd65f03c0", "OP_RET", "0x40012c", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_ADD"),
			self.decodeStage.animateExtract("0x91000404", "0x1"),
			self.decodeStage.animateDecideALU("OP_ADD", "PLUS_OP"),
			self.decodeStage.animateRegfile("0", "0", "32", "0x1", False, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_ADD", "0x400128", "PLUS_OP", "F", "0x1", "0x1", "0x1", "0x0", "4"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x1", "0x0", "0x0", "PASS_OP", "0", "T", "0x1", self.paths),

			self.memoryPipeline.animateMin("T", "0x400124", "0x1", "0x0", "32"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x1", "0x0"),

			self.writebackPipeline.animateWin("0x1", "0x0", "32"),

			# Writeback Ops
			self.writebackStage.animateMux("0x1", "0x0", "0x1", self.paths),


			self.fetchPipeline.animateFin("0x40012c"), 
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle7(self):
		self.play(
			self.fetchStage.animateInstruction("-"),
			self.decodeStage.animateInstruction("ret"),
			self.executeStage.animateInstruction("add x4, x0, #1"),
			self.memoryStage.animateInstruction("nop"),
			self.writebackStage.animateInstruction("nop")
		)

		self.play(
			# Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_ADD", "0x400124", "T", "OP_NOP", "0x40012c"),
			self.fetchStage.animateImemExtract("0x0", "-"),
			self.fetchStage.animatePredictPC("-", "0x40012c", "0x400130", "0x400130"),

			self.decodePipeline.animateDin("0x0", "-", "0x400130", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_RET"),
			self.decodeStage.animateExtract("0xd65f03c0", "0x0"),
			self.decodeStage.animateDecideALU("OP_RET", "PASS_OP"),
			self.decodeStage.animateRegfile("30", "30", "32", "0x1", False, "0x0", "0x0"),
			self.decodeStage.animateForward("0x0", "0x0", self.paths),

			self.executePipeline.animateXin("OP_RET", "0x40012c", "PASS_OP", "F", "0x0", "0x0", "0x0", "0x0", "0"),

			# Execute Ops
			self.executeStage.animateMux("0x1", "0x1", "0x1", self.paths),
			self.executeStage.animateALU("0x1", "0x1", "0x0", "PLUS_OP", "EQ", "T", "0x2", self.paths),

			self.memoryPipeline.animateMin("T", "0x400128", "0x2", "0x1", "4"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x1", "0x0"),

			self.writebackPipeline.animateWin("0x1", "0x0", "32"),

			# Writeback Ops
			self.writebackStage.animateMux("0x1", "0x0", "0x1", self.paths),


			self.fetchPipeline.animateFin("0x400130"), 
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle8(self):
		self.play(
			self.fetchStage.animateInstruction("hlt"),
			self.decodeStage.animateInstruction("-"),
			self.executeStage.animateInstruction("ret"),
			self.memoryStage.animateInstruction("add x4, x0, #1"),
			self.writebackStage.animateInstruction("nop")
		)

		self.play(
			# # Fetch Ops
			# self.fetchStage.animateSelectPC("0x1", "OP_ADD", "0x400124", "T", "0", "0x40012c"),
			# self.fetchStage.animateImemExtract("0x0", "OP_ERROR"),
			# self.fetchStage.animatePredictPC("OP_ERROR", "0x40012c", "0x400130", "0x400130"),

			self.decodePipeline.animateDin("0xd4400000", "OP_HLT", "0x400130", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_NOP"),
			self.decodeStage.animateExtract("0x0", "0x0"),
			self.decodeStage.animateDecideALU("OP_NOP", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "32", "0x1", False, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_NOP", "0x0", "PASS_OP", "EQ", "0x1", "0x0", "0x0", "0x0", "0"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x0", "0x0", "0x0", "PASS_OP", "EQ", "T", "0x0", self.paths),

			self.memoryPipeline.animateMin("T", "0x40012c", "0x0", "0x0", "0"),

			# Memory Ops
			self.memoryStage.animateDmem("0x1", "0x2", "0x0"),

			self.writebackPipeline.animateWin("0x2", "0x0", "4"),

			# Writeback Ops
			self.writebackStage.animateMux("0x1", "0x0", "0x1", self.paths),


			self.fetchPipeline.animateFin("0x400130"), 
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle9(self):
		self.play(
			self.fetchStage.animateInstruction("hlt"),
			self.decodeStage.animateInstruction("hlt"),
			self.executeStage.animateInstruction("-"),
			self.memoryStage.animateInstruction("ret"),
			self.writebackStage.animateInstruction("add x4, x0, #1")
		)

		self.play(
			# # Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_NOP", "0x40012c", "T", "OP_RET", "0x400130"),
			# self.fetchStage.animateImemExtract("0x0", "OP_ERROR"),
			# self.fetchStage.animatePredictPC("OP_ERROR", "0x40012c", "0x400130", "0x400130"),

			self.decodePipeline.animateDin("0xd4400000", "OP_HLT", "0x400130", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_HLT"),
			self.decodeStage.animateExtract("0xd4400000", "0x0"),
			self.decodeStage.animateDecideALU("OP_HLT", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "4", "0x2", True, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_HLT", "0x400130", "PASS_OP", "EQ", "0x1", "0x0", "0x0", "0x0", "0"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x1", "0x0", "0x0", "PASS_OP", "EQ", "T", "0x1", self.paths),

			self.memoryPipeline.animateMin("T", "0x0", "0x1", "0x0", "0"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x0", "0x0"),

			self.writebackPipeline.animateWin("0x0", "0x0", "0"),

			# Writeback Ops
			self.writebackStage.animateMux("0x2", "0x0", "0x2", self.paths),


			self.fetchPipeline.animateFin("0x400130"), 
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle10(self):
		self.play(
			self.fetchStage.animateInstruction("hlt"),
			self.decodeStage.animateInstruction("hlt"),
			self.executeStage.animateInstruction("hlt"),
			self.memoryStage.animateInstruction("-"),
			self.writebackStage.animateInstruction("ret")
		)

		self.play(
			# # Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_HLT", "0x0", "T", "OP_NOP", "0x400130"),
			# self.fetchStage.animateImemExtract("0x0", "OP_ERROR"),
			# self.fetchStage.animatePredictPC("OP_ERROR", "0x40012c", "0x400130", "0x400130"),

			self.decodePipeline.animateDin("0xd4400000", "OP_HLT", "0x400130", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_HLT"),
			self.decodeStage.animateExtract("0xd4400000", "0x0"),
			self.decodeStage.animateDecideALU("OP_HLT", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "0", "0x0", False, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_HLT", "0x400130", "PASS_OP", "EQ", "0x1", "0x0", "0x0", "0x0", "0"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x1", "0x0", "0x0", "PASS_OP", "EQ", "T", "0x1", self.paths),

			self.memoryPipeline.animateMin("T", "0x400130", "0x1", "0x0", "0"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x1", "0x0"),

			self.writebackPipeline.animateWin("0x1", "0x0", "0"),

			# Writeback Ops
			self.writebackStage.animateMux("0x0", "0x0", "0x0", self.paths),


			self.fetchPipeline.animateFin("0x400130"), 
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle11(self):
		self.play(
			self.fetchStage.animateInstruction("hlt"),
			self.decodeStage.animateInstruction("hlt"),
			self.executeStage.animateInstruction("hlt"),
			self.memoryStage.animateInstruction("hlt"),
			self.writebackStage.animateInstruction("-")
		)

		self.play(
			# # Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_HLT", "0x400130", "T", "OP_HLT", "0x40012c"),
			# self.fetchStage.animateImemExtract("0x0", "OP_ERROR"),
			# self.fetchStage.animatePredictPC("OP_ERROR", "0x40012c", "0x400130", "0x400130"),

			self.decodePipeline.animateDin("0xd4400000", "OP_HLT", "0x400130", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_HLT"),
			self.decodeStage.animateExtract("0xd4400000", "0x0"),
			self.decodeStage.animateDecideALU("OP_HLT", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "0", "0x1", False, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_HLT", "0x400130", "PASS_OP", "EQ", "0x1", "0x0", "0x0", "0x0", "0"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x1", "0x0", "0x0", "PASS_OP", "EQ", "T", "0x1", self.paths),

			self.memoryPipeline.animateMin("T", "0x400130", "0x1", "0x0", "0"),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x1", "0x0"),

			self.writebackPipeline.animateWin("0x1", "0x0", "0"),

			# Writeback Ops
			self.writebackStage.animateMux("0x1", "0x0", "0x1", self.paths),


			self.fetchPipeline.animateFin("0x400130"), 
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def cycle12(self):
		self.play(
			self.fetchStage.animateInstruction("hlt"),
			self.decodeStage.animateInstruction("hlt"),
			self.executeStage.animateInstruction("hlt"),
			self.memoryStage.animateInstruction("hlt"),
			self.writebackStage.animateInstruction("hlt")
		)

		self.play(
			# Fetch Ops
			self.fetchStage.animateSelectPC("0x1", "OP_HLT", "0x0", "F", "OP_NOP", "0x400130"),
			# self.play(self.fetchStage.animateImemExtract("0x0", "OP_ERROR"))
			# self.play(self.fetchStage.animatePredictPC("OP_ERROR", "0x40012c", "0x400130", "0x400130"))

			self.decodePipeline.animateDin("0xd4400000", "OP_HLT", "0x400130", "0x0"),

			# Decode Ops
			self.decodeStage.animateGenerateSigs("OP_HLT"),
			self.decodeStage.animateExtract("0xd4400000", "0x0"),
			self.decodeStage.animateDecideALU("OP_HLT", "PASS_OP"),
			self.decodeStage.animateRegfile("0", "0", "0", "0x1", False, "0x1", "0x1"),
			self.decodeStage.animateForward("0x1", "0x1", self.paths),

			self.executePipeline.animateXin("OP_HLT", "0x400130", "PASS_OP", "EQ", "0x1", "0x0", "0x0", "0x0", "0"),

			# Execute Ops
			self.executeStage.animateMux("0x0", "0x0", "0x0", self.paths),
			self.executeStage.animateALU("0x1", "0x0", "0x0", "PASS_OP", "EQ", "T", "0x1", self.paths),

			self.memoryPipeline.animateMin("T", "0x400130", "0x1", "0x0", "0"),
			self.camera.frame.animate.move_to(self.memoryStage).shift(UP),

			# Memory Ops
			self.memoryStage.animateDmem("0x0", "0x0", "0x0"),

			self.writebackPipeline.animateWin("0x0", "0x0", "0"),

			# Writeback Ops
			self.writebackStage.animateMux("0x1", "0x0", "0x1", self.paths),


			self.fetchPipeline.animateFin("0x400130"),
			run_time=self.STAGE_RUNTIME
		)


		self.play(
			self.fetchPipeline.animateClock(),
			self.decodePipeline.animateClock(),
			self.executePipeline.animateClock(),
			self.memoryPipeline.animateClock(),
			self.writebackPipeline.animateClock(), 
			run_time=self.CLOCK_RUNTIME
		)
		# End of cycle

	def construct(self):
		self.intro()

		self.wait(1)

		self.pipeline()

		self.wait(1)