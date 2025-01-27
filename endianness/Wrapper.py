from os import system
from pathlib import Path

from manim import Scene

class Wrapper(Scene):
	def __init__(self):
		super().__init__()

	def init(self):
		pass

	def view(self):
		outfile:Path = self.renderer.file_writer.movie_file_path
			
		# Temp
		system(f"wslview {outfile}")