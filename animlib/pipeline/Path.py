from manim import TipableVMobject, ManimColor, Dot, ArrowTriangleFilledTip
from manim.typing import Point3DLike_Array, Point3D
from typing_extensions import Self


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

	def markIntersections(self, indices:list[int], color:ManimColor):
		selected:list[Point3D] = [self.pathPoints[i] for i in indices]

		self.intersections = [Dot(point, color=color) for point in selected]
		self.add(*self.intersections)

		return self
	
	def highlight(self, color:ManimColor, width:int) -> Self:
		return self.animate.set_color(color).set_stroke(width=width)
	
class ArrowPath(Path):
	def __init__(self, *points, color, strokeWidth):
		super().__init__(*points, color=color, strokeWidth=strokeWidth)

		self.add_tip(tip_shape=ArrowTriangleFilledTip, tip_length=0.15, tip_width=0.15)