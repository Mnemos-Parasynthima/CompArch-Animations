from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.numwheel import NumberWheel

from manim import *


class UnsignedAddition(Scene):
	def construct(self):
		nbits = 3
		numX = 5
		numY = 5
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
			self.play(wheel.highlightNumber(xi, YELLOW, False), run_time=0.4)

			self.play(wheel.dehighlightNumber(xi, False), run_time=0.3)
		xi += 1
		self.play(x.animate.set_color(WHITE))

		self.play(y.animate.set_color(GREEN))

		self.play(FadeIn(wheel.setupArrow(xi)))
		for yi in range(numY):
			anims:list[Succession|Text|Rotate] = []

			if yi != numY-1: anims.append(wheel.rotateArrow())

			blink = False
			if xi+yi > wheel.totalSlices - 1:
				# When in overflow, show the actual mathematical result as well as its canonical number
				if not wheel.flag: wheel.flag = True
				mathNum, animMathNum = wheel.highlightMathNumber(xi + yi, GREEN)
				anims.append(animMathNum)
				blink = True

			anims.append(wheel.highlightNumber(xi + yi, ORANGE, blink))
			self.play(*anims, run_time=0.4)

			self.play(wheel.dehighlightNumber(xi + yi, blink), run_time=0.3)
			if wheel.flag: self.play(wheel.dehighlightMathNumber(mathNum, xi + yi), run_time=0.3)
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

class SignedAddition(Scene):
	def construct(self):
		nbits = 3
		numX = 3
		numY = 3
		mathSum = numX + numY
		# Sum for signed addition is more complex, with cases depending on n
		lowerBound = -2**(nbits-1)
		upperBound = 2**(nbits-1)

		if mathSum >= upperBound: _sum = mathSum - 2**nbits
		elif mathSum < lowerBound: _sum = mathSum + 2**nbits
		else: _sum = mathSum

		wheel = NumberWheel(nbits, signed=True)

		title = Text("Signed Addition").to_edge(UP)
		self.play(FadeIn(title))

		uAddEqu = MathTex("x \oplus_{s}^{n} y").next_to(title, RIGHT, 1)
		self.play(FadeIn(uAddEqu))

		n = MathTex(f"n = {nbits}").to_corner(UL).shift(DOWN)
		x = MathTex(f"x = {numX}").next_to(n, DOWN)
		y = MathTex(f"y = {numY}").next_to(x, DOWN)
		self.play(FadeIn(n), FadeIn(x), FadeIn(y))

		self.wait(0.5)

		self.play(FadeIn(wheel))
		
		self.wait(0.25)

		# When x is negative, highlight going CCW from 0 until it hits the appropriate num
		# When x is positive, do same as in Unsigned
		self.play(x.animate.set_color(YELLOW))

		rangeIter:range = None
		if numX >= 0: rangeIter = range(numX+1)
		else: rangeIter = range(-1, numX-1, -1)

		for xi in rangeIter:
			self.play(wheel.highlightNumber(xi, YELLOW, False), run_time=0.4)
			self.play(wheel.dehighlightNumber(xi, False), run_time=0.3)
		self.play(x.animate.set_color(WHITE))

		self.play(y.animate.set_color(GREEN))

		if numY >= 0 and numX >= 0: xi += 1
		elif numY >= 0 and numX < 0: xi += 1
		elif numY < 0 and numX >= 0: xi -= 1
		else: xi -= 1
		# xi is used to index from the right

		print("xi: ", xi)
		self.play(FadeIn(wheel.setupArrow(xi)))
		# print("numY: ", numY)
		if numY >= 0:
			for yi in range(numY):
				anims:list[Animation|AnimationGroup|VMobject] = []

				if yi != numY-1: anims.append(wheel.rotateArrow())

				blink = False
				if xi+yi >= wheel.totalSlices/2:
					if not wheel.flag: wheel.flag = True
					mathNum, animMathNum = wheel.highlightMathNumber(xi + yi, GREEN)
					anims.append(animMathNum)
					blink = True

				anims.append(wheel.highlightNumber(xi + yi, ORANGE, blink))
				self.play(*anims, run_time=0.4)

				self.play(wheel.dehighlightNumber(xi + yi, blink), run_time=0.3)
				if wheel.flag: self.play(wheel.dehighlightMathNumber(mathNum, xi + yi), run_time=0.3)
		else:
			# numY being negative would mean for the indices to be decrementing
			# Since the real indices is taken care of in highlightNumber(), the pseudo
			
			for yi in range(numY, 0):
				# yi is used to simply as a counting method, doing range(abs(numY)) would still work

				numberText = int(wheel.getNumber(xi).text)
				numberText = wheel._toUnsigned(numberText) if numberText < 0 else numberText

				anims:list[Text|Succession|Rotate] = []
				if yi != -1: anims.append(wheel.rotateArrow(False))

				blink = False
				print(xi, yi)
				if abs(xi) > wheel.totalSlices/2:
					if not wheel.flag: wheel.flag = True
					# print("Overflow")
					mathNum, animMathNum = wheel.highlightMathNumber(xi, GREEN)
					anims.append(animMathNum)
					blink = True

				anims.append(wheel.highlightNumber(numberText, ORANGE, blink))
				self.play(*anims, run_time=0.4)

				self.play(wheel.dehighlightNumber(numberText, blink), run_time=0.3)
				if wheel.flag: self.play(wheel.dehighlightMathNumber(mathNum, xi), run_time=0.3)

				xi -= 1

		self.play(x.animate.set_color(WHITE))

		self.wait(0.5)

		res = MathTex(f"{_sum}").to_edge(DOWN)

		mathSumText = MathTex(f"s = {numX} + {numY}").next_to(y, DOWN * 1).shift(RIGHT * 0.5)
		self.play(FadeIn(mathSumText))

		equ:str = None
		equstr0:str = None
		equstr1:str = None
		endequstr = str(_sum) + " = " + str(_sum)

		if mathSum >= upperBound:
			equ = MathTex(" = s - 2^n").next_to(res)
			equstr0 = str(_sum) + " = " + str(mathSum) + " - 2^" + str(nbits)
			equstr1 = str(_sum) + " = " + str(mathSum) + " - " + str(2**nbits)
		elif mathSum < lowerBound:
			equ = MathTex(" = s + 2^n").next_to(res)
			equstr0 = str(_sum) + " = " + str(mathSum) + " + 2^" + str(nbits)
			equstr1 = str(_sum) + " = " + str(mathSum) + " + " + str(2**nbits)
		else:
			equ = MathTex(" = s").next_to(res)

		self.play(TransformFromCopy(wheel.getNumber(_sum), res))

		requ = VGroup(res, equ).arrange(RIGHT).to_edge(DOWN)
		self.play(FadeIn(requ))

		equ2:MathTex = None 
		if equstr0:
			equ1 = MathTex(equstr0).to_edge(DOWN)
			self.play(Transform(requ, equ1, replace_mobject_with_target_in_scene=True))

			equ2 = MathTex(equstr1).to_edge(DOWN)
			self.play(Transform(equ1, equ2, replace_mobject_with_target_in_scene=True))
		
		equend = MathTex(endequstr).to_edge(DOWN)
		self.play(Transform((requ if not equ2 else equ2), equend, replace_mobject_with_target_in_scene=True))


		self.wait(2)