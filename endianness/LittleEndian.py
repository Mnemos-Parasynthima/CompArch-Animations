from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.mem import MemoryBlock
from animlib.hexdec import Hexadecimal

from manim import *

from constants import *

class LittleEndian(Scene):
	def construct(self):
		title = Text("Little Endian").to_edge(UP)
		self.play(Write(title))

		byte0 = Hexadecimal("0x07", color=LSB_COLOR)
		byte1 = Hexadecimal("0xe9", color=MSB_COLOR)
		hexIntBytes = VGroup(byte1, byte0).arrange(RIGHT, buff=1).move_to(4 * LEFT).to_edge(DOWN)
		self.play(FadeIn(hexIntBytes))

		mem = MemoryBlock(4, startAddr=Hexadecimal("0xF0"), endAddr=Hexadecimal("0xF3"))
		# mem.to_edge(UP)
		mem.scale(1.5)

		self.play(FadeIn(mem))
		self.wait(0.5)

		hexIntBytes -= byte1
		self.play(mem.setByte(1, byte1))

		comment = Text("Little byte gets higher address", font_size=18).next_to(title, DOWN, buff=1)
		self.play(FadeIn(comment))

		hexIntBytes -= byte0
		self.play(mem.setByte(2, byte0))

		self.wait(1.15)

		# allObjs = VGroup(hexIntBytes, mem, title)
		# allObjs.animate.set_opacity(0.5)

		note = Text("Notice that the number can be read from left to right").scale(0.75).to_edge(DOWN)
		self.play(
			Write(note),
			LaggedStart(mem.highlightByte(1, "#ffe342"), mem.highlightByte(2, "#ffe342"), lag_ratio=0.95)
		)

		self.wait(0.5)

		self.play(Unwrite(note, reverse=False))
		self.play(mem.dehighlightByte(2), mem.dehighlightByte(1))

		self.wait(0.5)

		self.play(FadeOut(comment))
		self.play(FadeOut(title))

		self.play(mem.transpose())
		self.play(mem.updateTextPos())
		

		self.wait(1)