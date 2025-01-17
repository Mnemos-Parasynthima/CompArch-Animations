from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.hexdec import Hexadecimal

from manim import *

from constants import *


class Nums(Scene):
	def construct(self):
		integer = Integer(number=2025, group_with_commas=False).to_edge(UP)
		self.play(FadeIn(integer))

		hexInt = Hexadecimal("0x7e9").next_to(integer, DOWN)
		self.play(Transform(integer.copy(), hexInt))

		hexIntMSB = Hexadecimal("0x07", color=MSB_COLOR)
		hexIntLSB = Hexadecimal("0xe9", color=LSB_COLOR)
		hexIntBytes = VGroup(hexIntMSB, hexIntLSB).arrange(RIGHT, buff=1).next_to(hexInt, DOWN, buff=1)

		MSB_TEXT.next_to(hexIntBytes[0], DOWN, buff=0.2)
		LSB_TEXT.next_to(hexIntBytes[-1], DOWN, buff=0.2)

		self.play(FadeIn(hexIntBytes, shift=DOWN))
		self.play(FadeIn(MSB_TEXT))
		self.play(FadeIn(LSB_TEXT))

		self.wait(1)