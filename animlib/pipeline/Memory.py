from manim import Rectangle, Succession, Animation, AnimationGroup, FadeIn, FadeOut
from manim import UP, DL, RIGHT, LEFT, DOWN
from manim import RED, BLUE, YELLOW, BLACK
from .core import Stage, Register
from .DMem import DMem
from ..hexdec import CodeBlock, Hexadecimal
from .Path import Path


class MemoryStage(Stage): 
	def __init__(self):
		super().__init__(4.5, 4)

		self.dmem = DMem().shift(UP*0.5)

		self.add(self.dmem)

	def animateDMem(self, wval:str, addr:str, rval:str, read:bool, write:bool, globalPaths:dict[str, Path]) -> Succession:
		anims:list[Animation|AnimationGroup] = []

		if self.dmem.wvalText:
			text = [self.dmem.wvalText, self.dmem.addrText]
			if self.dmem.rvalText: text.append(self.dmem.rvalText)

			anims.append(FadeOut(*text, shift=RIGHT))

		anims.append(
			FadeIn(
				self.dmem.setWVal(Hexadecimal(wval)),
				self.dmem.setAddr(Hexadecimal(addr)),
				shift=RIGHT
			)
		)

		# If no read or no write, then skip
		if read or write: 
			anims.append(self.dmem.setRead() if read else self.dmem.setWrite())
			anims.append(
				AnimationGroup(
					FadeIn(self.dmem.setRVal(Hexadecimal(rval)), shift=RIGHT),
					globalPaths["dmem_wvalmux"].highlight(BLUE, 4),
					self.dmem.setRead(False) if read else self.dmem.setWrite(False)
				)
			)

		anims.append(globalPaths["regfile_valbmux_dmem"].highlight(RED, 2))

		return Succession(*anims)

class MemoryPipeline(Register):
	def __init__(self):
		super().__init__(Register.MEMORY)

		for i in range(3, len(self.components)):
			if i in (3, 4, 7, 8, 11, 12):
				self.components[i] = None
				self.componentsText[i] = None

		# Used to store state for clock transition
		self.condholdsIn:CodeBlock = None
		self.seqSuccPCIn:Hexadecimal = None
		self.valExIn:Hexadecimal = None
		self.valBIn:Hexadecimal = None
		self.dstIn:Hexadecimal = None

		self.condholdsOut:CodeBlock = None
		self.seqSuccPCOut:Hexadecimal = None
		self.valExOut:Hexadecimal = None
		self.valBOut:Hexadecimal = None
		self.dstOut:Hexadecimal = None

		self.add(*filter(None, self.components), *filter(None, self.componentsText))

	def animateMin(self, condholds:str, valEx:str, valB:str, dst:str) -> FadeIn:
		self.condholdsIn = CodeBlock(condholds, fontSize=20).move_to(self.components[1].get_bottom()+UP*0.2)
		self.valExIn = Hexadecimal(valEx, fontSize=20).move_to(self.components[9].get_bottom()+UP*0.2)
		self.valBIn = Hexadecimal(valB, fontSize=20).move_to(self.components[10].get_bottom()+UP*0.2)
		self.dstIn = Hexadecimal(dst, fontSize=20).move_to(self.components[13].get_bottom()+UP*0.2)

		anim = FadeIn(self.condholdsIn, self.valExIn, self.valBIn, self.dstIn, shift=UP)

		return anim

	def animateMout(self, condholds:str, valEx:str, valB:str, dst:str):
		self.condholdsOut = CodeBlock(condholds, fontSize=20).move_to(self.components[1].get_top()+DOWN*0.15)
		self.valExOut = Hexadecimal(valEx, fontSize=20).move_to(self.components[9].get_top()+DOWN*0.15)
		self.valBOut = Hexadecimal(valB, fontSize=20).move_to(self.components[10].get_top()+DOWN*0.15)
		self.dstOut = Hexadecimal(dst, fontSize=20).move_to(self.components[13].get_top()+DOWN*0.15)

		anim = FadeIn(self.condholdsOut, self.valExOut, self.valBOut, self.dstOut, shift=UP)

		return anim

	def animateClock(self) -> Succession:
		anims:list[Animation] = []

		anims.append(AnimationGroup(self.submobjects[1].animate.set_fill(YELLOW, 1)))
		anims.append(FadeOut(self.condholdsOut,self.valExOut, self.valBOut, self.dstOut, shift=UP))
		anims.append(FadeOut(self.condholdsIn, self.valExIn, self.valBIn, self.dstIn, shift=UP))
		anims.append(self.animateMout(self.condholdsIn.value, self.valExIn.value, self.valBIn.value, self.dstIn.value))
		anims.append(AnimationGroup(self.submobjects[1].animate.set_fill(BLACK, 1)))

		return Succession(*anims)

class MemoryElements(Stage):
	def __init__(self):
		super().__init__(10, 3)

		stageLabel = CodeBlock("memory_instr", fontSize=35).move_to(self.submobjects[0].get_corner(DL)).shift(UP*0.5 + RIGHT*1.3)
		self.add(stageLabel)

		self.dmem = Rectangle(width=2, height=1.5).shift(RIGHT*3.28 + UP*0.5)
		self.dmemLabel = CodeBlock("dmem", fontSize=38).move_to(self.dmem.get_center())

		self.add(self.dmem, self.dmemLabel)

		self.valMemText:Hexadecimal = None

		self.instruction:CodeBlock = None

	def animateDmem(self, valB:str, valEx:str, valMem:str):
		anims = []

		if self.valMemText:
			anims.append(FadeOut(self.valBText, self.valExText, self.valMemText))

		self.valBText = Hexadecimal(valB, fontSize=20).next_to(self.dmem.get_bottom(), DOWN).shift(RIGHT*0.2)
		self.valExText = Hexadecimal(valEx, fontSize=20).next_to(self.dmem.get_left(), UP).shift(LEFT*0.2)
		self.valMemText = Hexadecimal(valMem, fontSize=20).next_to(self.dmem.get_top(), LEFT).shift(UP*0.15)

		anims.append(
			AnimationGroup(
				FadeIn(self.valBText, shift=UP), FadeIn(self.valExText, shift=RIGHT)
			)
		)

		anims.append(FadeIn(self.valMemText, shift=UP))

		return Succession(*anims)
	
	def animateInstruction(self, instr:str):
		anims = []

		if self.instruction:
			anims.append(FadeOut(self.instruction))

		self.instruction = CodeBlock(instr, fontSize=50).next_to(self.submobjects[0], RIGHT).shift(RIGHT*5)

		anims.append(FadeIn(self.instruction))

		return Succession(*anims)