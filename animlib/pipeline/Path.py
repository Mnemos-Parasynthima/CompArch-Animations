from manim import TipableVMobject, ManimColor, Dot, ArrowTriangleFilledTip
from manim.typing import Point3DLike_Array, Point3D
from typing_extensions import Self

from numpy import empty

class Path(TipableVMobject):
	'''
	A path connecting two or more components.
	'''
	def __init__(self, *points:Point3DLike_Array, color:ManimColor, strokeWidth:float):
		super().__init__()
		self.pathPoints = points
		self.set_points_as_corners(points)
		self.set_stroke(color, strokeWidth)
		self.intersections:list[Dot] = None

	def markIntersections(self, indices:list[int], color:ManimColor) -> Self:
		selected:list[Point3D] = [self.pathPoints[i] for i in indices]

		self.intersections = [Dot(point, color=color) for point in selected]
		self.add(*self.intersections)

		return self
	
	def highlight(self, color:ManimColor, width:int) -> Self:
		return self.animate.set_color(color).set_stroke(width=width)
	
class ArrowPath(Path):
	def __init__(self, *points, color, strokeWidth):
		super().__init__(*points, color=color, strokeWidth=strokeWidth)

		# Doing self.add_tip() does some funky stuff regarding changing the points due to reset_endpoints_based_on_tip()
		# which change the path such that it is not always straight
		# The following code just takes what is important regarding tipping
		tip = self.create_tip(ArrowTriangleFilledTip, tip_length=0.15, tip_width=0.15, at_start=False)
		self.asign_tip_attr(tip, False)
		self.add(tip)
		# Without this, the line ends where it was indicated, that is it ends where the arrow tip also ends
		# But the line needs to end where the arrow tip begins, so manually set it
		# Note that using points[] changes the vmobject's property, it does not change self.pathPoints, so it remains with the original
		# This might present some unforeseeable bug
		self.points[-1] = tip.base

	def addPaths(self, pointsList:list[Point3DLike_Array]) -> Self:
		for points in pointsList:
			subPath = ArrowPath(*points, color=self.color, strokeWidth=self.stroke_width)

			# Since markIntersections works on the "first-level" of self.pathPoints
			# In order for markIntersections to work for any added subpath, include each new subpath's points in this pathPoints
			# Courtesy from VMobject::append_points
			n = len(self.pathPoints)
			points = empty((n + len(subPath.pathPoints), self.dim))
			points[:n] = self.pathPoints
			points[n:] = subPath.pathPoints
			self.pathPoints = points

			self.add(subPath)

		return self