from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from animlib.numwheel import NumberWheel
from animlib.bitvector import Bitvector

from manim import *
from numpy import cos, sin, array, radians


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

		vec:Bitvector = None
		for vec in vecGroup.submobjects:
			anim, elemSq = vec.toSquares()
			self.play(anim)

		self.wait(1)

		# temp = VGroup(dots)

		for vec, i in zip(vecGroup.submobjects, range(len(vecGroup.submobjects))):
			if i == 4:
				self.play(dots.animate.move_to(ORIGIN, ORIGIN).to_edge(buff=3*4 - 0.7))

			# TODO: Find a way to interpolate the transposing and the other movement
			self.play(vec.transpose())
			self.play(vec.animate.scale(2).move_to(ORIGIN, ORIGIN).to_edge(buff=3*i + 0.5))
			# temp += vec

		self.play(FadeOut(zeroVal), FadeOut(sumVal))

		self.wait(1)

		for vec in vecGroup.submobjects:
			self.play(FadeOut(vec.openBracket), FadeOut(vec.closeBracket))
			vec.remove(vec.openBracket, vec.closeBracket)
			vec.openBracket = None
			vec.closeBracket = None

		self.play(FadeOut(let0), FadeOut(let1), FadeOut(dots))

		wedges:list[VGroup] = []
		for vec in vecGroup.submobjects:
			wedge, anim = vec.toWedge()
			self.play(anim)
			wedges.append(wedge)
			# self.play(Create(Dot(wedge.get_bottom())))
			# self.play(Rotate(wedge, PI/5, about_point=wedge.get_bottom()))

		# TODO: Do the transformation such that it applies on the actual wedge itself
		# That is, no new object is to be created per wedge
		# Tried it at first but too much math and angles

		anims:list[VGroup] = []
		for i, _wedge in enumerate(wedges[:-1]):
			_wedgeTo = _wedge.copy()
			# self.play(Create(Dot(ORIGIN, color=RED)))
			_wedgeTo.move_to(ORIGIN, DOWN)
			# self.play(Create(Dot(_wedgeTo.get_bottom())))
			# print(f"Pos of bottom of _wedgeTo: {_wedgeTo.get_bottom()}")
			_wedgeTo.rotate(-TAU/10 * i - 0.3, about_point=ORIGIN)

			anims.append(ReplacementTransform(_wedge, _wedgeTo))
			# anims.append(_wedge.animate.move_to(pos).rotate(rotateBy).build())
		# Edge case
		_wedgeTo = wedges[-1].copy().move_to(ORIGIN, DOWN).rotate(-TAU/10 * 9 - 0.3, about_point=ORIGIN)
		anims.append(ReplacementTransform(wedges[-1], _wedgeTo))

		self.play(Succession(anims, run_time=5))
		
		temp = VGroup(*wedges)

		wheel = NumberWheel(4)
		# self.play(FadeIn(wheel))

		self.play(ReplacementTransform(temp, wheel))

		text = MathTex("n\\text{-th Unsigned Number Wheel for vectors }b").to_edge(DOWN, buff=0.75)
		self.play(Write(text))

		self.wait(1)

		self.play(wheel.flipSignedness())
		newText = MathTex("n\\text{-th Signed Number Wheel for vectors }b").to_edge(DOWN, buff=0.75)
		self.play(Transform(text, newText, replace_mobject_with_target_in_scene=True))
		newTextAdd = MathTex("\\text{using Two's Complement}").next_to(newText, DOWN, 0.2)
		self.play(Write(newTextAdd))

		self.wait(1)