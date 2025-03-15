from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Text
from .core import Stage
from .ALU import ALU
from .logic import Mux
from .Path import Path
from ..hexdec import CodeBlock


class ExecuteStage(Stage): 
	def __init__(self):
		super().__init__(6.5, 5)

		self.alu = ALU().shift(RIGHT*1.8)
		self.valbmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.LR).shift(LEFT*1.5)
		self.valbmux.addSignal(CodeBlock("valb_sel", fontSize=23), Mux.BOTTOM)

		self.add(self.alu, self.valbmux)

		valbmux_alu = Path(self.valbmux.outputArrows[0].get_right(), self.alu.valBArrow.get_left(), color=RED, strokeWidth=2)
		self.paths["valbmux_alu"] = valbmux_alu

		self.add(*list(self.paths.values()))


class ExecutePipeline(VGroup): pass

class ExecuteElements(VGroup): pass