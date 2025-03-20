from manim import RoundedRectangle, LEFT, RIGHT, UP, DOWN, RED, BLUE, Text, DL, Succession, AnimationGroup, FadeIn, Arrow
from .core import Stage, Register
from .logic import Mux
from .Path import Path
from ..hexdec import CodeBlock, Hexadecimal


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

	def animateMuxs(self, wval0:str, wval1:str, dst:str, wvalSel:bool, dstSel:bool, globalPaths:dict[str, Path]) -> Succession:
		anims = []

		anims.append(
			FadeIn(
				*self.wvalmux.setArrowInfoList([Hexadecimal(wval0), Hexadecimal(wval1)], []),
				shift=LEFT
			)
		)

		# anims.append(self.wvalmux.setSignal())

		wval = wval1 if wvalSel else wval0

		anims.append(
			AnimationGroup(
				globalPaths["alu_dmem_wvalmux"].highlight(RED, 2),
				globalPaths["dmem_wvalmux"].highlight(RED, 2),
				FadeIn(self.wvalmux.setArrowInfo(Hexadecimal(wval), 0, False), shift=LEFT),
				self.highlightPath("wvalmux_dstmux")
			)
		)

		anims.append(
			FadeIn(
				*self.dstmux.setArrowInfoList([Hexadecimal(dst), Hexadecimal(wval)], []),
				shift=LEFT
			)
		)

		# anims.append(self.dstmux.setSignal())

		anims.append(
			AnimationGroup(
				self.dehighlightPath("wvalmux_dstmux"),
				FadeIn(
					self.dstmux.setArrowInfo(Hexadecimal(dst if dstSel else wval), 0, False),
					shift=LEFT
				),
				globalPaths["regfile_dstmux2"].highlight(BLUE, 4)
			)
		)

		return Succession(*anims)


class WritebackPipeline(Register):
	def __init__(self):
		super().__init__(Register.WRITEBACK)

		for i in range(len(self.components)):
			if i not in (0, 2, 6, 9, 11, 13):
				self.components[i] = None
				self.componentsText[i] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

class WritebackElements(Stage):
	def __init__(self):
		super().__init__(10, 1.5)

		stageLabel = CodeBlock("wback_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.3)
		self.add(stageLabel)

		self.mux = RoundedRectangle(corner_radius=0.25, width=3, height=0.5).shift(RIGHT*2.45)
		self.muxLabel = CodeBlock("2:1 mux", fontSize=22).move_to(self.mux.get_center())

		self.add(self.mux, self.muxLabel)

		muxArrow = Arrow(
			max_tip_length_to_length_ratio=0.1, stroke_width=3,
			color=BLUE
		).put_start_and_end_on(start=self.mux.get_left(), end=self.submobjects[0].get_left()+LEFT*0.4)
		self.add(muxArrow)