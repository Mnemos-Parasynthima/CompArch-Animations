from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.numwheel import NumberWheel
from animlib.bitvector import Bitvector

from manim import *


class Intro(Scene):
	def construct(self):
		let0 = MathTex("\\text{Let } n = 4").scale(0.75).to_edge(UP).to_edge(LEFT, buff=0.1)
		let1 = MathTex("\\text{Let vector } b \\text{ of length } n").scale(0.75).next_to(let0, DOWN, buff=0.25).to_edge(LEFT, buff = 0.1)

		self.play(Write(let0))
		self.play(Write(let1))

		templ = Bitvector().scale(2)
		self.play(FadeIn(templ))

		self.wait(0.2)

		self.play(templ.showLabels())
		self.wait(0.1)
		self.play(templ.updateLabels())

		self.wait(0.1)

		zeroVec = Bitvector(placeholder=False).scale(1.5)
		zeroVec.next_to(templ, DOWN, buff=0.25)
		self.play(TransformFromCopy(templ, zeroVec))

		self.wait(1)

		zeroVal = Integer()
		zeroVal.to_corner()
		self.play(Transform(zeroVec, zeroVal, replace_mobject_with_target_in_scene=True))

		oneVec = Bitvector(vec=[1,1,1,1], placeholder=False).scale(1.5)
		oneVec.next_to(templ, DOWN, buff=0.25)
		self.play(TransformFromCopy(templ, oneVec))

		self.wait(1)

		sumVal = Integer(15)
		sumVal.to_corner(DR)
		self.play(Transform(oneVec, sumVal, replace_mobject_with_target_in_scene=True))

		self.wait(0.5)

		self.play(templ.hideLabels())

		zeroVec = Bitvector(placeholder=False).scale(1.5)
		zeroVec.to_edge(UP, buff=1)
		self.play(TransformFromCopy(templ, zeroVec))

		vec1 = Bitvector(vec=[0,0,0,1], placeholder=False).scale(1.5)
		vec1.next_to(zeroVec, DOWN, buff=0.5)
		self.play(TransformFromCopy(templ, vec1))

		vec2 = Bitvector(vec=[0,0,1,0], placeholder=False).scale(1.5)
		# No need to set its position as it should be in the same position as templ
		self.play(Transform(templ, vec2, replace_mobject_with_target_in_scene=True))

		vec3 = Bitvector(vec=[0,0,1,1], placeholder=False).scale(1.5)
		vec3.next_to(vec2, DOWN, buff=0.45)
		self.play(TransformFromCopy(vec2, vec3))

		dots = Text("...")
		dots.next_to(vec3, DOWN, buff=0.5)
		self.play(FadeIn(dots))

		oneVec = Bitvector(vec=[1,1,1,1], placeholder=False).scale(1.5)
		oneVec.next_to(dots, DOWN, buff=0.5)
		self.play(TransformFromCopy(vec2, oneVec))

		self.wait(0.5)

		vecGroup = VGroup(zeroVec, vec1, vec2, vec3, oneVec)

		for vec in vecGroup.submobjects:
			self.play(vec.toSquares())

		self.wait(1)

		temp = VGroup(dots)

		for vec, i in zip(vecGroup.submobjects, range(len(vecGroup.submobjects))):
			if i == 4:
				self.play(dots.animate.move_to(ORIGIN, ORIGIN).to_edge(buff=3*4 - 0.7))

			# TODO: Find a way to interpolate the transposing and the other movement
			self.play(vec.transpose())
			self.play(vec.animate.scale(2).move_to(ORIGIN, ORIGIN).to_edge(buff=3*i + 0.5))
			temp += vec

		self.play(FadeOut(zeroVal), FadeOut(sumVal))

		self.wait(1)

		wheel = NumberWheel(4)

		self.play(Transform(temp, wheel, replace_mobject_with_target_in_scene=True))

		text = MathTex("n\\text{-th Unsigned Number Wheel for vectors }b").to_edge(DOWN, buff=0.75)
		self.play(Write(text))

		self.wait(1)

		self.play(wheel.flipSignedness())
		newText = MathTex("n\\text{-th Signed Number Wheel for vectors }b").to_edge(DOWN, buff=0.75)
		self.play(Transform(text, newText, replace_mobject_with_target_in_scene=True))
		newTextAdd = MathTex("\\text{using Two's Complement}").next_to(newText, DOWN, 0.2)
		self.play(Write(newTextAdd))

		self.wait(1)