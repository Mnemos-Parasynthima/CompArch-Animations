from manim import VMobject, ManimColor
from manim.typing import Point3DLike_Array


class Path(VMobject):
	def __init__(self, *points:Point3DLike_Array, color:ManimColor, strokeWidth:float):
		super().__init__()
		self.points = points
		self.set_points_as_corners(points)
		self.set_stroke(color, strokeWidth)