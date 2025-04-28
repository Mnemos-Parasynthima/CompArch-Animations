from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.mem import MemoryBlock
from animlib.hexdec import Hexadecimal

from manim import Text, Write, FadeIn, Scene, UP, DOWN

class QuestionOne(Scene):
	def construct(self):
		title = Text("Question", font="Helvetica").to_edge(UP)
		self.play(Write(title))
		
		hexInt = Hexadecimal("0x25beaa10").next_to(title, DOWN, buff=0.5)
		self.play(FadeIn(hexInt))

		descr = Text("Write the given integer in BIG endian", font_size=18, font="Helvetica").next_to(hexInt, DOWN, buff=0.5)
		self.play(Write(descr))

		mem = MemoryBlock(6, startAddr=Hexadecimal("0xa0"), endAddr=Hexadecimal("0xa5"))
		mem.scale(1.5)

		self.play(FadeIn(mem))
		self.wait(1.5)