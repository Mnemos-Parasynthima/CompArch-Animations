from manim import VMobject, ManimColor, Dot
from manim.typing import Point3DLike_Array, Point3D


class Path(VMobject):
	'''
	A path connecting two or more components.
	'''
	def __init__(self, *points:Point3DLike_Array, color:ManimColor, strokeWidth:float):
		super().__init__()
		self.pathPoints = points
		self.set_points_as_corners(points)
		self.set_stroke(color, strokeWidth)
		self.intersections:list[Dot] = None

	def markIntersections(self, indices:list[int], color:ManimColor):
		selected:list[Point3D] = [self.pathPoints[i] for i in indices]

		self.intersections = [Dot(point, color=color) for point in selected]
		self.add(*self.intersections)

		return self