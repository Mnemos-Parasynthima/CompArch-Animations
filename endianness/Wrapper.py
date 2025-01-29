from os import system
from pathlib import Path

from manim import Scene

class Wrapper(Scene):
	def __init__(self, window):
		super().__init__()
		# self.renderer.window = window

	def init(self):
		pass

	def view(self):
		outfile:Path = self.renderer.file_writer.movie_file_path
			
		# Temp
		system(f"wslview {outfile}")
	
	def littleEndian(self):
		pass

	def bigEndian(self):
		pass