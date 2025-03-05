from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.cache import Cache
from animlib.cpu import CPU
from animlib.mem import Memory, SplittableAddress
from animlib.hexdec import Hexadecimal

from manim import *


class CacheWrite(Scene):
	def __init__(self):
		super().__init__()

		self.wordsize = 16
		self.cpu:CPU = None
		self.cache = None
		self.mem:Memory = None

	def hit(self):
		addrn = 0xa0ef

		self.cpu = CPU().to_edge(LEFT, buff=-0.4).scale(0.75)
		self.cache = Cache(2, 4, 64, self.wordsize).to_edge(RIGHT, buff=-0.25).shift(DOWN * 0.5).scale(0.9)
		self.cache.initBytes([(addrn-2, 0xe2, 0), (0xfe00, 0x32, 0), (0xa0de, 0xe2, 0), (0x6b6e, 0x93, 0)])
		self.mem = Memory(2, 4)

		title = Text("Cache Hit").to_edge(UP)

		self.play(FadeIn(self.cpu, self.cache), Write(title))

		addr = SplittableAddress(addrn).move_to(self.cpu.get_center())
		addr.generate_target()
		addr.target.next_to(title, DOWN)

		databyte = Hexadecimal("d2", fontSize=30).move_to(self.cpu.getRegisters()[3].get_center())
		databyte.generate_target().next_to(self.cpu, RIGHT, 1.5)#.scale(1.5)

		self.play(MoveToTarget(addr), MoveToTarget(databyte))
		# databyte.scale(0.7)

		binaddr = SplittableAddress(addrn, [self.cache.t, self.cache.s, self.cache.b], True, 0.25).next_to(addr, DOWN)
		self.play(TransformFromCopy(addr, binaddr))

		taghex = Tex(f"\\verb|t={hex(int(binaddr.getGroup(0).value, 2))}|").to_corner(UL)
		setihex = Tex(f"\\verb|s={hex(int(binaddr.getGroup(1).value, 2))}|").next_to(taghex, DOWN)
		offsethex = Tex(f"\\verb|b={hex(int(binaddr.getGroup(2).value, 2))}|").next_to(setihex, DOWN)
		
		self.play(binaddr.highlightGroup(1), Write(setihex)) # highlight set in cache
		self.play(binaddr.highlightGroup(0), Write(taghex)) # highlight tag
		self.play(binaddr.highlightGroup(2), Write(offsethex)) # highlight offset in iteration


		self.play(self.cache.highlightSet(3, 0, YELLOW))
		self.play(self.cache.dehighlightSet(3, 0), self.cache.setByte(addrn, databyte, 0, True))

		caption = Text("Write-back for Memory copy").to_edge(DOWN)
		self.play(Write(caption))
		caption2 = Text("Maintain data status with dirty bit").to_edge(DOWN)
		self.play(ReplacementTransform(caption, caption2))

		self.wait(0.25)

		miniCache = Cache(2, 4, 8, self.wordsize).scale(0.90)

		# miniCache is only a slice/view of self.cache, so b/s/t need to remain the same
		# This needs to be done after the constructor since A, B, and C affect these bits
		miniCache.b = self.cache.b
		miniCache.s = self.cache.s
		miniCache.t = self.cache.t

		miniCache.move_to(self.cache.ways[0].sets[3].get_left(), aligned_edge=LEFT)

		way0data:list[tuple[int, int]] = [
			(self.cache.packAddress(self.cache.ways[0].sets[3].tag, 0, i), self.cache.ways[0].sets[3].data[i])
			for i in range(4)
		]
		way1data:list[tuple[int, int]] = [
			(self.cache.packAddress(self.cache.ways[1].sets[3].tag, 0, i), self.cache.ways[1].sets[3].data[i])
			for i in range(4)
		]
		# print(way0data)
		

		miniCache.initBytes(
			[(datatuple[0], datatuple[1], 1) for datatuple in way0data] + 
			[(datatuple[0], datatuple[1], 0) for datatuple in way1data]
		)

		self.play(
			FadeIn(miniCache), 
			FadeOut(self.cache, self.cpu, binaddr, addr, taghex, setihex, offsethex, title, caption, caption2, databyte)
		)

		self.cache = miniCache

	def readMiss(self):
		self.play(self.cache.animate.move_to(ORIGIN))

		caption = Text("Introduces clean and dirty eviction for Read-Miss/Replacement", font_size=30).to_edge(UP)
		self.play(Write(caption))

		# clean evict
		title = Text("Read-Miss/Replacement/Clean-Evict").to_edge(UP)

		addr = SplittableAddress(0xdf6c).next_to(title, DOWN)
		binaddr = SplittableAddress(0xdf6c, [self.cache.t, self.cache.s, self.cache.b], True, 0.25).next_to(addr, DOWN)
		self.play(ReplacementTransform(caption, title), FadeIn(addr))
		self.wait(0.5)
		self.play(TransformFromCopy(addr, binaddr))

		taghex = Tex(f"\\verb|t={hex(int(binaddr.getGroup(0).value, 2))}|").to_corner(UL + (DOWN))
		self.play(binaddr.highlightGroup(0), Write(taghex)) # highlight tag

		caption = Text("Select clean line").to_edge(DOWN)
		self.play(self.cache.highlightSet(0, 1, ORANGE), Write(caption))

		databytes = [
			Hexadecimal("20", "white", 30),
			Hexadecimal("23", "white", 30),
			Hexadecimal("ae", "white", 30), 
			Hexadecimal("d2", "white", 30)
		]
		databytesgroup = VGroup(*databytes).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).to_edge(RIGHT).shift(DOWN)
		# print("Addr of init databyte: 0x{0:x}".format(id(databytes[2])))

		self.play(FadeIn(databytesgroup, shift=LEFT))

		caption2 = Text("'Evict' line").to_edge(DOWN)
		self.play(self.cache.dehighlightSet(0, 1), ReplacementTransform(caption, caption2))

		# self.play(self.cache.ways[1].sets[0].dataText[2].animate.set_opacity(0))

		self.play(*[self.cache.setByte(0xdf60+i, databytes[i], 1) for i in range(4)], binaddr.dehighlightGroup(0))

		caption = Tex("Read byte \\verb|20|").to_edge(DOWN)
		self.play(ReplacementTransform(caption2, caption))

		self.wait(0.5)
		# data0 = self.cache.ways[1].sets[0].dataText[1]
		# print("Id of dataText to animte opacity: 0x{0:x}".format(id(data0)))
		# self.play(data0.animate.set_opacity(0))
		# self.play(self.cache.ways[1].sets[0].dataText[2].animate.set_opacity(0))

		title2 = Text("Read-Miss/Replacement/Dirty-Evict").to_edge(UP)
		addr2 = SplittableAddress(0xdc6c).next_to(title2, DOWN)
		binaddr2 = SplittableAddress(0xdc6c, [self.cache.t, self.cache.s, self.cache.b], True, 0.25).next_to(addr2, DOWN)
		taghex2 = Tex(f"\\verb|t={hex(int(binaddr2.getGroup(0).value, 2))}|").to_corner(UL + DOWN)

		self.play(FadeOut(databytesgroup),
				ReplacementTransform(title, title2), ReplacementTransform(addr, addr2), ReplacementTransform(binaddr, binaddr2),
				ReplacementTransform(taghex, taghex2), FadeOut(caption)
		)

		newbyte = Hexadecimal("f0", "white", 30)
		self.play(binaddr2.highlightGroup(0), self.cache.setByte(0xdf62, newbyte, 1, True))

		# self.play(self.cache.ways[1].sets[0].dataText[2].animate.set_color(RED))
		# print("Addr of accessed data: 0x{0:x}".format(id(self.cache.ways[1].sets[0].dataText[2])))

		caption = Text("Both lines are dirty\nSelect by LRU, evict").to_edge(DOWN)
		self.play(Write(caption), self.cache.highlightSet(0, 0, YELLOW))
		self.wait(0.2)
		self.play(self.cache.dehighlightSet(0, 0))

		self.mem.shift(DOWN*0.65).to_edge(RIGHT)
		self.play(FadeOut(caption, taghex2), self.cache.animate.shift(LEFT*2.5), FadeIn(self.mem))
		self.play(self.cache.ways[1].animate.set_color(GREY))

		databytes = [self.cache.getByte(0xa0e0+i) for i in range(4)]

		addrbytes = [addr.getGroup(0).copy().scale(0.5), addr.getGroup(1).copy().scale(0.5)]

		# Note to self: the current address `addr` is the address for the data to read in the cache
		# Since it is a read miss, the dirty line selected to evict has a different tag than `addr`
		# Meaning when writing the dirty line back to memory, how does it know to what memory address that goes to
		# Since it is not `addr`
		# Maybe it's constructed based on the tag, set, and offset
		# On a different/similar note:
		# When the offset of the address request is not 0 and it requires a memory read as well as writing to cache
		# the address given to memory is the address itself (right? or is it rounded down)
		# it will then read x amount of bytes and write it to cache
		# If not rounded down, it will write what is supposed to be offset of b at offset 0

		self.play(self.mem.setWE(), self.mem.setData([databyte.copy() for _,databyte in databytes]))

		self.wait(0.2)

		caption = Text("Writeback from prior Write Hit", font_size=30).to_edge(DOWN).shift(LEFT)
		self.play(
			*[data.animate.move_to(self.mem.getMemoryBlock(0).get_top()+DOWN*(0.4 + (0.2*i))) for i,data in enumerate(self.mem.getData())],
			Write(caption)
		)

		self.wait(0.5)

		databytes = [
			Hexadecimal("82", "white", 30).move_to(self.mem.getMemoryBlock(2).get_top()+DOWN*0.2),
			Hexadecimal("a3", "white", 30).move_to(self.mem.getMemoryBlock(2).get_top()+DOWN*0.4),
			Hexadecimal("f8", "white", 30).move_to(self.mem.getMemoryBlock(2).get_top()+DOWN*0.6),
			Hexadecimal("b5", "white", 30).move_to(self.mem.getMemoryBlock(2).get_top()+DOWN*0.8)
		]

		self.play(self.mem.setAddr(addrbytes), self.mem.setRE(), self.mem.setWE(False), FadeOut(caption))
		self.play(self.mem.setData(databytes))
		self.wait(0.2)
		self.play(*[self.cache.setByte(0xdc60+i, databytes[i], 0) for i in range(4)])

		_, bytehex = self.cache.getByte(0xdc60)
		copyByte = bytehex.copy()
		# self.play(bytehex.animate.set_color(YELLOW))
		self.play(FadeOut(copyByte, shift=LEFT))

		self.wait(0.3)

		self.play(FadeOut(self.cache, self.mem, binaddr2, addr2, title2))

	def miss(self):
		self.cpu = CPU().to_edge(LEFT, buff=-0.4).scale(0.75)
		# self.cache = Cache(2, 4, 64, self.wordsize).to_edge(RIGHT, buff=-0.25).shift(DOWN * 0.5).scale(0.9)
		self.mem = Memory(2, 4).to_edge(RIGHT, buff=-0.5).scale(0.7)



		addrn = 0x9a88

		self.cache = Cache(2, 4, 64, self.wordsize).scale(0.8).move_to(ORIGIN + (LEFT * 0.25)+ (DOWN * 0.2))
		self.cache.initBytes([(0xf000, 0x32, 1), (0xa030, 0xa2, 0), (0x6f6f, 0x93, 0), (0xa0de, 0xaa, 1), (0xa931, 0xbc, 0)])

		title = Text("Cache Miss").to_edge(UP)

		self.play(FadeIn(self.cpu, self.cache, self.mem), Write(title))

		addr = SplittableAddress(addrn).move_to(self.cpu.get_center())
		addr.generate_target()
		addr.target.next_to(title, DOWN)

		databyte = Hexadecimal("a0", fontSize=30).move_to(self.cpu.getRegisters()[5].get_center())

		self.play(MoveToTarget(addr), FadeIn(databyte))

		binaddr = SplittableAddress(addrn, [self.cache.t, self.cache.s, self.cache.b], True, 0.25).next_to(addr, DOWN)
		self.play(TransformFromCopy(addr, binaddr))

		taghex = Tex(f"\\verb|t={hex(int(binaddr.getGroup(0).value, 2))}|").to_corner(UL)
		setihex = Tex(f"\\verb|s={hex(int(binaddr.getGroup(1).value, 2))}|").next_to(taghex, DOWN)
		offsethex = Tex(f"\\verb|b={hex(int(binaddr.getGroup(2).value, 2))}|").next_to(setihex, DOWN)
		
		self.play(binaddr.highlightGroup(1), Write(setihex))
		self.play(binaddr.highlightGroup(0), Write(taghex))
		self.play(binaddr.highlightGroup(2), Write(offsethex))

		self.play(self.cache.highlightSet(2, 0, RED), self.cache.highlightSet(2, 1, RED))
		self.wait(0.2)
		self.play(self.cache.dehighlightSet(2, 0), self.cache.dehighlightSet(2, 1))

		caption = Text("Block in memory\nWrite-allocate").to_edge(DOWN)
		self.play(Write(caption))

		self.wait(0.5)

		caption2 = Text("Handle as a Read Miss\nRM/NR in this example", font_size=35).to_edge(DOWN)
		self.play(ReplacementTransform(caption, caption2))

		addrbytes = [addr.getGroup(0).copy().scale(0.5), addr.getGroup(1).copy().scale(0.5)]
		self.play(self.mem.setAddr(addrbytes), self.mem.setRE())

		databytes = [
			Hexadecimal("52", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(4).get_top()+DOWN*0.8),
			Hexadecimal("8b", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(4).get_top()+DOWN*1.0),
			Hexadecimal("aa", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(4).get_top()+DOWN*1.2), 
			Hexadecimal("c7", "white", 30).scale(0.7).move_to(self.mem.getMemoryBlock(4).get_top()+DOWN*1.4)
		]
		self.play(self.mem.setData(databytes))

		self.play(*[self.cache.setByte(addrn+i, databytes[i], 0) for i in range(4)])

		self.wait(0.5)

		caption = Text("Handle as Write Hit").to_edge(DOWN)
		self.play(ReplacementTransform(caption2, caption))

		self.play(self.cache.highlightSet(2, 0, YELLOW))
		self.play(self.cache.dehighlightSet(2, 0), self.cache.setByte(addrn, databyte, 0, True))

		self.wait(0.5)

		self.play(FadeOut(self.cpu, self.cache, self.mem, *databytes, title, caption, binaddr, addr, taghex, setihex, offsethex, databyte))

	def construct(self):
		self.hit()
		self.readMiss()

		self.wait(0.5)

		self.miss()

		self.wait(2)