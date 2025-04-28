from os import system
from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.numwheel import NumberWheel

from manim import Scene, MathTex, UL, DOWN

NBITS_LIMIT = 5 # Figure out what is an appropriate limit

class IntegersScene(Scene):
	def __init__(self):
		super().__init__()
		self.nbits = 0
		self.numX = 0
		self.numY = 0
		self._sum = 0

		self.n:MathTex = None
		self.x:MathTex = None
		self.y:MathTex = None

		self.wheel:NumberWheel = None

	def init(self):
		nbits = int(input("How many bits? "))

		# Since more bits means more sectors/wedges/etc, it means more costly and slower
		# Limit input to a low number
		while nbits <= 0 or nbits > NBITS_LIMIT:
			print("N bits cannot be negative or more than ", NBITS_LIMIT)
			nbits = int(input("How many bits? "))

		self.nbits = nbits
		self.wheel = NumberWheel(nbits)

		# Regarding numX and numY, it varies whether it is unsigned or signed
		# That should be checked for each child class

	def endInit(self):
		self.n = MathTex(f"n = {self.nbits}").to_corner(UL).shift(DOWN)
		self.x = MathTex(f"x = {self.numX}").next_to(self.n, DOWN)
		self.y = MathTex(f"y = {self.numY}").next_to(self.x, DOWN)

	def view(self):
		outfile:Path = self.renderer.file_writer.movie_file_path

		# Temp
		system(f"wslview {outfile}")
	
	def intro(self):
		pass

	def wheelAnim(self):
		pass

	def math(self):
		pass