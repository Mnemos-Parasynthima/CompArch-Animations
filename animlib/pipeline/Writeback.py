from manim import VGroup, RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Text
from .core import Stage, Register
from .logic import Mux
from .Path import Path
from ..hexdec import CodeBlock


class WritebackStage(Stage):
	def __init__(self):
		super().__init__(9, 3.4)

		self.dstmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.RL).shift(LEFT*0.5 + UP*0.2)
		self.dstmux.addSignal(CodeBlock("dst_sel", fontSize=23), Mux.TOP)
		self.wvalmux = Mux(2,1, width=1.5, arrowSpacing=0.2, direction=Mux.RL).shift(RIGHT*2.8 + DOWN*0.15)
		self.wvalmux.addSignal(CodeBlock("wval_sel", fontSize=23), Mux.BOTTOM)
		self.statusLogic = RoundedRectangle(corner_radius=0.3, width=1.5, height=2).shift(LEFT*3.2)
		self.statusLogicLabel = Text("Status\n Logic", font_size=28).move_to(self.statusLogic.get_center())

		self.add(self.dstmux, self.wvalmux, self.statusLogic, self.statusLogicLabel)

		wvalmux_dstmux = Path(self.wvalmux.outputArrows[0].get_left(), self.dstmux.inputArrows[1].get_right(), color=RED, strokeWidth=2)
		self.paths["wvalmux_dstmux"] = wvalmux_dstmux

		self.add(*list(self.paths.values()))


class WritebackPipeline(Register):
	def __init__(self):
		super().__init__(Register.WRITEBACK)

		for i in range(len(self.components)):
			if i not in (0, 2, 6, 9, 11, 13):
				self.components[i] = None
				self.componentsText[i] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

class WritebackElements(VGroup): pass