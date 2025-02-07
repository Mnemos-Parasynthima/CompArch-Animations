from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.numwheel import NumberWheel

from manim import *

class Addition(Scene):
	def construct(self):
		nbits = 3
		numX = 7
		numY = 7
		_sum = (numX + numY) % 2**nbits

		wheel = NumberWheel(nbits)

		title = Text("Unsigned Addition").to_edge(UP)
		self.play(FadeIn(title))

		uAddEqu = MathTex("x \oplus_{u}^{n} y").next_to(title, RIGHT, 1)
		self.play(FadeIn(uAddEqu))

		n = MathTex(f"n = {nbits}").to_corner(UL).shift(DOWN)
		x = MathTex(f"x = {numX}").next_to(n, DOWN)
		y = MathTex(f"y = {numY}").next_to(x, DOWN)
		self.play(FadeIn(n), FadeIn(x), FadeIn(y))

		self.wait(0.5)

		self.play(FadeIn(wheel))
		
		self.wait(0.25)

		self.play(x.animate.set_color(YELLOW))
		for xi in range(numX+1):
			# print(xi)
			self.play(wheel.highlightNumber(xi, YELLOW, False), run_time=0.4)

			self.play(wheel.dehighlightNumber(xi, False), run_time=0.3)
		xi += 1
		self.play(x.animate.set_color(WHITE))

		self.play(y.animate.set_color(GREEN))

		self.play(FadeIn(wheel.arrow))
		for yi in range(numY):
			# print(yi, xi + yi)
			anims:list[Animation|AnimationGroup|VMobject] = []

			anims.append(wheel.highlightNumber(xi + yi, ORANGE, True))
			# self.play(anim, run_time=0.4)
			if xi+yi > wheel.totalSlices - 1:
				mathNum, animMathNum = wheel.highlightMathNumber(xi + yi, GREEN)
				if yi != numY-1: anims.append(Rotate(wheel.arrow, -PI/4, about_point=ORIGIN, rate_func=rate_functions.ease_in_expo))
				anims.append(animMathNum)
				# self.play(animMathNum, run_time=1)
			self.play(*anims, run_time=0.4)

			# if yi != numY-1: 
			self.play(wheel.dehighlightNumber(xi + yi, True), run_time=0.3)
			if xi+yi > wheel.totalSlices - 1: self.play(wheel.dehighlightMathNumber(mathNum, xi + yi), run_time=0.3)
		self.play(x.animate.set_color(WHITE))

		self.wait(0.5)

		res = MathTex(f"{_sum}").to_edge(DOWN)
		equ = MathTex("= (x + y \\text{ mod } 2^n)").next_to(res)

		self.play(TransformFromCopy(wheel.getNumber(_sum), res))

		requ = VGroup(res, equ).arrange(RIGHT).to_edge(DOWN)

		self.play(FadeIn(requ))

		equstr = str(_sum) + " = " + str(numX) + " + " + str(numY) + "\\text{ mod } 2^" + str(nbits)
		equ1 = MathTex(equstr).to_edge(DOWN)
		self.play(Transform(requ, equ1, replace_mobject_with_target_in_scene=True))

		equstr = str(_sum) + " = " + str(numX + numY) + "\\text{ mod } " + str(2**nbits)
		equ2 = MathTex(equstr).to_edge(DOWN)
		self.play(Transform(equ1, equ2, replace_mobject_with_target_in_scene=True))

		equstr = str(_sum) + " = " + str((numX + numY) % (2**nbits))
		equ3 = MathTex(equstr).to_edge(DOWN)
		self.play(Transform(equ2, equ3, replace_mobject_with_target_in_scene=True))

		self.wait(2)