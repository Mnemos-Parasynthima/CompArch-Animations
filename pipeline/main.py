from sys import path
from pathlib import Path as libPath

path.append(str(libPath(__file__).resolve().parent.parent))

from animlib.pipeline import *
from animlib.mem import InstructionMemory
from animlib.hexdec import Hexadecimal, CodeBlock

from manim import *
from manim.typing import Point3D


class Main(MovingCameraScene):
	def __init__(self):
		super().__init__()

		# self.paths:list[Path] = []
		self.paths:dict[str, Path] = {}

		self.instructionMemory:InstructionMemory = None

		self.fetchStage:FetchStage = None
		self.decodeStage:DecodeStage = None
		self.executeStage:ExecuteStage = None
		self.memoryStage:MemoryStage = None
		self.writebackStage:WritebackStage = None
		

	def intro(self):
		title = Text("Current Working Program", font_size=35).to_edge(UP)
		self.play(Write(title))

		# paraiso-dark, one-dark, fruity

		completeAsm = Code(
			"asm.s",
			tab_width=2,
			formatter_style="one-dark",
			background="rectangle",
			language="as"
		).to_edge(LEFT, buff=0.1)

		self.play(FadeIn(completeAsm))

		strippedAsm = Code(
			"asm-stripped.s",
			tab_width=2,
			formatter_style="fruity",
			background="rectangle",
			language="as"
		).shift(RIGHT * 1.4)

		self.play(TransformFromCopy(completeAsm, strippedAsm))

		self.play(strippedAsm.animate.shift(LEFT*4), FadeOut(completeAsm))

		self.instructionMemory = InstructionMemory("asm-stripped.s", 
				end=0xf00, startAddr=Hexadecimal("0xf06"), endAddr=Hexadecimal("0xf00")).to_edge(RIGHT, buff=0.05).shift(DOWN*0.3)

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
		self.fetchStage = FetchStage().shift(LEFT*10.2)
		self.decodeStage = DecodeStage().shift(DOWN*3.1+LEFT*2)
		self.executeStage = ExecuteStage().shift(RIGHT*6.8 + DOWN*4.25)
		self.memoryStage = MemoryStage().shift(RIGHT*10.8 + UP*2)
		self.writebackStage = WritebackStage().shift(UP*3 + RIGHT*1.35)
		self.createGlobalPaths()

		self.play(self.camera.frame.animate.scale(1.9))

		self.play(FadeIn(
			self.fetchStage, self.decodeStage, self.executeStage, self.memoryStage, self.writebackStage,
			*list(self.paths.values())
		))

		self.camera.frame.save_state()

		# View Fetch
		self.play(self.camera.frame.animate.set_height(5).move_to(self.fetchStage.get_bottom()+UP*1.8))

		self.play(
			FadeIn(
				self.fetchStage.pc.setCurrPC(Hexadecimal(hex(self.instructionMemory.end))),
				shift=RIGHT
			)
		)
		self.play(
			FadeIn(
				self.fetchStage.imem.setAddr(Hexadecimal(hex(self.instructionMemory.end))),
				shift=RIGHT
			),
			self.fetchStage.highlightPath("pc_imem_adders"),
			FadeIn(
				self.fetchStage.seqPCAdder.setA(Hexadecimal(hex(self.instructionMemory.end))),
				self.fetchStage.brPCAdder.setA(Hexadecimal(hex(self.instructionMemory.end))),
				shift=UP
			)
		)

		self.play(self.fetchStage.dehighlightPath("pc_imem_adders"))

		insn = 0x91000400

		self.play(
			FadeIn(self.fetchStage.imem.setRVal(Hexadecimal(hex(insn))), shift=RIGHT),
			self.paths["imem_DecodeLogic"].highlight(BLUE, 4)
		)

		self.play(self.camera.frame.animate.shift(UP*4))

		self.play(
			FadeIn(self.fetchStage.seqPCAdder.setC(Hexadecimal(hex(self.instructionMemory.end+4))), shift=UP)
		)

		self.play(
			FadeIn(
				self.fetchStage.mux.setArrowInfo(Hexadecimal(hex(self.instructionMemory.end+4)), 0),
				self.fetchStage.mux.setArrowInfo(Hexadecimal(hex(self.instructionMemory.end+4)), 1),
				shift=LEFT
			),
			self.fetchStage.highlightPath("seqAdder_mux"),
			self.paths["dstmux_pcmux"].highlight(BLUE, 4),
			self.paths["imem_DecodeLogic"].highlight(RED, 2)
		)

		# View Decode
		self.play(self.camera.frame.animate.move_to(self.decodeStage.get_center() + RIGHT*0.75))

		self.play(
			FadeIn(
				*self.decodeStage.dstmux.setArrowInfoList([Hexadecimal(str(insn & 0b11111)), Hexadecimal("30")], []),
				shift=RIGHT
			)
		)
		self.play(FadeIn(
			*self.decodeStage.dstmux.setArrowInfoList([], [Hexadecimal(str(insn & 0b11111))]),
			self.decodeStage.regfile.setDst(Hexadecimal(str(0x91000400 & 0b11111))),
			shift=RIGHT
		), self.decodeStage.highlightPath("dstmux_regfile"))

		x0val = 0x0

		self.play(FadeIn(
			self.decodeStage.regfile.setValA(Hexadecimal(hex(x0val))),
			self.decodeStage.regfile.setSrc1(Hexadecimal("0")),
			shift=RIGHT
		), self.paths["regfile_alu"].highlight(BLUE, 4), self.decodeStage.dehighlightPath("dstmux_regfile"))

		# View Execute
		self.play(self.camera.frame.animate.move_to(self.executeStage.get_center()))

		self.play(FadeIn(self.executeStage.valbmux.setArrowInfo(Hexadecimal("0x1"), 1), shift=RIGHT))

		self.play(FadeIn(self.executeStage.valbmux.setArrowInfo(Hexadecimal("0x1"), 0, False), shift=RIGHT))

		self.play(
			FadeIn(
				self.executeStage.alu.setValA(Hexadecimal(hex(x0val))),
				self.executeStage.alu.setValB(Hexadecimal("0x1")),
				shift=RIGHT),
			FadeIn(self.executeStage.alu.setALUOp(Hexadecimal(ALU_OP.PLUS_OP.value)), shift=UP),
			self.executeStage.highlightPath("valbmux_alu")
		)

		self.play(
			FadeIn(self.executeStage.alu.setValE(Hexadecimal(hex(x0val + 0x1))), shift=RIGHT),
			self.paths["alu_dmem_wvalmux"].highlight(BLUE, 4),
			self.executeStage.dehighlightPath("valbmux_alu"),
			self.paths["regfile_alu"].highlight(RED, 2)
		)

		# View Memory
		self.play(self.camera.frame.animate.move_to(self.memoryStage.get_center()))

		self.play(FadeIn(self.memoryStage.dmem.setAddr(Hexadecimal(hex(x0val + 0x1))), shift=RIGHT))

		# View Writeback
		self.play(self.camera.frame.animate.move_to(self.writebackStage.get_center()+RIGHT))

		self.play(
			FadeIn(self.writebackStage.wvalmux.setArrowInfo(Hexadecimal(hex(x0val + 0x1)), 0), shift=LEFT),
			self.paths["alu_dmem_wvalmux"].highlight(RED, 2)
		)

		self.play(
			self.writebackStage.highlightPath("wvalmux_dstmux"),
			FadeIn(*self.writebackStage.dstmux.setArrowInfoList([
				Hexadecimal(hex(x0val + 0x1)), Hexadecimal(hex(self.instructionMemory.end+4))
			],[]), shift=LEFT)
		)

		self.play(
			self.writebackStage.dehighlightPath("wvalmux_dstmux"),
			FadeIn(self.writebackStage.dstmux.setArrowInfo(Hexadecimal(hex(x0val + 0x1)), 0, False), shift=LEFT),
			self.paths["regfile_dstmux2"].highlight(BLUE, 4)
		)

		self.play(self.camera.frame.animate.move_to(self.decodeStage.regfile.get_top()))

		self.play(
			FadeIn(self.decodeStage.regfile.setValW(Hexadecimal(hex(x0val + 0x1))), shift=RIGHT),
			self.decodeStage.regfile.writeEnable()
		)

		self.play(
			self.decodeStage.regfile.writeEnable(False),
			self.paths["regfile_dstmux2"].highlight(RED, 2),
			self.camera.frame.animate.move_to(self.fetchStage.get_top() + DOWN)
		)

		self.play(
			FadeIn(self.fetchStage.mux.setArrowInfo(Hexadecimal(hex(self.instructionMemory.end+4)), 0, False), shift=LEFT),
			self.fetchStage.highlightPath("mux_pc"),
			self.fetchStage.dehighlightPath("seqAdder_mux"),
			self.paths["dstmux_pcmux"].highlight(RED, 2)
		)


		self.play(
			self.fetchStage.dehighlightPath("mux_pc"),
			self.camera.frame.animate.set_height(5).move_to(self.fetchStage.get_bottom()+UP*1.8)
		)

		self.play(FadeIn(self.fetchStage.pc.setNextPC(Hexadecimal(hex(self.instructionMemory.end+4))), shift=RIGHT))

		self.play(self.camera.frame.animate.restore())

	def construct(self):
		self.intro()

		self.stages()

		self.wait(2)
