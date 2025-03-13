from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Text
from .logic import Mux
from .Path import Path
from ..hexdec import CodeBlock


class WritebackStage(VGroup): 
	def __init__(self):
		super().__init__()

		stage = RoundedRectangle(corner_radius=0.5, width=9, height=3.5)
		self.dstmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.RL).shift(LEFT*0.5 + UP*0.2)
		self.dstmux.addSignal(CodeBlock("dst_sel", fontSize=23), Mux.TOP)
		self.wvalmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.RL).shift(RIGHT*2.8 + DOWN*0.15)
		self.wvalmux.addSignal(CodeBlock("wval_sel", fontSize=23), Mux.BOTTOM)
		self.statusLogic = RoundedRectangle(corner_radius=0.3, width=1.5, height=2).shift(LEFT*3.2)
		self.statusLogicLabel = Text("Status\n Logic", font_size=28).move_to(self.statusLogic.get_center())

		self.add(stage, self.dstmux, self.wvalmux, self.statusLogic, self.statusLogicLabel)

		# Connecting line/paths
		# These will only concern with paths within the Stage
		# For interstage paths, they will be made at the outside level
		self.paths:list[Path] = []

		wvalmux_dstmux = Path(self.wvalmux.outputArrows[0].get_left(), self.dstmux.inputArrows[1].get_right(), color=RED, strokeWidth=2)
		self.paths.append(wvalmux_dstmux)

		self.add(*self.paths)

	def highlightPath(self, index:int):
		return self.paths[index].animate.set_color(BLUE).set_stroke(width=4)
	
	def dehighlightPath(self, index:int):
		return self.paths[index].animate.set_color(RED).set_stroke(width=2)
	


class WritebackPipeline(VGroup): pass

class WritebackElements(VGroup): pass