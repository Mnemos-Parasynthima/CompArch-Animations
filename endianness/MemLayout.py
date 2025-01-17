from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.mem import MemoryBlock
from animlib.hexdec import Hexadecimal

from manim import *

from constants import *

class MemLayout(Scene):
	def construct(self):
		title = Text("Memory Layout").to_edge(UP)
		self.play(Write(title))

		# byte0 = Hexadecimal("0x07", color=LSB_COLOR)
		# byte1 = Hexadecimal("0xe9", color=MSB_COLOR)
		# hexIntBytes = VGroup(byte1, byte0).arrange(RIGHT, buff=1).move_to(4 * LEFT).to_edge(DOWN)
		# self.play(FadeIn(hexIntBytes))

		mem = MemoryBlock(4, startAddr=Hexadecimal("0xF0"), endAddr=Hexadecimal("0xF3"))
		# mem.to_edge(UP)
		mem.scale(1.5)

		self.play(FadeIn(mem))
		self.wait(1.5)

		self.play(*[FadeOut(mobj) for mobj in self.mobjects])