from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE
from .PC import PC
from .IMem import IMem
from .logic import Adder, Mux
from .Path import Path
from ..hexdec import CodeBlock


class FetchStage(VGroup): 
	def __init__(self):
		super().__init__()

		stage = RoundedRectangle(corner_radius=0.5, width=6, height=8)
		self.pc = PC().shift(DOWN*2.4 + LEFT*1.65).scale(0.8)
		self.imem = IMem().shift(DOWN*3 + RIGHT*1.2).scale(0.8)
		self.mux = Mux(4,1, width=1.5, direction=Mux.RL).shift(LEFT*1.24 + UP*2) #2.5
		self.mux.addSignal(CodeBlock("next_PC_sel", fontSize=23), Mux.TOP)
		self.seqPCAdder = Adder(CodeBlock("4"), 4).shift(RIGHT*0.8 + DOWN*0.5).scale(0.5)
		label = CodeBlock("branch_offset", fontSize=40)
		self.brPCAdder = Adder(label).shift(RIGHT*1.6 + DOWN*0.5).scale(0.5)

		self.add(stage, self.pc, self.imem, self.mux, self.seqPCAdder, self.brPCAdder)

		# Connecting line/paths
		# These will only concern with paths within the Stage
		# For interstage paths, they will be made at the outside level
		self.paths:list[Path] = []

		mux_pc = Path(self.mux.outputArrows[0].get_left(), self.pc.nextPCArrow.get_left(), color=RED, strokeWidth=2)
		self.paths.append(mux_pc)

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
		self.paths.append(pc_imem_adders)

		seqUp = self.seqPCAdder.cArrow.get_top()
		muxIn0Right = self.mux.inputArrows[0].get_right()
		muxIn1Right = self.mux.inputArrows[1].get_right()
		seqAdder_mux = Path(
			seqUp, [seqUp[0], muxIn1Right[1], 0], 
			muxIn1Right, [seqUp[0], muxIn1Right[1], 0],
			[seqUp[0], muxIn0Right[1], 0], muxIn0Right, color=RED, strokeWidth=2
		).markIntersections([1], RED)
		self.paths.append(seqAdder_mux)

		brUp = self.brPCAdder.cArrow.get_top()
		muxIn2Right = self.mux.inputArrows[2].get_right()
		brAdder_mux = Path(brUp, [brUp[0], muxIn2Right[1], 0], muxIn2Right, color=RED, strokeWidth=2)
		self.paths.append(brAdder_mux)

		self.add(*self.paths)

	def highlightPath(self, index:int):
		return self.paths[index].animate.set_color(BLUE).set_stroke(width=4)
	
	def dehighlightPath(self, index:int):
		return self.paths[index].animate.set_color(RED).set_stroke(width=2)
	


class FetchPipeline(VGroup): pass

class FetchElements(VGroup): pass


