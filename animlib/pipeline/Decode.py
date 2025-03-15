from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Text
from .RegFile import RegFile
from .logic import Mux
from .Path import Path
from ..hexdec import CodeBlock


class DecodeStage(VGroup): 
	def __init__(self):
		super().__init__()

		stage = RoundedRectangle(corner_radius=0.5, width=10, height=5)
		self.regfile = RegFile().shift(RIGHT*3)
		self.dstmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*0.5 + UP*0.34)
		self.dstmux.addSignal(CodeBlock("dst_sel", fontSize=23), Mux.TOP)
		self.src2mux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*0.5 + DOWN)
		self.src2mux.addSignal(CodeBlock("src2_sel", fontSize=23), Mux.BOTTOM)
		self.decodeLogic = RoundedRectangle(corner_radius=0.4, width=2, height=3).shift(LEFT*3.5)
		self.decodeLogicLabel = Text("Decode\n  Logic", font_size=28).move_to(self.decodeLogic.get_center())

		self.add(stage, self.regfile, self.dstmux, self.src2mux, self.decodeLogic, self.decodeLogicLabel)

		# Connecting line/paths
		# These will only concern with paths within the Stage
		# For interstage paths, they will be made at the outside level
		self.paths:list[Path] = []

		dstmux_regfile = Path(self.dstmux.outputArrows[0].get_right(), self.regfile.dstArrow.get_left(), color=RED, strokeWidth=2)
		self.paths.append(dstmux_regfile)

		src2mux_regfile = Path(self.src2mux.outputArrows[0].get_right(), self.regfile.src2Arrow.get_left(), color=RED, strokeWidth=2)
		self.paths.append(src2mux_regfile)

		self.add(*self.paths)

	def highlightPath(self, index:int):
		return self.paths[index].highlight(BLUE, 4)
	
	def dehighlightPath(self, index:int):
		return self.paths[index].highlight(RED, 2)
	


class DecodePipeline(VGroup): pass

class DecodeElements(VGroup): pass