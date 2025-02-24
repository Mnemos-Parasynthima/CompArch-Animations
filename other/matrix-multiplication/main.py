from manim import *

from Matrix import Matrix

class Kernel(Scene):
	def __init__(self):
		super().__init__()

		# The values for each m*/n* means how much does that dimension consists of
		# For example, in the diagram, kc first appears in the 4th loop
		# Tracing it down leads to kc being the number of rectangles (or columns), which is 10
		# Another example, for mr and nr, they first appear in the 2nd loop
		# Tracing it down leads to an unspecified number, but appears as one
		self.mr = 1
		self.mc = 3
		self.m = 3
		self.nr = 1
		self.nc = 8
		self.n = 2
		self.kc = 10
		self.k = 3

		self.A:Matrix = None
		self.B:Matrix = None
		self.C:Matrix = None
		self.cross:MathTex = None
		self.iteration:MathTex = None

	def microkernel(self):
		title = Text("Microkernel", font_size=20)
		title.to_corner(UL)

		Cr = Matrix(self.mr, self.nr, "mr", "nr", self.mr, self.nr, RED)
		Cr.to_edge(LEFT, buff=1)

		Ar = Matrix(self.mr, self.kc, "mr", "kc", 1, 0.5, GREEN)

		Br = Matrix(self.kc, self.nr, "kc", "nr", 0.5, 1, BLUE)
		Br.to_edge(RIGHT)

		self.play(FadeIn(
			Cr, Ar, Br,
			*Ar.showLabels(),
			*Br.showLabels(),
			*Cr.showLabels(),
			title
		))

		for i in range(self.kc):
			self.play(Ar.highlightRowCol(i), Br.highlightRowCol(i))

			ArVec = Ar.getVector(i).copy().set_fill(BLACK, 1)
			BrVec = Br.getVector(i).copy().set_fill(BLACK, 1)
			ArVec.to_edge(UP)
			self.cross = MathTex("\\times").next_to(ArVec, RIGHT, buff=0.2)
			BrVec.next_to(self.cross, RIGHT, buff=0.2)

			self.play(TransformFromCopy(Ar.getVector(i), ArVec), FadeIn(self.cross), TransformFromCopy(Br.getVector(i), BrVec))

			mat = VGroup(ArVec, BrVec)
			self.play(FadeTransform(mat, Cr), FadeOut(self.cross), Ar.dehighlightRowCol(i), Br.dehighlightRowCol(i))

		self.wait(0.2)

		self.play(Ar.hideLabels(), Br.hideLabels(), Cr.hideLabels(), Cr.animate.set_color(WHITE, 1), FadeOut(title))

		self.A = Ar
		self.B = Br
		self.C = Cr

	def loop1(self):
		iteration = MathTex("i = 0").to_corner(UL)

		Cc = Matrix(self.mc, self.nr, "mc", "nr", self.mc/self.mc, self.nr).to_edge(LEFT, buff=1)

		Ac = Matrix(self.mc, self.kc//self.kc, "mc", "kc", self.mc/self.mc, 0.5 * self.kc, GREEN)

		Bc = Matrix(self.kc//self.kc, self.nr, "kc", "nr", self.kc * 0.5, self.nr, BLUE).to_edge(RIGHT)

		self.cross.next_to(Ac, RIGHT, buff=1)

		self.play(
			ReplacementTransform(self.C, Cc),
			ReplacementTransform(self.A, Ac),
			ReplacementTransform(self.B, Bc),
			FadeIn(*Ac.showLabels(), *Bc.showLabels(), *Cc.showLabels(), self.cross, iteration)
		)

		for i in range(self.mc):
			AcVec = Ac.getVector(i).copy()
			BcVec = Bc.getVector(0).copy()

			self.play(Ac.highlightRowCol(i), Bc.highlightRowCol(0))

			mat = VGroup(AcVec, BcVec)
			self.play(FadeTransform(mat, Cc.getVector(i)), Ac.dehighlightRowCol(i))

		self.wait(0.2)

		self.play(Ac.hideLabels(), Bc.hideLabels(), Cc.hideLabels(), Cc.animate.set_color(WHITE, 1), Bc.dehighlightRowCol(0), FadeOut(self.cross))

		self.iteration = iteration
		self.A = Ac
		self.B = Bc
		self.C = Cc

	def loop2(self):
		iteration = MathTex("i = 1").to_corner(UL)

		Ai = Matrix(self.mc//self.mc, self.kc//self.kc, "mc", "kc", 0.5*self.mc, 0.15 * self.kc, GREEN)

		Bp = Matrix(self.kc//self.kc, self.nc, "kc", "nc", 0.15*self.kc, 0.0625*self.nc, PURPLE).to_edge(RIGHT)

		Ci = Matrix(self.mc//self.mc, self.nc, "mc", "nc", 0.5*self.mc, 0.0625*self.nc).to_edge(LEFT, buff=0.9)

		self.cross.next_to(Ai, RIGHT, buff=0.5)

		self.play(
			ReplacementTransform(self.C, Ci),
			ReplacementTransform(self.A, Ai),
			ReplacementTransform(self.B, Bp),
			ReplacementTransform(self.iteration, iteration),
			FadeIn(*Ai.showLabels(), *Bp.showLabels(), *Ci.showLabels(), self.cross)
		)

		for i in range(self.nc):
			AiVec = Ai.getVector(0).copy()
			BpVec = Bp.getVector(i).copy()

			self.play(Ai.highlightRowCol(0), Bp.highlightRowCol(i))

			mat = VGroup(AiVec, BpVec)
			self.play(FadeTransform(mat, Ci.getVector(i)), Bp.dehighlightRowCol(i))

		self.wait(0.2)

		self.play(Ai.hideLabels(), Bp.hideLabels(), Ci.hideLabels(), Ai.dehighlightRowCol(0), FadeOut(self.cross))

		self.iteration = iteration
		self.A = Ai
		self.B = Bp
		self.C = Ci

	def loop3(self):
		iteration = MathTex("i = 2").to_corner(UL)

		Ap = Matrix(self.m, self.kc//self.kc, "m", "kc", 0.5*self.mc, 0.15*self.kc)

		Bp = Matrix(self.kc//self.kc, self.nc//self.nc, "kc", "nc", 0.15*self.kc, 0.5*self.nc, PURPLE).to_edge(RIGHT)

		Cj = Matrix(self.m, self.nc//self.nc, "m", "nc", 0.5*self.mc, 0.5*self.nc).to_edge(LEFT, buff=0.75)

		self.cross.next_to(Ap, RIGHT, buff=0.5)

		self.play(
			ReplacementTransform(self.C, Cj),
			ReplacementTransform(self.A, Ap),
			ReplacementTransform(self.B, Bp),
			ReplacementTransform(self.iteration, iteration),
			FadeIn(*Ap.showLabels(), *Bp.showLabels(), *Cj.showLabels(), self.cross)
		)

		for i in range(self.mc):
			ApVec = Ap.getVector(i).copy()
			BpVec = Bp.getVector(0).copy()

			self.play(Ap.highlightRowCol(i), Bp.highlightRowCol(0))

			mat = VGroup(ApVec, BpVec)
			self.play(FadeTransform(mat, Cj.getVector(i)), Ap.dehighlightRowCol(i))

		self.wait(0.2)

		self.play(Ap.hideLabels(), Bp.hideLabels(), Cj.hideLabels(), Bp.dehighlightRowCol(0), FadeOut(self.cross))

		self.iteration = iteration
		self.A = Ap
		self.B = Bp
		self.C = Cj

	def loop4(self):
		iteration = MathTex("i = 3").to_corner(UL)

		A = Matrix(self.m//self.m, self.k, "m", "k", self.mc, 1)

		Bj = Matrix(self.k, self.nc//self.nc, "k", "nc", 1, self.mc).to_edge(RIGHT)

		Cj = Matrix(self.m//self.m, self.nc//self.nc, "m", "nc", self.mc, self.mc).to_edge(LEFT, buff=1)

		self.cross.next_to(A, RIGHT, buff=0.75)

		self.play(
			ReplacementTransform(self.C, Cj),
			ReplacementTransform(self.A, A),
			ReplacementTransform(self.B, Bj),
			ReplacementTransform(self.iteration, iteration),
			FadeIn(*A.showLabels(), *Bj.showLabels(), *Cj.showLabels(), self.cross)
		)

		for i in range(self.k):
			AiVec = A.getVector(i).copy()
			BpVec = Bj.getVector(i).copy()

			self.play(A.highlightRowCol(i), Bj.highlightRowCol(i))

			mat = VGroup(AiVec, BpVec)
			self.play(FadeTransform(mat, Cj), A.dehighlightRowCol(i), Bj.dehighlightRowCol(i))

		self.wait(0.2)

		self.play(A.hideLabels(), Bj.hideLabels(), Cj.hideLabels(), FadeOut(self.cross))

		self.iteration = iteration
		self.A = A
		self.B = Bj
		self.C = Cj

	def loop5(self):
		iteration = MathTex("i = 4").to_corner(UL)

		A = Matrix(self.m//self.m, self.k//self.k, "m", "k", 2.2, 2.2)

		B = Matrix(self.kc//self.kc, self.n, "k", "n", 2.2, 2.2)
		B.to_edge(RIGHT, buff=0.25)

		C = Matrix(self.m//self.m, self.n, "m", "n", 2.2, 2.2)
		C.to_edge(LEFT, buff=0.75)

		self.cross.next_to(A, RIGHT, buff=0.4)

		self.play(
			ReplacementTransform(self.C, C),
			ReplacementTransform(self.A, A),
			ReplacementTransform(self.B, B),
			ReplacementTransform(self.iteration, iteration),
			FadeIn(*A.showLabels(), *B.showLabels(), *C.showLabels(), self.cross)
		)

		for i in range(2):
			AVec = A.getVector(0).copy()
			BVec = B.getVector(i).copy()

			self.play(A.highlightRowCol(0), B.highlightRowCol(i))

			mat = VGroup(AVec, BVec)
			self.play(FadeTransform(mat, C), A.dehighlightRowCol(0), B.dehighlightRowCol(i))

	def construct(self):
		# MICROKERNEL
		self.microkernel()

		# START 1ST LOOP AROUND MICRO-KERNEL
		self.loop1()

		# START 2ND LOOP AROUND MICRO-KERNEL
		self.loop2()

		# START 3RD LOOP
		self.loop3()

		# START 4TH LOOP
		self.loop4()

		# START 5TH LOOP
		self.loop5()

		self.wait(1)

if __name__ == "__main__":
	kernel = Kernel()
	kernel.render()