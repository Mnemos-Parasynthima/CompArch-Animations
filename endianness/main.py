from manim import *

class SquareCircle(Scene):
	def construct(self):
		circle:Circle = Circle()
		square:Square = Square()
		square.flip(RIGHT)
		square.rotate(-3 * TAU / 8)
		circle.set_fill(PINK, opacity=0.5)

		self.play(Create(square))
		self.play(Transform(square, circle))
		self.play(FadeOut(square))