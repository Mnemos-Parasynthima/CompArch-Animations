from sys import path
from pathlib import Path
import os

path.append(str(Path(__file__).resolve().parent.parent))

from manim import *

# from Wrapper import Wrapper
from animlib.funcs import inttstr, splithex
from animlib.hexdec import Hexadecimal
from animlib.mem import MemoryBlock
from constants import *

class Endianness(Scene):
	def __init__(self):
		super().__init__()
		self.value:int = 0
		self.hexIntMSB:Hexadecimal = None
		self.hexIntLSB:Hexadecimal = None
		self.hexIntBytesGroup:VGroup = None
		self.mem:MemoryBlock = None

	def init(self):
		# self.value:int = int(input("Enter an integer: "))
		# self.value = 0xfabbccddeeff0011
		self.value = 0xfabbcc

	def construct(self):
		integer = Integer(number=self.value, group_with_commas=False).to_edge(UP)
		self.play(FadeIn(integer))

		hexstr:str = inttstr(self.value)
		hexbytes:list[str] = splithex(hexstr)

		hexInt = Hexadecimal(hexstr).next_to(integer, DOWN)
		self.play(Transform(integer.copy(), hexInt, replace_mobject_with_target_in_scene=True))

		self.hexIntMSB = Hexadecimal(hexbytes[0], color=MSB_COLOR)
		self.hexIntLSB = Hexadecimal(hexbytes[-1], color=LSB_COLOR)

		_hexbytes:list[Hexadecimal] = []
		for i in range(len(hexbytes) - 2):
			_hexbytes.append(Hexadecimal(hexbytes[i+1]))

		self.hexIntBytes = VGroup(self.hexIntMSB, *_hexbytes, self.hexIntLSB)

		maxBytesRow = 7
		byteCount = len(hexbytes)
		if byteCount > maxBytesRow:
			scale = max(0.7, 7 / byteCount)
			self.hexIntBytes.scale(scale)
			spacing = 0.5 * scale
		else: spacing = 1

		self.hexIntBytes.arrange(RIGHT, buff=spacing).next_to(hexInt, DOWN, buff=1)

		MSB_TEXT.next_to(self.hexIntBytes[0], DOWN, buff=0.2)
		LSB_TEXT.next_to(self.hexIntBytes[-1], DOWN, buff=0.2)

		self.play(FadeIn(self.hexIntBytes, shift=DOWN))
		self.play(FadeIn(MSB_TEXT))
		self.play(FadeIn(LSB_TEXT))

		self.wait(1)

		self.play(FadeOut(MSB_TEXT), FadeOut(LSB_TEXT), FadeOut(self.hexIntBytes), FadeOut(hexInt), FadeOut(integer))

		title = Text("Memory Layout").to_edge(UP)
		self.play(Write(title))

		self.mem = MemoryBlock(len(hexbytes) + 2, startAddr=Hexadecimal("0xf0"), endAddr=Hexadecimal(inttstr(0xf0 + len(hexbytes) + 1)))
		self.mem.scale(1.5)

		self.play(FadeIn(self.mem))
		self.wait(1.5)

		self.play(Unwrite(title))

		self.littleEndian()

		# Reset the memory block
		self.mem = MemoryBlock(len(hexbytes) + 2, startAddr=Hexadecimal("0xf0"), endAddr=Hexadecimal(inttstr(0xf0 + len(hexbytes) + 1)))
		self.mem.scale(1.5)

		self.hexIntBytes.arrange(RIGHT, buff=spacing).to_edge(DOWN)

		self.wait(0.5)

		self.bigEndian()

		self.wait(1)

	def littleEndian(self):
		title = Text("Little Endian").to_edge(UP)
		self.play(Write(title))

		self.hexIntBytes.to_edge(DOWN)
		self.play(FadeIn(self.hexIntBytes))

		self.wait(0.5)

		self.play(self.mem.setByte(1, self.hexIntMSB))

		for i in range(len(self.hexIntBytes.submobjects) - 2):
			self.play(self.mem.setByte(i+2, self.hexIntBytes.submobjects[i+1]))

		comment = Text("Little byte gets higher address", font_size=18).next_to(title, DOWN, buff=1)
		self.play(FadeIn(comment))
		self.play(self.mem.setByte(-2, self.hexIntLSB))

		self.wait(1.15)

		note = Text("Notice that the number can be read from left to right").scale(0.75).to_edge(DOWN)
		self.play(
			Write(note),
			LaggedStart(
				*[self.mem.highlightByte(i+1, "#ffe342") for i in range(len(self.mem.blocks) - 2)],
				lag_ratio=0.85
			)
		)

		self.wait(0.5)

		self.play(Unwrite(note, reverse=False))
		self.play(*[self.mem.dehighlightByte(i+1) for i in range(len(self.mem.blocks) - 2)])

		self.wait(0.5)

		self.play(FadeOut(comment))
		self.play(FadeOut(title))
		# Maybe possible fix/alt is to have a vert copy with its labels as well,
		# iterating through the objects in curr mem (horiz) and Transform each one to its respective obj in vert copy
		# memT = MemoryBlock(len(self.mem.blocks), 1)

		self.play(self.mem.transpose())
		# Refer to comment in transpose; overall, needs to be fixed
		# This v should NOT be here, but it is here because it somehow works
		self.play(self.mem.blocks.animate.arrange(UP, buff=0))
		self.play(self.mem.updateTextPos())

		self.wait(0.5)

		self.play(*[FadeOut(mobj) for mobj in self.mobjects])

	def bigEndian(self):
		title = Text("Big Endian").to_edge(UP)
		self.play(Write(title))

		self.play(FadeIn(self.hexIntBytes))

		self.wait(0.5)

		self.play(FadeIn(self.mem))
		self.wait(0.5)

		comment = Text("Big byte gets higher address", font_size=18).next_to(title, DOWN, buff=1)
		self.play(FadeIn(comment))
		self.play(self.mem.setByte(-2, self.hexIntMSB))

		for i in range(len(self.hexIntBytes.submobjects) - 2):
			self.play(self.mem.setByte(i-3, self.hexIntBytes.submobjects[i+1]))

		self.play(self.mem.setByte(1, self.hexIntLSB))

		self.wait(0.5)

		note = Text("This time, notice that the number cannot be read from left to right").scale(0.65).to_edge(DOWN)
		self.play(
			Write(note),
			LaggedStart(
				*[self.mem.highlightByte(-i - 2, "#ffe342") for i in range(len(self.mem.blocks) - 2)],
				lag_ratio=0.85
			)
		)

		self.wait(0.5)

		self.play(Unwrite(note, reverse=False))
		self.play(*[self.mem.dehighlightByte(i+1) for i in range(len(self.mem.blocks) - 2)])

		self.play(FadeOut(comment))
		self.play(FadeOut(title))

		self.play(self.mem.transpose())
		self.play(self.mem.blocks.animate.arrange(UP, buff=0))
		self.play(self.mem.updateTextPos())
		

		self.wait(1)

		
		



def main() -> None:
	endianness = Endianness()
	endianness.init()
	endianness.render()

	outfile:Path = endianness.renderer.file_writer.movie_file_path
	
	# Temp
	os.system(f"wslview {outfile}")
		

if __name__ == "__main__":
	main()