from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.mem import MemoryBlock
from animlib.hexdec import Hexadecimal

from manim import *

class QuestionTwo(Scene):
	def construct(self):
		title = Text("Question").to_edge(UP).to_edge(LEFT)
		self.play(Write(title))

		descr = Paragraph("What is the number stored in memory", "starting at address 0xa1", "given LITTLE endian", 
				alignment="left").scale(0.75).to_edge(LEFT)
		# descr = Text("What is the number stored in memory starting at address 0xa1 given LITTLE endian", 
		# 	font_size=18)
		self.play(Write(descr))

		mem = MemoryBlock(6, startAddr=Hexadecimal("0xa0"), endAddr=Hexadecimal("0xa5"), layout=1)
		mem.scale(1.15).to_edge(RIGHT, buff=1)

		self.play(FadeIn(mem))

		bytes:list[Hexadecimal] = [
			Hexadecimal("0x2e"), Hexadecimal("0xff"),
			Hexadecimal("0xb2"), Hexadecimal("0x11")
		]

		for i, byte in zip(range(1, 5), bytes):
			self.play(mem.setByte(i, byte))

		self.wait(1.5)