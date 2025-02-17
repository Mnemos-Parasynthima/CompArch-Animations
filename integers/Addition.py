from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.numwheel import NumberWheel
from IntegersScene import IntegersScene

from manim import *


class UnsignedAddition(IntegersScene):
	def init(self):
		super().init()

		minNum = 0
		maxNum = 2**(self.nbits)-1

		numX = int(input(f"Enter an integer between {minNum} and {maxNum} for x: "))
		while numX < minNum or numX > maxNum:
			print("Number is out of bounds permitted by nbits or is negative!")
			numX = int(input(f"Enter an integer between {minNum} and {maxNum} for x: "))

		self.numX = numX

		numY = int(input(f"Enter an integer between {minNum} and {maxNum} for y: "))
		while numY < minNum or numY > maxNum:
			print("Number is out of bounds permitted by nbits or is negative!")
			numY = int(input(f"Enter an integer between {minNum} and {maxNum} for y: "))

		self.numY = numY

		self._sum:int = (numX + numY) % 2**self.nbits

		self.wheel = NumberWheel(self.nbits)

		super().endInit()

	def intro(self):
		title = Text("Unsigned Addition").to_edge(UP)
		self.play(FadeIn(title))

		uAddEqu = MathTex("x \oplus_{u}^{n} y").next_to(title, RIGHT, 1)
		self.play(FadeIn(uAddEqu))

		self.play(FadeIn(self.n), FadeIn(self.x), FadeIn(self.y))

		self.wait(0.5)

		self.play(FadeIn(self.wheel))

	def wheelAnim(self):
		self.play(self.x.animate.set_color(YELLOW))
		for xi in range(self.numX+1):
			self.play(self.wheel.highlightNumber(xi, YELLOW, False), run_time=0.4)

			self.play(self.wheel.dehighlightNumber(xi, False), run_time=0.3)
		xi += 1
		self.play(self.x.animate.set_color(WHITE))

		self.play(self.y.animate.set_color(GREEN))

		self.play(FadeIn(self.wheel.setupArrow(xi)))
		for yi in range(self.numY):
			anims:list[Succession|Text|Rotate] = []

			if yi != self.numY-1: anims.append(self.wheel.rotateArrow())

			blink = False
			if xi+yi > self.wheel.totalSlices - 1:
				# When in overflow, show the actual mathematical result as well as its canonical number
				if not self.wheel.flag: self.wheel.flag = True
				mathNum, animMathNum = self.wheel.highlightMathNumber(xi + yi, GREEN)
				anims.append(animMathNum)
				blink = True

			anims.append(self.wheel.highlightNumber(xi + yi, ORANGE, blink))
			self.play(*anims, run_time=0.4)

			self.play(self.wheel.dehighlightNumber(xi + yi, blink), run_time=0.3)
			if self.wheel.flag: self.play(self.wheel.dehighlightMathNumber(mathNum, xi + yi), run_time=0.3)
		self.play(self.x.animate.set_color(WHITE))

	def math(self):
		res = MathTex(f"{self._sum}").to_edge(DOWN)
		equ = MathTex("= (x + y \\text{ mod } 2^n)").next_to(res)

		self.play(TransformFromCopy(self.wheel.getNumber(self._sum), res))

		requ = VGroup(res, equ).arrange(RIGHT).to_edge(DOWN)

		self.play(FadeIn(requ))

		equstr = str(self._sum) + " = " + str(self.numX) + " + " + str(self.numY) + "\\text{ mod } 2^" + str(self.nbits)
		equ1 = MathTex(equstr).to_edge(DOWN)
		self.play(Transform(requ, equ1, replace_mobject_with_target_in_scene=True))

		equstr = str(self._sum) + " = " + str(self.numX + self.numY) + "\\text{ mod } " + str(2**self.nbits)
		equ2 = MathTex(equstr).to_edge(DOWN)
		self.play(Transform(equ1, equ2, replace_mobject_with_target_in_scene=True))

		equstr = str(self._sum) + " = " + str((self.numX + self.numY) % (2**self.nbits))
		equ3 = MathTex(equstr).to_edge(DOWN)
		self.play(Transform(equ2, equ3, replace_mobject_with_target_in_scene=True))

	def construct(self):
		self.intro()

		self.wait(0.25)

		self.wheelAnim()

		self.wait(0.5)

		self.math()

		self.wait(2)

