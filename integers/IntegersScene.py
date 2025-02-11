from os import system
from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.numwheel import NumberWheel

from manim import Scene, MathTex, UL, DOWN

class IntegersScene(Scene):
	def __init__(self, nbits:int, numX:int, numY:int):
		super().__init__()
		# self.renderer.window = window
		self.nbits:int = nbits
		self.numX = numX
		self.numY = numY
		self._sum:int = (numX + numY) % 2**nbits

		self.n = MathTex(f"n = {nbits}").to_corner(UL).shift(DOWN)
		self.x = MathTex(f"x = {numX}").next_to(self.n, DOWN)
		self.y = MathTex(f"y = {numY}").next_to(self.x, DOWN)

		self.wheel = NumberWheel(nbits)

	def init(self):
		pass

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