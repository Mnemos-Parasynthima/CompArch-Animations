from manim import VGroup, RoundedRectangle, BLUE, RED
from abc import ABC
from .Path import Path


class Stage(VGroup, ABC):
	def __init__(self, stageWidth:int, stageHeight:int, stageCornerRadius:float=0.5):
		super().__init__()

		stage = RoundedRectangle(corner_radius=stageCornerRadius, width=stageWidth, height=stageHeight)
		self.add(stage)

		# Connecting line/paths
		# These will only concern with paths within the Stage
		# For interstage paths, they will be made at the outside level
		self.paths:dict[str, Path] = {}


	def highlightPath(self, path:str):
		return self.paths[path].highlight(BLUE, 4)
	
	def dehighlightPath(self, path:str):
		return self.paths[path].highlight(RED, 2)