class SignedAddition(IntegersScene):
	def init(self):
		super().init()

		# Negative numbers are allowed but they are to be within a certain range according to nbits
		self.lowerBound = -2**(self.nbits-1)
		self.upperBound = 2**(self.nbits-1)

		minNum = -2**(self.nbits-1)
		maxNum = 2**(self.nbits-1) - 1

		numX = int(input(f"Enter an integer between {minNum} and {maxNum} for x: "))
		while numX < minNum or numX > maxNum:
			print("Number is out of bounds permitted by nbits or is negative!")
			numX = int(input(f"Enter an integer between {minNum} and {maxNum} for x: "))

		self.numX = numX

		numY = int(input(f"Enter an integer between {minNum} and {maxNum} for y: "))
		while numY < minNum or numY > maxNum:
			print("Number is out of bounds permitted by nbits or is negative!")
			numY = int(input(f"Enter an integer between {minNum} and {maxNum} for y: "))

		self.numY = numY

		self._sum:int = (numX + numY) % 2**self.nbits

		# Sum for signed addition is more complex, with cases depending on n
		self.mathSum = self.numX + self.numY

		if self.mathSum >= self.upperBound: self._sum = self.mathSum - 2**self.nbits
		elif self.mathSum < self.lowerBound: self._sum = self.mathSum + 2**self.nbits
		else: self._sum = self.mathSum

		self.wheel = NumberWheel(self.nbits, signed=True)

		super().endInit()

	def intro(self): 
		title = Text("Signed Addition").to_edge(UP)
		self.play(FadeIn(title))

		uAddEqu = MathTex("x \oplus_{s}^{n} y").next_to(title, RIGHT, 1)
		self.play(FadeIn(uAddEqu))

		self.play(FadeIn(self.n), FadeIn(self.x), FadeIn(self.y))

		self.wait(0.5)

		self.play(FadeIn(self.wheel))

	def wheelAnim(self): 
		# When x is negative, highlight going CCW from 0 until it hits the appropriate num
		# When x is positive, do same as in Unsigned
		self.play(self.x.animate.set_color(YELLOW))

		rangeIter:range = None
		if self.numX >= 0: rangeIter = range(self.numX+1)
		else: rangeIter = range(-1, self.numX-1, -1)

		for xi in rangeIter:
			self.play(self.wheel.highlightNumber(xi, YELLOW, False), run_time=0.4)
			self.play(self.wheel.dehighlightNumber(xi, False), run_time=0.3)
		self.play(self.x.animate.set_color(WHITE))

		self.play(self.y.animate.set_color(GREEN))

		if self.numY >= 0 and self.numX >= 0: xi += 1
		elif self.numY >= 0 and self.numX < 0: xi += 1
		elif self.numY < 0 and self.numX >= 0: xi -= 1
		else: xi -= 1
		# xi is used to index from the right

		self.play(FadeIn(self.wheel.setupArrow(xi)))

		if self.numY >= 0:
			for yi in range(self.numY):
				anims:list[Animation|AnimationGroup|VMobject] = []

				if yi != self.numY-1: anims.append(self.wheel.rotateArrow())

				blink = False
				if xi+yi >= self.wheel.totalSlices/2:
					if not self.wheel.flag: self.wheel.flag = True
					mathNum, animMathNum = self.wheel.highlightMathNumber(xi + yi, GREEN)
					anims.append(animMathNum)
					blink = True

				anims.append(self.wheel.highlightNumber(xi + yi, ORANGE, blink))
				self.play(*anims, run_time=0.4)

				self.play(self.wheel.dehighlightNumber(xi + yi, blink), run_time=0.3)
				if self.wheel.flag: self.play(self.wheel.dehighlightMathNumber(mathNum, xi + yi), run_time=0.3)
		else:
			# numY being negative would mean for the indices to be decrementing
			# Since the real indices is taken care of in highlightNumber(), the pseudo
			
			for yi in range(self.numY, 0):
				# yi is used to simply as a counting method, doing range(abs(numY)) would still work

				numberText = int(self.wheel.getNumber(xi).text)
				numberText = self.wheel._toUnsigned(numberText) if numberText < 0 else numberText

				anims:list[Text|Succession|Rotate] = []
				if yi != -1: anims.append(self.wheel.rotateArrow(False))

				blink = False
				if abs(xi) > self.wheel.totalSlices/2:
					if not self.wheel.flag: self.wheel.flag = True
					# print("Overflow")
					mathNum, animMathNum = self.wheel.highlightMathNumber(xi, GREEN)
					anims.append(animMathNum)
					blink = True

				anims.append(self.wheel.highlightNumber(numberText, ORANGE, blink))
				self.play(*anims, run_time=0.4)

				self.play(self.wheel.dehighlightNumber(numberText, blink), run_time=0.3)
				if self.wheel.flag: self.play(self.wheel.dehighlightMathNumber(mathNum, xi), run_time=0.3)

				xi -= 1

		self.play(self.x.animate.set_color(WHITE))

	def math(self): 
		res = MathTex(f"{self._sum}").to_edge(DOWN)

		mathSumText = MathTex(f"s = {self.numX} + {self.numY}").next_to(self.y, DOWN * 1).shift(RIGHT * 0.5)
		self.play(FadeIn(mathSumText))

		equ:str = None
		equstr0:str = None
		equstr1:str = None
		endequstr = str(self._sum) + " = " + str(self._sum)

		if self.mathSum >= self.upperBound:
			equ = MathTex(" = s - 2^n").next_to(res)
			equstr0 = str(self._sum) + " = " + str(self.mathSum) + " - 2^" + str(self.nbits)
			equstr1 = str(self._sum) + " = " + str(self.mathSum) + " - " + str(2**self.nbits)
		elif self.mathSum < self.lowerBound:
			equ = MathTex(" = s + 2^n").next_to(res)
			equstr0 = str(self._sum) + " = " + str(self.mathSum) + " + 2^" + str(self.nbits)
			equstr1 = str(self._sum) + " = " + str(self.mathSum) + " + " + str(2**self.nbits)
		else:
			equ = MathTex(" = s").next_to(res)

		self.play(TransformFromCopy(self.wheel.getNumber(self._sum), res))

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

	def construct(self):
		self.intro()

		self.wait(0.25)

		self.wheelAnim()

		self.wait(0.5)

		self.math()

		self.wait(2)