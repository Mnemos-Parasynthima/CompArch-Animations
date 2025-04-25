from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from manim import *

from animlib.structs import *
from animlib.types import *
from animlib.mem import MemoryBlock
from animlib.funcs import inttstr
from animlib.hexdec import Hexadecimal

from numpy import array
from copy import deepcopy

PADDING_COLOR = GRAY

class Padding(Scene):
	def __init__(self):
		super().__init__()
		self.mem:MemoryBlock = None
		self.struct:Struct_T = None
		self.union:Union_T = None

		self.objs = [
			Type("ch1", "50", BLUE, TypeEnum.CHAR, fontSize=32),
			Type("i", "0x200", GREEN, TypeEnum.INT, fontSize=32),
			Type("s", "63", RED, TypeEnum.SHORT, fontSize=32),
			Type("s2", "50", PURPLE, TypeEnum.SHORT, fontSize=32)
		]

		self.struct = Struct_T("foo", self.objs, 32)
		structSize = self.struct.sizeof()

		self.mem = MemoryBlock(structSize, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal(inttstr(structSize-1)))
		self.mem.to_edge(RIGHT)

	def structFillMemory(self, padded=False, startIdx:int=0, ignorePaddings:list[bool]=None):
		memIdx = startIdx
		for i in range(len(self.struct)):
			self.play(self.struct.highlightProperty(i, YELLOW))
			# For the ith property of struct
			# How many bytes does it occupy (including padding?) in memory
			sizeof, paddingSize = self.struct.propSizeof(i)

			for _ in range(sizeof):
				self.play(self.mem.highlightByte(memIdx, self.struct[i]._color), run_time=0.4)
				memIdx += 1

			if padded or (ignorePaddings and not ignorePaddings[i]):
				for _ in range(paddingSize):
					self.play(self.mem.highlightByte(memIdx, PADDING_COLOR), run_time=0.4)
					memIdx += 1

			self.play(self.struct.dehighlightProperty(i))

	def unionFillMemory(self, activePropIdx:int=0):
		memIdx = 0
		self.play(self.union.highlightProperty(activePropIdx, YELLOW))
		sizeof, paddingSize = self.union.propSizeof(activePropIdx)
		color = self.union[activePropIdx]._color
		for i in range(sizeof):
			self.play(self.mem.highlightByte(memIdx, color), run_time=0.4)
			memIdx += 1

		for _ in range(paddingSize):
			self.play(self.mem.highlightByte(memIdx, PADDING_COLOR), run_time=0.4)
			memIdx += 1

		self.play(self.union.dehighlightProperty(activePropIdx))

	def intro(self):
		addrDef = Tex("Let $ADDR(x)$ be the address of x")
		addrDef.to_edge(UP)
		sizeDef = Tex("Let $SIZE(x)$ be the size of x")
		sizeDef.next_to(addrDef, DOWN)
		alignedDef = Tex("Let $IS\_ALIGNED(x)$ be true if $ADDR(x)$ mod $SIZE(x) = 0$")
		alignedDef.next_to(sizeDef, DOWN)

		subObjRule = Tex("Let SoR be the Sub-object Rule where every sub-object \\verb|x| has the property $IS\_ALIGNED(x)$ recursively").scale(0.85)
		subObjRule.next_to(alignedDef, DOWN * 3)
		arrRule = Tex("Let ArR be the Array Rule where every object \\verb|a| of type array in object \\verb|x| has the property $IS\_ALIGNED(a)$").scale(0.8)
		arrRule.next_to(subObjRule, DOWN)

		self.play(Write(addrDef))
		self.play(Write(sizeDef))
		self.play(Write(alignedDef))
		self.play(Write(subObjRule))
		self.play(Write(arrRule))

		self.play(FadeOut(addrDef, sizeDef, alignedDef, subObjRule, arrRule))

	def noPadding(self):
		self.play(FadeIn(self.struct, self.mem))
		# self.play(FadeIn(self.mem))

		# First show no padding, demonstrating how objects are not aligned
		self.structFillMemory()

		self.play(self.struct.animate.shift(LEFT * 4.83))

		iSizeN = self.struct[1].sizeof()
		iAddr = Tex("$ADDR(\\verb|i|) = \\verb|0x1|$")
		iSize = Tex(f"$SIZE(\\verb|i|) = {iSizeN}$")
		iSize.next_to(iAddr, RIGHT)
		iAddrSize = VGroup(iAddr, iSize).shift(LEFT)
		self.play(FadeIn(iAddr, iSize))

		pos = DOWN# + (RIGHT * 0.001)
		equ0 = Tex("$ADDR(\\verb|i|)$ mod $SIZE(\\verb|i|)$")
		equ0.next_to(iAddrSize, pos)

		equ1 = Tex(f"$\\verb|0x1|$ mod ${iSizeN}$")
		equ1.next_to(iAddrSize, pos)
		res = Tex(f"${1%iSizeN}$")
		res.next_to(iAddrSize, pos)

		self.play(FadeIn(equ0))
		self.play(ReplacementTransform(equ0, equ1))
		self.play(ReplacementTransform(equ1, res))

		conclusion = Tex(f"FAILED SoR")
		conclusion.next_to(iAddrSize, UP)

		self.play(FadeIn(conclusion), conclusion.animate.set_color(RED))

		self.play(FadeOut(conclusion, res, iAddrSize), self.mem.dehighlightBytes())

	def paddingSoR(self):
		# Show that it is now aligned with padding (no focus on ArR yet)
		title = Text("With Padding", font="Helvetica")
		title.to_edge(UP)
		self.play(Write(title))

		# self.play(FadeIn(self.struct, self.mem))
		
		self.structFillMemory(True)

		# self.play(self.struct.animate.shift(LEFT * 4.8))

		conclusion = Tex(f"$IS\_ALIGNED(\\forall e \\in {self.struct.structName} )$")
		sor = Tex("SoR")
		sor.next_to(conclusion, UP)

		self.play(FadeIn(conclusion), conclusion.animate.set_color(GREEN))

		self.wait(0.3)

		self.play(FadeOut(conclusion), self.mem.dehighlightBytes())

	def paddingArR(self):
		# self.play(FadeIn(self.struct, self.mem))
		# self.play(self.struct.animate.shift(LEFT * 4.83))

		# Swap elements to demonstrate ArR
		self.play(self.struct.swap(1, 3))
		self.play(self.struct.swap(2, 3))

		self.structFillMemory(ignorePaddings=[False, False, False, True])

		self.play(self.mem.animate.shift(LEFT * 1.15))

		structSize = Tex(f"$10$")

		# Show SoR met


		# Show as an array
		mem2 = MemoryBlock(20, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal("0x14"))
		mem2.to_edge(RIGHT)
		self.play(TransformFromCopy(self.mem, mem2))
		


		array = VGroup(*[
			Text(f"struct {self.struct.structName} structs[] {{", font_size=20, font="Helvetica"),
			Text(f"struct {self.struct.structName} s0;", font_size=20, font="Helvetica"),
			Text(f"struct {self.struct.structName} s1;", font_size=20, font="Helvetica"),
			Text("};", font_size=20, font="Helvetica")
		])
		array.arrange(DOWN, aligned_edge=LEFT).to_edge(UP, buff=1.5)
		array.submobjects[1].shift(RIGHT * 0.2)
		array.submobjects[2].shift(RIGHT * 0.2)

		self.play(FadeIn(array))


		memIdx = 0
		anims = []
		for i in range(4):
			sizeof, paddingSize = self.struct.propSizeof(i)

			for _ in range(sizeof):
				anims.append(mem2.highlightByte(memIdx, self.struct[i]._color))
				memIdx += 1

			if i != 3:
				for _ in range(paddingSize):
					anims.append(mem2.highlightByte(memIdx, PADDING_COLOR))
					memIdx += 1

		self.play(array.submobjects[1].animate.set_color(YELLOW), AnimationGroup(*anims))
		anims.clear()
		self.play(array.submobjects[1].animate.set_color(WHITE))

		anims.append(mem2.showLabel(10))
		for i in range(4):
			sizeof, paddingSize = self.struct.propSizeof(i)

			for _ in range(sizeof):
				anims.append(mem2.highlightByte(memIdx, self.struct[i]._color))
				memIdx += 1

			if i != 3:
				for _ in range(paddingSize):
					anims.append(mem2.highlightByte(memIdx, PADDING_COLOR))
					memIdx += 1

		self.play(array.submobjects[2].animate.set_color(YELLOW), AnimationGroup(*anims))
		self.wait(0.2)
		self.play(array.submobjects[2].animate.set_color(WHITE))

		# Show that the second struct is not aligned, thus ArR not met

		iAddr = Tex("$ADDR(\\verb|structs[1].i|)$  $SIZE(\\verb|structs[1].i|)$").scale(0.65)
		self.play(mem2.showLabel(14), FadeIn(iAddr))

		equ0 = Tex("$ADDR(\\verb|structs[1].i|)$ mod $SIZE(\\verb|structs[1].i|)$").scale(0.55)
		equ0.next_to(iAddr, DOWN)
		self.play(FadeIn(equ0))

		equ1 = Tex(f"\\verb|0xe| mod $4$")
		equ1.next_to(iAddr, DOWN)
		self.play(FadeTransform(equ0, equ1))

		res = Tex(f"${14%4}$")
		res.next_to(iAddr, DOWN)
		self.play(FadeTransform(equ1, res))

		# structs[1].i is not aligned thus,
		# structs[1] fails SoR thus,
		# struct fails ArR
		conclusion0 = Tex("NOT $IS\_ALIGNED(\\verb|structs[1].i|)$").scale(0.8)
		conclusion0.next_to(iAddr, UP, buff=0.1).set_color(RED)
		self.play(FadeIn(conclusion0))
		self.wait(0.2)

		conclusion1 = Tex("\\verb|structs[1]| fails SoR")
		conclusion1.next_to(iAddr, UP).set_color(RED)
		self.play(ReplacementTransform(conclusion0, conclusion1))
		self.wait(0.2)

		conclusion2 = Tex("\\verb|struct| fails ArR")
		conclusion2.next_to(iAddr, UP).set_color(RED)
		self.play(FadeTransform(conclusion1, conclusion2))

		self.wait(0.1)

		self.play(FadeOut(conclusion2, iAddr, res), self.mem.dehighlightBytes(), mem2.dehighlightBytes())

		# Add padding to the end (for both structs) to show SoR and ArR are met
		mem3 = MemoryBlock(24, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal("0x18"), start=0x0, end=0x18)
		mem3.move_to(mem2.get_center())
		self.play(ReplacementTransform(mem2, mem3))

		del mem2

		self.structFillMemory(True, 0)

		memIdx = 0
		anims = []
		for i in range(4):
			sizeof, paddingSize = self.struct.propSizeof(i)

			for _ in range(sizeof):
				anims.append(mem3.highlightByte(memIdx, self.struct[i]._color))
				memIdx += 1

			for _ in range(paddingSize):
				anims.append(mem3.highlightByte(memIdx, PADDING_COLOR))
				memIdx += 1

		self.play(array.submobjects[1].animate.set_color(YELLOW), AnimationGroup(*anims))
		anims.clear()
		self.play(array.submobjects[1].animate.set_color(WHITE))

		anims.append(mem3.showLabel(12))
		for i in range(4):
			sizeof, paddingSize = self.struct.propSizeof(i)

			for _ in range(sizeof):
				anims.append(mem3.highlightByte(memIdx, self.struct[i]._color))
				memIdx += 1

			for _ in range(paddingSize):
				anims.append(mem3.highlightByte(memIdx, PADDING_COLOR))
				memIdx += 1

		self.play(array.submobjects[2].animate.set_color(YELLOW), AnimationGroup(*anims))
		self.wait(0.2)
		self.play(array.submobjects[2].animate.set_color(WHITE))

		conclusion = Tex(f"$IS\_ALIGNED(\\verb|{self.struct.structName}|)$").set_color(GREEN)
		self.play(FadeIn(conclusion))

	def unionIntro(self):
		self.union = Union_T("buzz", self.objs, 32)
		unionSize = self.union.sizeof()

		self.mem = MemoryBlock(unionSize, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal(inttstr(unionSize-1)))
		self.mem.to_edge(RIGHT)

		self.play(FadeIn(self.union, self.mem))

		for i, obj in enumerate(self.union.objs):
			self.unionFillMemory(i)
			self.play(self.mem.dehighlightBytes())

		sizeofText = Tex(f"$SIZE(\\verb|union|) = max(\\forall elem \\in \\verb|union| \\vert SIZE(elem))$")
		sizeofText.to_edge(DOWN)

		memIdx = 0
		anims = []
		sizeof, paddingSize = self.union.propSizeof(1)

		for _ in range(sizeof):
			anims.append(self.mem.highlightByte(memIdx, self.union[1]._color))
			memIdx += 1

		for _ in range(paddingSize):
			anims.append(self.mem.highlightByte(memIdx, PADDING_COLOR))
			memIdx += 1

		self.play(FadeIn(sizeofText), self.union.highlightProperty(1, YELLOW), AnimationGroup(*anims))

		self.wait(0.2)

		self.play(FadeOut(sizeofText), self.union.dehighlightProperty(1), self.mem.dehighlightBytes())
		self.play(self.union.animate.shift(LEFT * 5))

		mem2 = MemoryBlock(unionSize*4, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal(inttstr(4*unionSize-1)))
		mem2.to_edge(RIGHT)

		self.play(ReplacementTransform(self.mem, mem2))
		self.mem = mem2

		array = VGroup(*[
			Text(f"union {self.union.unionName} unions[] {{", font_size=32, font="Helvetica"),
			Text(f"union {self.union.unionName} u0;", font_size=32, font="Helvetica"),
			Text(f"union {self.union.unionName} u1;", font_size=32, font="Helvetica"),
			Text(f"union {self.union.unionName} u2;", font_size=32, font="Helvetica"),
			Text(f"union {self.union.unionName} u3;", font_size=32, font="Helvetica"),
			Text("};", font_size=32, font="Helvetica")
		])
		array.arrange(DOWN, aligned_edge=LEFT)#.to_edge(UP, buff=1.5)
		array.submobjects[1].shift(RIGHT * 0.2)
		array.submobjects[2].shift(RIGHT * 0.2)
		array.submobjects[3].shift(RIGHT * 0.2)
		array.submobjects[4].shift(RIGHT * 0.2)

		self.play(FadeIn(array))

		memIdx = 0

		for i in range(4):
			self.play(array.submobjects[i+1].animate.set_color(GREEN))

			anims = []
			for j in range(4):
				anims.append(self.mem.highlightByte(memIdx, GREEN))
				memIdx += 1
				# self.play(self.mem.highlightByte(memIdx, GREEN), run_time=0.4)
			self.play(AnimationGroup(*anims))
			self.wait(0.2)
			self.play(array.submobjects[i+1].animate.set_color(WHITE))

	def unionStruct(self):
		pass

	def construct(self):
		# self.intro()

		# self.noPadding()

		# self.paddingSoR()

		# self.paddingArR()

		# # self.clear()

		# self.unionIntro()

		# self.clear()

		self.unionStruct()

		# arrobjs = [
		# 	Type("a0", "20", GREEN, TypeEnum.CHAR), Type("a1", "20", GREEN, TypeEnum.CHAR), Type("a2", "20", GREEN, TypeEnum.CHAR),
		# 	Type("a3", "20", GREEN, TypeEnum.CHAR), Type("a4", "20", GREEN, TypeEnum.CHAR), Type("a5", "20", GREEN, TypeEnum.CHAR)
		# ]
		# arr = Array_T("arr", "char", arrobjs)
		# self.play(FadeIn(arr))


		# objs = [
		# 	Type("ch1", "50", BLUE, TypeEnum.CHAR, fontSize=32),
		# 	Type("i", "0x200", GREEN, TypeEnum.POINTER, TypeEnum.INT, fontSize=32),
		# 	Type("s", "63", RED, TypeEnum.SHORT, fontSize=32),
		# 	Type("ch2", "50", PURPLE, TypeEnum.CHAR, fontSize=32)
		# ]

		# objss = [
		# 	Type("ch1", "50", BLUE, TypeEnum.CHAR, fontSize=32),
		# 	Type("s", "63", RED, TypeEnum.SHORT, fontSize=32),
		# 	Type("i", "0x200", GREEN, TypeEnum.POINTER, TypeEnum.INT, fontSize=32),
		# 	Type("ch2", "50", PURPLE, TypeEnum.CHAR, fontSize=32)
		# ]

		# struct = Struct_T("ping", objs, 32)
		# structSize = struct.sizeof()
		# struct.to_edge(LEFT)
		# self.play(FadeIn(struct))

		# print(struct[1].symbol, struct[2].symbol, struct.sizeof(), struct.paddings)
		# self.play(struct.swap(1, 2))
		# print(struct[1].symbol, struct[2].symbol, struct.sizeof(), struct.paddings)

		# sstruct = Struct("pong", objss, 32)
		# sstruct.to_edge(RIGHT)
		# self.play(FadeIn(sstruct))
		# print(sstruct.paddings)

		# union = Union_("pong", objs, 32)
		# self.play(FadeIn(union))

		# print(union[1].symbol, union[2].symbol, union.sizeof(), union.paddings)
		# self.play(union.swap(1, 2))
		# print(union[1].symbol, union[2].symbol, union.sizeof(), union.paddings)

		# table = StructTable(struct).scale(0.5)
		# table.move_to(ORIGIN + array((3,0,0)))
		# self.play(FadeIn(table))
		# self.play(table.highlightRow(1, GREEN))


		# mem = MemoryBlock(structSize, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal(inttstr(structSize-1)))
		# mem.to_edge(RIGHT)
		# self.play(FadeIn(mem))

		# memIdx = 0
		# for i in range(len(struct)):
		# 	self.play(struct.highlightProperty(i, YELLOW))
		# 	# For the ith property of struct
		# 	# How many bytes does it occupy (including padding?) in memory
		# 	sizeof, paddingSize = struct.propSizeof(i)

		# 	# Highlight the actual byte contents
		# 	for _ in range(sizeof):
		# 		# print(memIdx)
		# 		self.play(mem.highlightByte(memIdx, struct[i]._color))
		# 		memIdx += 1

		# 	for _ in range(paddingSize):
		# 		self.play(mem.highlightByte(memIdx, PADDING_COLOR))
		# 		memIdx += 1

		# 	self.play(struct.dehighlightProperty(i))
		# self.play(mem.dehighlightBytes())

		# memIdx = 0
		# self.play(union.highlightProperty(0, YELLOW))
		# sizeof, paddingSize = union.propSizeof(0)
		# for i in range(sizeof):
		# 	self.play(mem.highlightByte(memIdx, union[i]._color))
		# 	memIdx += 1

		# for _ in range(paddingSize):
		# 	self.play(mem.highlightByte(memIdx, PADDING_COLOR))
		# 	memIdx += 1

		# self.play(mem.dehighlightBytes())



		self.wait(2)



if __name__ == "__main__":
	# main()

	scene = Padding()
	scene.render()