from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.cache import Cache
from animlib.cpu import CPU
from animlib.mem import Memory, SplittableAddress
from animlib.hexdec import Hexadecimal

from manim import *


class CacheRead(Scene):
	def __init__(self):
		super().__init__()

		self.wordsize = 16
		self.cpu:CPU = None
		self.cache = None
		self.mem:Memory = None

	def hit(self):
		addrn = 0xa0ef

		self.cpu = CPU().to_edge(LEFT, buff=-0.4).scale(0.75)
		self.cache = Cache(2, 4, 64, self.wordsize).to_edge(RIGHT, buff=-0.5).shift(DOWN * 0.5)
		self.cache.initBytes([(addrn, 0xfe, 0), (addrn+1, 0xae, 0), (addrn+0xa, 0x12, 0)])
		self.cache.scale(0.85)

		title = Text("Cache Hit").to_edge(UP)

		self.play(FadeIn(self.cpu, self.cache), Write(title))

		addr = SplittableAddress(addrn).move_to(self.cpu.get_center())
		addr.generate_target()
		addr.target.next_to(title, DOWN)

		self.play(MoveToTarget(addr))

		binaddr = SplittableAddress(addrn, [self.cache.t, self.cache.s, self.cache.b], True, 0.25).next_to(addr, DOWN)
		self.play(TransformFromCopy(addr, binaddr))

		taghex = Tex(f"\\verb|t={hex(int(binaddr.getGroup(0).value, 2))}|").to_corner(UR)
		setihex = Tex(f"\\verb|s={hex(int(binaddr.getGroup(1).value, 2))}|").next_to(taghex, DOWN)
		offsethex = Tex(f"\\verb|b={hex(int(binaddr.getGroup(2).value, 2))}|").next_to(setihex, DOWN)
		
		self.play(binaddr.highlightGroup(1), Write(setihex)) # highlight set in cache
		self.play(binaddr.highlightGroup(0), Write(taghex)) # highlight tag
		self.play(binaddr.highlightGroup(2), Write(offsethex)) # highlight offset in iteration

		_, bytehex = self.cache.getByte(addrn)
		copyByte = bytehex.copy()
		self.play(bytehex.animate.set_color(YELLOW))
		self.play(copyByte.animate.move_to(self.cpu.getRegisters()[0].get_center()), bytehex.animate.set_color(WHITE))

		self.wait(0.3)

		self.play(
			FadeOut(copyByte, self.cache, self.cpu, binaddr, addr, taghex, setihex, offsethex),
			Unwrite(title)
		)

	def missNR(self):
		addrn = 0x9bd8

		# self.cpu = CPU().to_edge(LEFT, buff=-0.4).scale(0.7)
		# self.cache = Cache(2, 4, 64, self.wordsize)
		self.cache.move_to(ORIGIN)
		self.cache.initBytes([(0xae43, 0xde, 0), (0xdead, 0x32, 0), (0xbeef, 0x32, 0), (0xfeed, -0xed, 0), (0x1023, 0x0f, 0)])
		self.cache.scale(0.75)

		title = Text("Cache Miss, No Replacement", font_size=40).to_edge(UP)
		self.play(Write(title))

		self.mem = Memory(2, 4)
		self.mem.to_edge(RIGHT, buff=-0.4).scale(0.8)
		self.cache.move_to(ORIGIN + LEFT * 0.5)

		self.play(FadeIn(self.mem, self.cpu, self.cache))
		
		addr = SplittableAddress(addrn).move_to(self.cpu.get_center())
		addr.generate_target()
		addr.target.next_to(title, DOWN)

		self.play(MoveToTarget(addr))

		binaddr = SplittableAddress(addrn, [self.cache.t, self.cache.s, self.cache.b], True, 0.25).next_to(addr, DOWN)
		self.play(TransformFromCopy(addr, binaddr))

		taghex = Tex(f"\\verb|t={hex(int(binaddr.getGroup(0).value, 2))}|").to_corner(UL)
		setihex = Tex(f"\\verb|s={hex(int(binaddr.getGroup(1).value, 2))}|").next_to(taghex, DOWN)
		offsethex = Tex(f"\\verb|b={hex(int(binaddr.getGroup(2).value, 2))}|").next_to(setihex, DOWN)
		
		self.play(binaddr.highlightGroup(1), Write(setihex)) # highlight set in cache
		self.play(binaddr.highlightGroup(0), Write(taghex)) # highlight tag
		self.play(binaddr.highlightGroup(2), Write(offsethex)) # highlight offset in iteration

		self.play(self.cache.highlightSet(6, 0, RED), self.cache.highlightSet(6, 1, RED))
		self.wait(0.2)
		self.play(self.cache.dehighlightSet(6, 0), self.cache.dehighlightSet(6, 1))

		addrbytes = [addr.getGroup(0).copy().scale(0.5), addr.getGroup(1).copy().scale(0.5)]
		self.play(self.mem.setAddr(addrbytes), self.mem.setRE())

		databytes = [
			Hexadecimal("20", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.2),
			Hexadecimal("23", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.4),
			Hexadecimal("ae", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.6), 
			Hexadecimal("d2", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.8)
		]
		self.play(self.mem.setData(databytes))

		self.play(*[self.cache.setByte(addrn+i, databytes[i], 1) for i in range(4)])

		_, bytehex = self.cache.getByte(addrn)
		copyByte = bytehex.copy()
		self.play(bytehex.animate.set_color(YELLOW))
		self.play(copyByte.animate.move_to(self.cpu.getRegisters()[0].get_center()), FadeOut(bytehex))
		# bytehex is somehow a different object/image than its "origin"

		self.wait(0.3)

		self.play(
			FadeOut(self.cache, self.cpu, self.mem, binaddr, addr, taghex, setihex, offsethex, copyByte),
			Unwrite(title)
		)

	def missR(self): 
		addrn = 0x9bd8

		# self.cpu = CPU().to_edge(LEFT, buff=-0.4).scale(0.7)
		self.cache = Cache(2, 4, 64, self.wordsize)
		self.cache.move_to(ORIGIN)
		self.cache.initBytes([
			(0xae43, 0xde, 0), (0x1023, 0x0f, 1), # set 0
			(0x4967, 0xa0, 1), (0x5b26, 0xad, 0), # set 1
			(0x496b, 0xaa, 0), (0x772a, 0x11, 1), # ....
			(0xdead, 0x32, 0), (0xbeef, 0x32, 0),
			(0xdd70, 0x12, 1), (0x7771, 0x71, 0),
			(0x9534, 0x95, 0), (0x5b15, 0x5b, 0),
			(0xfb38, 0x38, 0), (0x5b19, 0x19, 1),
			(0xfb3c, 0xc3, 0), (0x671d, 0x1d, 0)
		])
		self.cache.scale(0.7)

		title = Text("Cache Miss, Replacement", font_size=40).to_edge(UP)
		self.play(Write(title))

		self.mem = Memory(2, 4)
		self.mem.to_edge(RIGHT, buff=-0.4).scale(0.8)
		self.cache.move_to(ORIGIN + LEFT * 0.5)

		self.play(FadeIn(self.mem, self.cpu, self.cache))
		
		addr = SplittableAddress(addrn).move_to(self.cpu.get_center())
		addr.generate_target()
		addr.target.next_to(title, DOWN)

		self.play(MoveToTarget(addr))

		binaddr = SplittableAddress(addrn, [self.cache.t, self.cache.s, self.cache.b], True, 0.25).next_to(addr, DOWN)
		self.play(TransformFromCopy(addr, binaddr))

		taghex = Tex(f"\\verb|t={hex(int(binaddr.getGroup(0).value, 2))}|").to_corner(UL)
		setihex = Tex(f"\\verb|s={hex(int(binaddr.getGroup(1).value, 2))}|").next_to(taghex, DOWN)
		offsethex = Tex(f"\\verb|b={hex(int(binaddr.getGroup(2).value, 2))}|").next_to(setihex, DOWN)
		
		self.play(binaddr.highlightGroup(1), Write(setihex)) # highlight set in cache
		self.play(binaddr.highlightGroup(0), Write(taghex)) # highlight tag
		self.play(binaddr.highlightGroup(2), Write(offsethex)) # highlight offset in iteration

		self.play(self.cache.highlightSet(6, 0, RED), self.cache.highlightSet(6, 1, RED))
		self.wait(0.2)
		self.play(self.cache.dehighlightSet(6, 0), self.cache.dehighlightSet(6, 1))

		addrbytes = [addr.getGroup(0).copy().scale(0.5), addr.getGroup(1).copy().scale(0.5)]
		self.play(self.mem.setAddr(addrbytes), self.mem.setRE())

		databytes = [
			Hexadecimal("20", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.2),
			Hexadecimal("23", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.4),
			Hexadecimal("ae", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.6), 
			Hexadecimal("d2", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(1).get_top()+DOWN*0.8)
		]
		self.play(self.mem.setData(databytes))

		caption = Text("Selecting based on LRU").to_edge(DOWN)
		self.play(Write(caption), self.cache.highlightSet(6, 0, YELLOW))
		self.wait(0.2)
		# self.play(self.cache.dehighlightSet(6, 0))

		self.play(*[self.cache.setByte(addrn+i, databytes[i], 0) for i in range(4)])

		_, bytehex = self.cache.getByte(addrn)
		copyByte = bytehex.copy()
		# self.play(bytehex.animate.set_color(YELLOW))
		self.play(copyByte.animate.move_to(self.cpu.getRegisters()[0].get_center()), FadeOut(bytehex))

		self.wait(0.3)

		self.play(FadeOut(copyByte, self.cache, self.cpu, self.mem, binaddr, addr, taghex, setihex, offsethex, title, caption))

	def construct(self):
		self.hit()
		
		self.wait(0.5)

		self.missNR()

		self.wait(1)

		self.missR()

		self.wait(2)