from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from manim import *
from manim.opengl import *

from Wrapper import Wrapper

from animlib.funcs import inttstr, splithex
from animlib.hexdec import Hexadecimal
from animlib.mem import MemoryBlock
from animlib.bitvector import Bytesvector, Bitvector


MSB_COLOR = "#ff5e5e"
LSB_COLOR = "#19b9d1"

class IntEndianness(Wrapper):
	def __init__(self, window=None):
		super().__init__(window)
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
		self.wait(0.5)
		self.play(ReplacementTransform(integer.copy(), hexInt))

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

		MSB_TEXT = Text("MSB", color=MSB_COLOR, font_size=24, font="Helvetica")
		LSB_TEXT = Text("LSB", color=LSB_COLOR, font_size=24, font="Helvetica")

		MSB_TEXT.next_to(self.hexIntBytes[0], DOWN, buff=0.2)
		LSB_TEXT.next_to(self.hexIntBytes[-1], DOWN, buff=0.2)

		self.play(FadeIn(self.hexIntBytes, shift=DOWN))
		self.play(FadeIn(MSB_TEXT))
		self.play(FadeIn(LSB_TEXT))

		self.wait(0.5)

		self.play(FadeOut(MSB_TEXT), FadeOut(LSB_TEXT), FadeOut(self.hexIntBytes), FadeOut(hexInt), FadeOut(integer))

		title = Text("Memory Layout", font="Helvetica").to_edge(UP)
		self.play(Write(title))

		self.mem = MemoryBlock(len(hexbytes) + 2, startAddr=Hexadecimal("0xf0"), endAddr=Hexadecimal(inttstr(0xf0 + len(hexbytes) + 1)))
		self.mem.scale(1.5)

		self.play(FadeIn(self.mem))
		self.wait(0.5)

		self.play(Unwrite(title))
		# self.play(FadeOut(title))

		self.littleEndian()

		# Reset the memory block
		self.mem = MemoryBlock(len(hexbytes) + 2, startAddr=Hexadecimal("0xf0"), endAddr=Hexadecimal(inttstr(0xf0 + len(hexbytes) + 1)))
		self.mem.scale(1.5)

		self.hexIntBytes.arrange(RIGHT, buff=spacing).to_edge(DOWN)

		self.wait(0.5)

		self.bigEndian()


	def littleEndian(self):
		title = Text("Little Endian", font="Helvetica").to_edge(UP)
		self.play(Write(title))

		self.hexIntBytes.to_edge(DOWN)
		self.play(FadeIn(self.hexIntBytes))

		self.wait(0.5)

		self.play(self.mem.setByte(1, self.hexIntMSB))

		for i in range(len(self.hexIntBytes.submobjects) - 2):
			self.play(self.mem.setByte(i+2, self.hexIntBytes.submobjects[i+1]))

		comment = Text("Little byte gets higher address", font_size=18, font="Helvetica").next_to(title, DOWN, buff=1)
		self.play(FadeIn(comment))
		self.play(self.mem.setByte(-2, self.hexIntLSB))

		self.wait(0.15)

		note = Text("Notice that the number can be read from left to right", font="Helvetica").scale(0.75).to_edge(DOWN)
		self.play(
			Write(note),
			LaggedStart(
				*[self.mem.highlightByte(i+1, "#ffe342") for i in range(len(self.mem.blocks) - 2)],
				lag_ratio=0.85
			)
		)

		self.wait(0.5)

		# self.play(Unwrite(note, reverse=False))
		self.play(FadeOut(note))
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
		title = Text("Big Endian", font="Helvetica").to_edge(UP)
		self.play(Write(title))

		self.play(FadeIn(self.hexIntBytes))

		self.wait(0.5)

		self.play(FadeIn(self.mem))
		self.wait(0.5)

		comment = Text("Big byte gets higher address", font_size=18, font="Helvetica").next_to(title, DOWN, buff=1)
		self.play(FadeIn(comment))
		self.play(self.mem.setByte(-2, self.hexIntMSB))

		for i in range(len(self.hexIntBytes.submobjects) - 2):
			self.play(self.mem.setByte(i-3, self.hexIntBytes.submobjects[i+1]))

		self.play(self.mem.setByte(1, self.hexIntLSB))

		self.wait(0.5)

		note = Text("This time, notice that the number cannot be read from left to right", font="Helvetica").scale(0.55).to_edge(DOWN)
		self.play(
			Write(note),
			LaggedStart(
				*[self.mem.highlightByte(-i - 2, "#ffe342") for i in range(len(self.mem.blocks) - 2)],
				lag_ratio=0.85
			)
		)

		self.wait(0.5)

		# self.play(Unwrite(note, reverse=False))
		self.play(FadeOut(note))
		self.play(*[self.mem.dehighlightByte(i+1) for i in range(len(self.mem.blocks) - 2)])

		self.play(FadeOut(comment))
		self.play(FadeOut(title))

		self.play(self.mem.transpose())
		self.play(self.mem.blocks.animate.arrange(UP, buff=0))
		self.play(self.mem.updateTextPos())
		
		self.wait(0.5)

		self.play(*[FadeOut(mobj) for mobj in self.mobjects])

class CharArrEndianness(Wrapper):
	def __init__(self):
		super().__init__()

	def init(self):
		pass

	def construct(self):
		pass

class IntArrEndianness(Wrapper):
	def __init__(self):
		super().__init__()
		self.arr:list[int] = None
		self.bytevec:Bytesvector = None
		self.mem:MemoryBlock = None

	def init(self):
		self.arr = [2048, 32768, 1024, 1060]

	def construct(self):
		intvec = Bitvector(len(self.arr), self.arr, False).to_edge(UP)
		self.bytesvec = Bytesvector(len(self.arr), self.arr).next_to(intvec, DOWN)

		self.play(FadeIn(intvec))
		self.play(TransformFromCopy(intvec, self.bytesvec))
		# self.play(FadeIn(self.bytesvec))


def main() -> None:
	choice = int(input("For what data do you want to see its endianness for? [number: 0, char array: 1, number array: 2, exit: -1]: "))

	while choice != -1:
		endianScene:Wrapper = None

		if choice == 0:
			endianScene = IntEndianness()
		elif choice == 1:
			endianScene = CharArrEndianness()
		elif choice == 2:
			endianScene = IntArrEndianness()

		endianScene.init()
		endianScene.render()

		# endianScene.renderer = None
		endianScene.view()
		
		choice = int(input("For what data do you want to see its endianness for? [number: 0, char array: 1, number array: 2, exit: -1]: "))


if __name__ == "__main__":
	# config.renderer = "opengl"
	# config.write_to_movie = False
	# config.preview = True
	# config.save_last_frame = False
	# config.format = None
	# config.dry_run = False
	# config.input_file = "main.py"
	# config.disable_caching = False

	main()

	# intArrEndian = IntArrEndianness()
	# intArrEndian.init()
	# intArrEndian.render()
	# intArrEndian.view()
	
	# scene = IntEndianness()
	# scene.init()
	# scene.render()

	# add tts to run in synch