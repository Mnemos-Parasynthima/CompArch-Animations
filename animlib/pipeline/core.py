from manim import VGroup, RoundedRectangle, BLUE, RED, Rectangle, Polygon, RIGHT, WHITE, LEFT, ORIGIN, DashedLine, BLACK, GREY, UP, DOWN
from abc import ABC
from .Path import Path, ArrowPath
from ..hexdec import CodeBlock


class Stage(VGroup, ABC):
	def __init__(self, stageWidth:float, stageHeight:int, stageCornerRadius:float=0.5):
		super().__init__()

		stage = RoundedRectangle(corner_radius=stageCornerRadius, width=stageWidth, height=stageHeight)
		self.add(stage)

		# Connecting line/paths
		# These will only concern with paths within the Stage
		# For interstage paths, they will be made at the outside level
		self.paths:dict[str, Path|ArrowPath] = {}


	def highlightPath(self, path:str):
		return self.paths[path].highlight(BLUE, 4)
	
	def dehighlightPath(self, path:str):
		return self.paths[path].highlight(RED, 2)
	
class Register(VGroup, ABC):
	FETCH = 0
	DECODE = 1
	EXECUTE = 2
	MEMORY = 3
	WRITEBACK = 4

	def __init__(self, stage:int, registerWidth:int=14, registerHeight:int=1):
		super().__init__()

		stageLookup = ["F", "D", "X", "M", "W"]

		register = Rectangle(width=registerWidth, height=registerHeight)
		# Make vertices depend on height, following vertices are when height = 1
		clock = Polygon(*[[0.35,-0.25,0], [0,0,0], [0.35,0.25,0]], color=WHITE).move_to(register.get_right(), RIGHT)
		label = CodeBlock(f"{stageLookup[stage]}_instr", fontSize=25).next_to(clock, LEFT, buff=0.1)

		division = DashedLine(dash_length=0.02, dashed_ratio=0.2, color=GREY).put_start_and_end_on(start=register.get_left(), end=label.get_left())

		_out = CodeBlock(f"{stageLookup[stage]}_out", fontSize=18).next_to(label, UP, buff=0.13)
		_in = CodeBlock(f"{stageLookup[stage]}_in", fontSize=18).next_to(label, DOWN, buff=0.13)
		self.add(register, clock, label, division, _in, _out)

		# Initialize all components, regardless of the register type
		# This is so all of them can have the equal "distance"
		self.components:list[Rectangle] = [None for _ in range(14)]

		self.components[0] = Rectangle(width=0.7, height=registerHeight, fill_color=BLACK, fill_opacity=1).move_to(register.get_left(), LEFT).shift(RIGHT*0.08)
		self.components[1] = Rectangle(width=1.4, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[0], RIGHT, buff=0.08)
		self.components[2] = Rectangle(width=0.4, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[1], RIGHT, buff=0.08)
		self.components[3] = Rectangle(width=1.4, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[2], RIGHT, buff=0.08)
		self.components[4] = Rectangle(width=(0.7 if stage!=self.DECODE else 1.48), height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[3], RIGHT, buff=0.08)
		self.components[5] = Rectangle(width=0.7, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[4], RIGHT, buff=0.08)
		self.components[6] = Rectangle(width=0.7, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[5], RIGHT, buff=0.08)
		self.components[7] = Rectangle(width=0.7, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[6], RIGHT, buff=0.08)
		self.components[8] = Rectangle(width=0.64, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[7], RIGHT, buff=0.08)
		self.components[9] = Rectangle(width=0.78, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[8], RIGHT, buff=0.08)
		self.components[10] =	Rectangle(width=0.78, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[9], RIGHT, buff=0.08)
		self.components[11] =	Rectangle(width=0.84, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[10], RIGHT, buff=0.08)
		self.components[12] =	Rectangle(width=0.7, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[11], RIGHT, buff=0.08)
		self.components[13] =	Rectangle(width=0.6, height=registerHeight, fill_color=BLACK, fill_opacity=1).next_to(self.components[12], RIGHT, buff=0.08)

		self.componentsText:list[CodeBlock] = [
			CodeBlock("status", fontSize=20).move_to(self.components[0].get_center()),
			CodeBlock("insnbits" if stage==self.DECODE else "cond_holds", fontSize=20).move_to(self.components[1].get_center()),
			CodeBlock("op", fontSize=20).move_to(self.components[2].get_center()),
			CodeBlock("seq_succ_PC" if stage!=self.FETCH else "pred_PC", fontSize=20).move_to(self.components[3].get_center()),
			CodeBlock("X_sigs" if stage!=self.DECODE else "adrp_val", fontSize=20).move_to(self.components[4].get_center()),
			CodeBlock("M_sigs", fontSize=20).move_to(self.components[5].get_center()),
			CodeBlock("W_sigs", fontSize=20).move_to(self.components[6].get_center()),
			CodeBlock("ALU_op", fontSize=20).move_to(self.components[7].get_center()),
			CodeBlock("cond", fontSize=20).move_to(self.components[8].get_center()),
			CodeBlock("val_a" if stage==self.EXECUTE else "val_ex", fontSize=20).move_to(self.components[9].get_center()),
			CodeBlock("val_b", fontSize=20).move_to(self.components[10].get_center()),
			CodeBlock("val_imm" if stage==self.EXECUTE else "val_mem", fontSize=20).move_to(self.components[11].get_center()),
			CodeBlock("val_hw", fontSize=20).move_to(self.components[12].get_center()),
			CodeBlock("dst", fontSize=20).move_to(self.components[13].get_center())
		]

	def createSimplified(self) -> VGroup:
		register:Rectangle = self.submobjects[0].copy().move_to(ORIGIN)
		register.stretch_to_fit_height(0.75).stretch_to_fit_width(7)

		clock:Polygon = self.submobjects[1].copy()
		clock.move_to(register.get_right(), RIGHT)

		label:CodeBlock = self.submobjects[2].copy()
		label.next_to(clock, LEFT, buff=0.1)
		label.font_size = 16

		return VGroup(register, clock, label)