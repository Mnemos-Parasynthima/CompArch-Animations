from manim import VGroup, Text, DOWN, LEFT, RIGHT, ManimColor
from .types import Type, TypeEnum


class Struct(VGroup):
	def __init__(self, name:str, objs:list[Type], fontSize=14):
		assert(len(objs) != 0)

		super().__init__()

		self.structName = name
		self.objs = objs
		self.size = len(objs)


		self.add(Text(f"struct {name} {{", font_size=fontSize))

		for obj in self.objs:
			self.add(obj)
			

		self.add(Text("};", font_size=fontSize))

		self.arrange(DOWN, aligned_edge=LEFT)

		for i in range(1, len(objs)+1):
			self.submobjects[i].shift(RIGHT * 0.2)

		# print(type(struct), type(self))

		print(len(self.submobjects))

	def __len__(self):
		return self.size

	def getSize(self) -> int:
		'''

		'''
		alignBy = max(prop.sizeof() for prop in self.objs)
		offset = 0

		for prop in self.objs:
			size = prop.sizeof()
			align = size

			padding = (align - (offset % align)) % align
			offset += padding + size

		finalPadding = (alignBy - (offset % alignBy)) % alignBy
		return offset + finalPadding

	def highlightProperty(self, index:int, color:ManimColor) -> Type:
		_type:Type = self.submobjects[index+1]

		return _type.animate.set_color(color)
	
	def dehighlightProperty(self, index:int) -> Type:
		_type:Type = self.submobjects[index+1]
		originalColor = _type._color

		return _type.animate.set_color(originalColor)