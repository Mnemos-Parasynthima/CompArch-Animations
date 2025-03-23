from sys import path
from pathlib import Path as libPath

path.append(str(libPath(__file__).resolve().parent.parent))

from animlib.pipeline import *
from animlib.mem import InstructionMemory
from animlib.hexdec import Hexadecimal, CodeBlock

from manim import *
from manim.typing import Point3D

from selib import *


class SEQScene(MovingCameraScene):
	def __init__(self, asmfile:str="asm-stripped.s"):
		super().__init__()

		self.paths:dict[str, Path|ArrowPath] = {}

		self.asmfile = "./assembly/" + asmfile
		self.instructionMemory:InstructionMemory = None

		self.fetchStage = FetchStage()
		self.decodeStage = DecodeStage()
		self.executeStage = ExecuteStage()
		self.memoryStage = MemoryStage()
		self.writebackStage = WritebackStage()

	def intro(self):
		title = Text("Current Working Program", font_size=35).to_edge(UP)
		self.play(Write(title))

		# paraiso-dark, fruity

		completeAsm = Code(
			"./assembly/asm.s",
			tab_width=2,
			formatter_style="paraiso-dark",
			background="rectangle",
			language="as"
		).to_edge(LEFT, buff=0.1)

		self.play(FadeIn(completeAsm))

		strippedAsm = Code(
			self.asmfile,
			tab_width=2,
			formatter_style="fruity",
			background="rectangle",
			language="as"
		).shift(RIGHT * 1.4)

		self.play(TransformFromCopy(completeAsm, strippedAsm))

		self.play(strippedAsm.animate.shift(LEFT*4), FadeOut(completeAsm))

		self.instructionMemory = InstructionMemory(self.asmfile, entry=0xf00, entryAddr=Hexadecimal("0xf00")).to_edge(RIGHT, buff=0.05).shift(DOWN*0.3)

		caption = Text("Instruction Memory", font_size=20).move_to(self.instructionMemory.blocks.get_top() + UP*0.25)#.next_to(self.instructionMemory, UP, buff=0.2).shift(LEFT*0.05)

		self.play(FadeIn(self.instructionMemory, caption))

		self.wait(0.5)

		self.play(FadeOut(strippedAsm, self.instructionMemory, title, caption))

	def createGlobalPaths(self):
		srcArrow:Point3D = None
		dstArrow:Point3D = None
		dst1Arrow:Point3D = None

		srcArrow = self.fetchStage.imem.rvalArrow.get_right()
		imem_DecodeLogic = Path(
			srcArrow, [self.decodeStage.decodeLogic.get_left()[0], srcArrow[1], 0],
			color=RED, strokeWidth=2
		)
		self.paths["imem_DecodeLogic"] = imem_DecodeLogic

		srcArrow = self.decodeStage.regfile.valWArrow.get_left()
		dstArrow = self.writebackStage.dstmux.outputArrows[0].get_left()
		regfile_dstmux2 = Path(
			srcArrow, dstArrow,
			color=RED, strokeWidth=2
		)
		self.paths["regfile_dstmux2"] = regfile_dstmux2

		srcArrow = self.decodeStage.regfile.valAArrow.get_right()
		dstArrow = self.executeStage.alu.valAArrow.get_left()
		regfile_alu = Path(
			srcArrow, dstArrow,
			color=RED, strokeWidth=2
		)
		self.paths["regfile_alu"] = regfile_alu

		srcArrow = self.decodeStage.regfile.valBArrow.get_right()
		dstArrow = self.executeStage.valbmux.inputArrows[0].get_left()
		dst1Arrow = self.memoryStage.dmem.wvalArrow.get_left()
		regfile_valbmux_dmem = Path(
			srcArrow, dstArrow,
			srcArrow+(RIGHT*0.5), srcArrow+(RIGHT*0.5)+(UP*3.5),
			srcArrow+(RIGHT*0.5)+(UP*3.5)+(RIGHT*5), [(srcArrow+(RIGHT*0.5)+(UP*3.5)+(RIGHT*5))[0], dst1Arrow[1], 0],
			dst1Arrow,
			color=RED, strokeWidth=2
		).markIntersections([2], RED)
		self.paths["regfile_valbmux_dmem"] = regfile_valbmux_dmem

		dstArrow = self.fetchStage.mux.inputArrows[3].get_right()
		regfile_nextmux = Path(
			srcArrow, [srcArrow[0], dstArrow[1], 0], dstArrow,
			color=RED, strokeWidth=2
		).markIntersections([0], RED)
		self.paths["regfile_nextmux"] = regfile_nextmux

		srcArrow = self.executeStage.alu.valEArrow.get_right()
		dstArrow = self.memoryStage.dmem.addrArrow.get_left()
		dst1Arrow = self.writebackStage.wvalmux.inputArrows[0].get_right()
		alu_dmem_wvalmux = Path(
			srcArrow, srcArrow+RIGHT,
			srcArrow+RIGHT+(UP*3), srcArrow+RIGHT+(UP*3)+(LEFT*3.5),
			[(srcArrow+RIGHT+(UP*3)+(LEFT*3.5))[0], dstArrow[1], 0], dstArrow,
			[(srcArrow+RIGHT+(UP*3)+(LEFT*3.5))[0], dstArrow[1], 0], [(srcArrow+RIGHT+(UP*3)+(LEFT*3.5))[0], dst1Arrow[1], 0], dst1Arrow,
			color=RED, strokeWidth=2
		).markIntersections([6], RED)
		self.paths["alu_dmem_wvalmux"] = alu_dmem_wvalmux

		srcArrow = self.memoryStage.dmem.rvalArrow.get_right()
		dstArrow = self.writebackStage.wvalmux.inputArrows[1].get_right()
		dmem_wvalmux = Path(
			srcArrow, srcArrow+(RIGHT*0.6),
			srcArrow+(RIGHT*0.6)+(UP*2), srcArrow+(RIGHT*0.6)+(UP*2)+(LEFT*6.5), [(srcArrow+(RIGHT*0.6)+UP+(LEFT*6.5))[0], dstArrow[1], 0], dstArrow,
			color=RED, strokeWidth=2
		)
		self.paths["dmem_wvalmux"] = dmem_wvalmux

		srcArrow = self.writebackStage.dstmux.inputArrows[0].get_right()
		dstArrow = self.fetchStage.mux.inputArrows[0].get_right()
		dst1Arrow = self.fetchStage.seqPCAdder.cArrow.get_top() # not really a dst but a temp/helper
		dstmux_pcmux = Path(
			srcArrow, srcArrow+(UP*1.4),
			[dst1Arrow[0], (srcArrow+(UP*1.4))[1], 0], [dst1Arrow[0], dstArrow[1], 0],
			color=RED, strokeWidth=2
		).markIntersections([3], RED)
		self.paths["dstmux_pcmux"] = dstmux_pcmux

	def stages(self):
		selib = SELib("./libse.so")

		self.fetchStage.shift(LEFT*10.2)
		self.decodeStage.shift(DOWN*3.1+LEFT*2)
		self.executeStage.shift(RIGHT*6.8 + DOWN*4.25)
		self.memoryStage.shift(RIGHT*10.8 + UP*2)
		self.writebackStage.shift(UP*3 + RIGHT*1.35)

		self.createGlobalPaths()


		# Instead of scaling the stages down, just increase the view
		self.camera.frame.scale(1.9)

		self.play(FadeIn(
			self.fetchStage, self.decodeStage, self.executeStage, self.memoryStage, self.writebackStage,
			*list(self.paths.values())
		))

		self.camera.frame.save_state()

		guest = selib.initMachine()
		_globals = selib.initGlobals()
		entry = selib.loadElf("./assembly/add", guest)
		selib.initRunElf(entry, guest)
		

		# View Fetch
		currInstrBox = Rectangle(width=self.instructionMemory.maxLen*0.4, height=1).shift(UP*6.8 + RIGHT*9)
		currInstr0 = CodeBlock(self.instructionMemory.getInstruction(0).instructionText).move_to(currInstrBox)
		self.play(FadeIn(currInstrBox, currInstr0))


		self.play(self.camera.frame.animate.set_height(5).move_to(self.fetchStage.get_bottom()+UP*1.8))

		selib.fetchInstr(guest, _globals)

		insn = self.instructionMemory.getInstruction(0).encoded
		insnStr = hex(insn)

		pc = self.instructionMemory.end
		pcStr = hex(pc)

		self.play(self.fetchStage.animateCurrPC(pcStr, insnStr, self.paths))

		self.play(self.camera.frame.animate.shift(UP*4))

		offset = selib.getBranchOffset(_globals, guest)
		self.play(self.fetchStage.animatePredPC(hex(pc+4), hex(pc+offset), self.paths))


		# View Decode
		self.play(self.camera.frame.animate.move_to(self.decodeStage.get_center() + RIGHT*0.75))

		selib.decodeInstr(guest, _globals)
		_tuple = selib.getDecodeSrc2Data(guest)

		dst:str = hex(selib.getDecodeDst(guest))
		src2_1:str = hex(selib.getDecodeSrc2_1(_tuple))
		src2_2:str = hex(selib.getDecodeSrc2_2(_tuple))

		src1:str = hex(selib.getDecodeSrc1(guest))

		imm:str = hex(selib.getImmval(guest))

		# Logic to determine muxes selection
		dstSel = selib.getDecodeDstSel(guest)
		src2Sel = selib.getDecodeSrc2Sel(_tuple)

		self.play(self.decodeStage.animateMuxs(dst, src2_1, src2_2, dstSel, src2Sel))

		# if src2Sel: src2 = src2_2
		# else: src2 = src2_1
		src2 = hex(selib.getDecodeSrc2(_tuple))

		valA = hex(selib.getValA(guest))
		valB = hex(selib.getValB(guest))

		self.play(self.decodeStage.animateRegfileRead(dst, src1, src2, valA, valB, self.paths))


		# View Execute
		
		self.play(self.camera.frame.animate.move_to(self.executeStage.get_center()))

		selib.executeInstr(guest)

		# Logic to determine mux selection
		valBSel = selib.getValBSel(guest)

		self.play(self.executeStage.animateMux(valB, imm, valBSel))

		if valBSel: aluValB = valB
		else: aluValB = imm

		valHw:str = hex(selib.getValHw(guest))

		# Logic to do ALU
		valE:str = hex(selib.getValEx(guest))

		aluOP = selib.getAluOp(guest)
		setCC = selib.getSetCC(guest)
		cond = selib.getCond(guest)
		condVal = selib.getCondVal(guest)

		self.play(self.executeStage.animateALU(valA, aluValB, valHw, aluOP, setCC, cond, condVal, valE, self.paths))


		# View Memory
		self.play(self.camera.frame.animate.move_to(self.memoryStage.get_center()))

		selib.memoryInstr(guest)

		# Logic to get memory
		addr:str = valE
		wval:str = valB
		rval:str = hex(selib.getRVal(guest))
		# rval will either be the read value or 0
		memRead = selib.getMemRead(guest)
		memWrite = selib.getMemWrite(guest)

		self.play(self.memoryStage.animateDMem(wval, addr, rval, memRead, memWrite, self.paths))


		# View Writeback
		self.play(self.camera.frame.animate.move_to(self.writebackStage.get_center()+RIGHT))

		selib.wbackInstr(guest, _globals)

		# Logic for muxes
		# No need to have api functions since the values are just transferred between pipeline registers
		# And valE and rval are acquired from there
		# dst can be left as pc+4 as that never changes, plus, reduces size of api functions
		wval0:str = valE
		wval1:str = rval
		dst = hex(pc+4)

		wvalSel = selib.getWvalSel(guest)
		dstSel = selib.getWriteDstSel(guest)

		self.play(self.writebackStage.animateMuxs(wval0, wval1, dst, wvalSel, dstSel, self.paths))

		self.play(self.camera.frame.animate.move_to(self.decodeStage.regfile.get_top()))

		if dstSel: wval = dst
		else:
			if wvalSel: wval = wval1
			else: wval = wval0

		self.play(self.decodeStage.animateRegfileWrite(wval, selib.getWEnable(guest), self.paths))

		self.play(self.camera.frame.animate.move_to(self.fetchStage.get_top() + DOWN))

		# Update pc

		# Logic to select next pc
		nextpc:str = dst
		sel = 0

		self.play(self.fetchStage.animateUpdatePC(valB, nextpc, sel, self.paths))

		self.play(self.camera.frame.animate.set_height(5).move_to(self.fetchStage.get_bottom()+UP*1.8))

		self.play(self.fetchStage.animateUpdateEnd(nextpc))

		self.play(self.camera.frame.animate.restore())

		selib.postCycle(guest, _globals)

		idx = 1

		# Continue the execution while in global view
		while (True):
			selib.fetchInstr(guest, _globals)

			currInstr1 = CodeBlock(self.instructionMemory.getInstruction(idx).instructionText).move_to(currInstrBox)
			self.play(ReplacementTransform(currInstr0, currInstr1))
			currInstr0 = currInstr1

			insn = self.instructionMemory.getInstruction(idx).encoded
			insnStr = hex(insn)

			print(insnStr)

			pcStr = nextpc
			pc = int(nextpc, 16)

			self.play(self.fetchStage.animateCurrPC(pcStr, insnStr, self.paths))

			offset = selib.getBranchOffset(_globals, guest)
			self.play(self.fetchStage.animatePredPC(hex(pc+4), hex(pc+offset), self.paths))


			# View Decode
			selib.decodeInstr(guest, _globals)
			_tuple = selib.getDecodeSrc2Data(guest)

			dst:str = hex(selib.getDecodeDst(guest))
			src2_1:str = hex(selib.getDecodeSrc2_1(_tuple))
			src2_2:str = hex(selib.getDecodeSrc2_2(_tuple))

			src1:str = hex(selib.getDecodeSrc1(guest))

			imm:str = hex(selib.getImmval(guest))

			dstSel = selib.getDecodeDstSel(guest)
			src2Sel = selib.getDecodeSrc2Sel(_tuple)

			self.play(self.decodeStage.animateMuxs(dst, src2_1, src2_2, dstSel, src2Sel))

			src2 = hex(selib.getDecodeSrc2(_tuple))

			valA = hex(selib.getValA(guest))
			valB = hex(selib.getValB(guest))

			self.play(self.decodeStage.animateRegfileRead(dst, src1, src2, valA, valB, self.paths))


			# View Execute
			selib.executeInstr(guest)

			valBSel = selib.getValBSel(guest)

			self.play(self.executeStage.animateMux(valB, imm, valBSel))

			if valBSel: aluValB = valB
			else: aluValB = imm

			valHw:str = hex(selib.getValHw(guest))

			valE:str = hex(selib.getValEx(guest))

			aluOP = selib.getAluOp(guest)
			setCC = selib.getSetCC(guest)
			cond = selib.getCond(guest)
			condVal = selib.getCondVal(guest)

			self.play(self.executeStage.animateALU(valA, aluValB, valHw, aluOP, setCC, cond, condVal, valE, self.paths))


			# View Memory
			selib.memoryInstr(guest)

			addr:str = valE
			wval:str = valB
			rval:str = hex(selib.getRVal(guest))

			memRead = selib.getMemRead(guest)
			memWrite = selib.getMemWrite(guest)

			self.play(self.memoryStage.animateDMem(wval, addr, rval, memRead, memWrite, self.paths))


			# View Writeback
			selib.wbackInstr(guest, _globals)

			wval0:str = valE
			wval1:str = rval
			dst = hex(pc+4)

			wvalSel = selib.getWvalSel(guest)
			dstSel = selib.getWriteDstSel(guest)

			self.play(self.writebackStage.animateMuxs(wval0, wval1, dst, wvalSel, dstSel, self.paths))

			if dstSel: wval = dst
			else:
				if wvalSel: wval = wval1
				else: wval = wval0

			self.play(self.decodeStage.animateRegfileWrite(wval, selib.getWEnable(guest), self.paths))

			# Update pc

			# Logic to select next pc
			nextpc:str = dst
			sel = 0

			self.play(self.fetchStage.animateUpdatePC(valB, nextpc, sel, self.paths))

			self.play(self.fetchStage.animateUpdateEnd(nextpc))

			selib.postCycle(guest, _globals)

			idx += 1
			if (idx >= self.instructionMemory.size): break

		regState = RegistersState(list(selib.getRegisters(guest).contents), selib.getSP(guest), selib.getPC(guest), selib.getNZCV(guest))
		regState.scale(1.5)
		self.play(FadeIn(regState))
		self.wait(1)
		self.play(FadeOut(regState))

		self.clear()
		selib.shutdownMachine(guest, _globals)

	def construct(self):
		self.intro()

		self.wait(1)

		self.stages()

		self.wait(2)
