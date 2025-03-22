from manim import UP, Rectangle, DL, RIGHT, Succession, Animation, AnimationGroup, FadeIn, RED, BLUE, FadeOut
from .core import Stage, Register
from .DMem import DMem
from ..hexdec import CodeBlock, Hexadecimal
from .Path import Path


class MemoryStage(Stage): 
	def __init__(self):
		super().__init__(4.5, 4)

		self.dmem = DMem().shift(UP*0.5)

		self.add(self.dmem)

	def animateDMem(self, wval:str, addr:str, rval:str, globalPaths:dict[str, Path]) -> Succession:
		anims:list[Animation|AnimationGroup] = []

		if self.dmem.wvalText:
			anims.append(
				FadeOut(
					self.dmem.wvalText, self.dmem.addrText, self.dmem.rvalText,
					shift=RIGHT
				)
			)

		anims.append(
			FadeIn(
				self.dmem.setWVal(Hexadecimal(wval)),
				self.dmem.setAddr(Hexadecimal(addr)),
				shift=RIGHT
			)
		)

		# If no read or write, then no setRVal()
		# anims.append(
		# 	AnimationGroup(
		# 		self.dmem.setRead(),
		# 		self.dmem.setWrite()
		# 	)
		# )

		anims.append(
			AnimationGroup(
				globalPaths["regfile_valbmux_dmem"].highlight(RED, 2),
				FadeIn(self.dmem.setRVal(Hexadecimal(rval)), shift=RIGHT),
				globalPaths["dmem_wvalmux"].highlight(BLUE, 4)
			)
		)

		return Succession(*anims)

class MemoryPipeline(Register):
	def __init__(self):
		super().__init__(Register.MEMORY)

		for i in range(4, len(self.components)):
			if i in (4, 7, 8, 11, 12):
				self.components[i] = None
				self.componentsText[i] = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

class MemoryElements(Stage):
	def __init__(self):
		super().__init__(10, 3)

		stageLabel = CodeBlock("memory_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.3)
		self.add(stageLabel)

		self.dmem = Rectangle(width=2, height=1.5).shift(RIGHT*3.28 + UP*0.5)
		self.dmemLabel = CodeBlock("dmem", fontSize=38).move_to(self.dmem.get_center())

		self.add(self.dmem, self.dmemLabel)