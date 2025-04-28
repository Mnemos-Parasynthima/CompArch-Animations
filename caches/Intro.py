from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from manim import *

from animlib.mem import MemoryBlock, Memory
from animlib.cache import Cache
from animlib.hexdec import Hexadecimal
from animlib.cpu import CPU


class Intro(Scene):
	def __init__(self):
		super().__init__()

		self.mem:Memory = None
		self.cpu:CPU = None
		self.cache:Rectangle|Cache = None

	def moveBetweenRegisters(self, dataDot:Dot, cycles:int):
		dataDot.set_color(GREEN)
		# Assuming dot is already at register, going to alu
		anims = [ 
			dataDot.animate(rate_func=linear, run_time=0.75).move_to(self.cpu.getALU().get_center()).build() if i % 2 == 0 else 
			dataDot.animate(rate_func=linear, run_time=0.75).move_to(self.cpu.getRegisters()[0].get_center()).build() for i in range(cycles)
		]
		self.play(Succession(*anims, lag_ratio=1))

	def moveBetweenCPUMemory(self, dataDot:Dot, cycles:int):
		dataDot.set_color(RED)
		# Assuming dot is already at cpu, start going to mem
		anims = [ 
			dataDot.animate(rate_func=linear, run_time=4).move_to(self.mem.getMemoryBlock(0).get_center()).build() if i % 2 == 0 else 
			dataDot.animate(rate_func=linear, run_time=4).move_to(self.cpu.getRegisters()[0].get_center()).build() for i in range(cycles)
		]
		self.play(Succession(*anims, lag_ratio=1))

	def moveBetweenCPUCache(self, dataDot:Dot, cycles:int):
		dataDot.set_color(ORANGE)
		# Assuming dot is already at cpu, start going to cache
		anims = [ 
			dataDot.animate(rate_func=linear, run_time=1).move_to(self.cache.get_left()).build() if i % 2 == 0 else 
			dataDot.animate(rate_func=linear, run_time=1).move_to(self.cpu.getRegisters()[0].get_center()).build() for i in range(cycles)
		]
		self.play(Succession(*anims, lag_ratio=1))

	def moveBetweenCacheCPU(self, dataDot:Dot, cycles:int):
		dataDot.move_to(self.cache.get_left()).set_color(ORANGE)
		# This is slightly different than moveBetweenCPUCache as here,
		# it is assuming that the dot starts from cache after doing a memory access
		anims = [ 
			dataDot.animate(rate_func=linear, run_time=1).move_to(self.cpu.getRegisters()[0].get_center()).build() if i % 2 == 0 else 
			dataDot.animate(rate_func=linear, run_time=1).move_to(self.cache.get_left()).build() for i in range(cycles)
		]
		self.play(Succession(*anims, lag_ratio=1))

	def moveBetweenCacheMemory(self, dataDot:Dot, cycles:int):
		dataDot.move_to(self.cache.get_right()).set_color(RED)
		# Assuming dot is already at cache, start going to mem
		anims = [ 
			dataDot.animate(rate_func=linear, run_time=2).move_to(self.mem.getMemoryBlock(0).get_center()).build() if i % 2 == 0 else 
			dataDot.animate(rate_func=linear, run_time=2).move_to(self.cache.get_right()).build() for i in range(cycles)
		]
		self.play(Succession(*anims, lag_ratio=1))

	def showLatency(self):
		self.mem = Memory(8, 8)
		self.mem.to_edge(RIGHT)

		self.cpu = CPU().scale(0.8)
		self.cpu.to_edge(LEFT)

		self.play(FadeIn(self.mem, self.cpu))
		
		# Have a dot move between regs and alu fast
		# Then have a dot move between cpu/regs and mem slow
		dataDot = Dot(self.cpu.getRegisters()[0].get_center())
		self.play(FadeIn(dataDot))

		self.moveBetweenRegisters(dataDot, 3)
		
		self.moveBetweenCPUMemory(dataDot, 3)

		# Introduce a box in the middle for "small fast memory"
		# Have dots move to showcase it
		# Rename to "cache"
		self.cache = Square(3.75).shift(LEFT*0.85)
		cacheText = Text("Small\nFast\nMemory", font="Helvetica").move_to(self.cache.get_center())
		self.play(FadeIn(self.cache, cacheText))

		self.moveBetweenRegisters(dataDot, 2)

		self.moveBetweenCPUCache(dataDot, 2)

		self.moveBetweenRegisters(dataDot, 2)

		self.moveBetweenCPUCache(dataDot, 1)

		self.moveBetweenCacheMemory(dataDot, 2)

		self.moveBetweenCacheCPU(dataDot, 3)

		self.moveBetweenRegisters(dataDot, 4)

		self.play(ReplacementTransform(cacheText, Text("Cache", font="Helvetica").move_to(self.cache.get_center())))

		self.wait(0.2)
		self.play(FadeOut(self.cpu, self.mem, self.cache))

	def buildUp(self):
		letC = MathTex("\\text{Let } C = 16").scale(0.75).to_corner(UL)
		self.play(Write(letC))

		size = 16

		cache = MemoryBlock(size, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal("0xf"), start=0x0, end=0xf)

		cache2 = VGroup(MemoryBlock(size//2, MemoryBlock.VERTICAL, Hexadecimal("0x0"), Hexadecimal("0xe")), 
									  MemoryBlock(size//2, MemoryBlock.VERTICAL, Hexadecimal("0x1"), Hexadecimal("0xf")))
		cache2.arrange(RIGHT, buff=1)

		cache3 = VGroup(*[MemoryBlock(size//4, MemoryBlock.VERTICAL, None, None) for _ in range(4)])
		cache3.arrange(RIGHT, buff=0.5)

		self.play(FadeIn(cache))
		self.wait(0.5)
		self.play(ReplacementTransform(cache, cache2))
		self.wait(0.5)
		self.play(ReplacementTransform(cache2, cache3))

		caption = Text("Unit of Memory Transfer: block", font="Helvetica").to_edge(DOWN)
		self.play(Write(caption))

		anims:list[Rectangle] = [ cache3.submobjects[i].highlightByte(0, YELLOW) for i in range(4) ]

		letB = MathTex("\\text{Let } B = 4").scale(0.75).next_to(letC, DOWN, buff=0.2, aligned_edge=LEFT)
		title = Text("One block: size of 4 KB", font="Helvetica").to_edge(UP)
		self.play(Write(title), Write(letB), *anims)

		cachebox = Rectangle(width=6.5, height=4)
		text = Text("Simple Cache", font="Helvetica").to_edge(UP)
		text2 = Text("Cache line", font="Helvetica").next_to(cache3.submobjects[3].blocks[0], RIGHT, buff=0.5)
		self.play(ReplacementTransform(title, text), ReplacementTransform(caption, text2), FadeIn(cachebox))
		cachegroup = VGroup(cache3, cachebox)

		self.cache = Cache(1, 4, size, 16)
		title = Text("Simple Direct Mapped Cache", font_size=30, font="Helvetica").to_edge(UP)
		self.play(ReplacementTransform(cachegroup, self.cache), FadeOut(text2), ReplacementTransform(text, title))



		self.play(self.cache.ways[0].sets[0].tagText.animate.set_color(YELLOW))
		self.play(FadeIn(Text("Tag", font="Helvetica").to_edge(DOWN).shift(LEFT*4)))

		self.play(self.cache.ways[0].sets[0].validText.animate.set_color(YELLOW))
		self.play(FadeIn(Text("Valid Bit", font="Helvetica").to_edge(DOWN).shift(RIGHT*4)))

		self.play(self.cache.ways[0].sets[0].dirtyText.animate.set_color(YELLOW))
		self.play(FadeIn(Text("Dirty Bit", font="Helvetica").to_edge(DOWN)))

		self.play(self.cache.highlightSet(0, 0, YELLOW))
		self.play(FadeIn(Text("Set", font="Helvetica").next_to(self.cache, LEFT, buff=2)))

		self.play(
			AnimationGroup(
			self.cache.highlightSet(1, 0, YELLOW),
			self.cache.highlightSet(2, 0, YELLOW),
			self.cache.highlightSet(3, 0, YELLOW))
		)
		self.play(FadeIn(Text("Way", font="Helvetica").next_to(self.cache, UP)))

	def construct(self):
		self.showLatency()

		self.clear()

		self.buildUp()

		self.wait(2)