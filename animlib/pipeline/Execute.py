from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Text
from .ALU import ALU
from .logic import Mux
from .Path import Path
from ..hexdec import CodeBlock


class ExecuteStage(VGroup): 
	def __init__(self):
		super().__init__()

		stage = RoundedRectangle(corner_radius=0.5, width=6.5, height=5)
		self.alu = ALU().shift(RIGHT*1.8)
		self.valbmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*1.5)
		self.valbmux.addSignal(CodeBlock("valb_sel", fontSize=23), Mux.BOTTOM)

		self.add(stage, self.alu, self.valbmux)

		# Connecting line/paths
		# These will only concern with paths within the Stage
		# For interstage paths, they will be made at the outside level
		self.paths:list[Path] = []

		valbmux_alu = Path(self.valbmux.outputArrows[0].get_right(), self.alu.valBArrow.get_left(), color=RED, strokeWidth=2)
		self.paths.append(valbmux_alu)

		self.add(*self.paths)

	def highlightPath(self, index:int):
		# return self.paths[index].animate.set_color(BLUE).set_stroke(width=4)
		return self.paths[index].highlight(BLUE,4)
	
	def dehighlightPath(self, index:int):
		return self.paths[index].animate.set_color(RED).set_stroke(width=2)
	


class ExecutePipeline(VGroup): pass

class ExecuteElements(VGroup): pass