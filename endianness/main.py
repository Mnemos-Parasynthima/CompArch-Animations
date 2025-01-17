from manim import *

from Nums import Nums

class Endianness(Scene):
	def construct(self):
		numsScene = Nums()
		numsScene.construct()

		

# if __name__ == "__main__":
# 	scene:Scene = Endianness()
# 	scene.render()