from manim import VGroup, Text, DOWN, LEFT, RIGHT, ManimColor
from .types import Type, TypeEnum


class Struct(VGroup):
	def __init__(self, name:str, objs:list[Type], fontSize=14):
		assert(len(objs) != 0)

		super().__init__()

		self.structName = name
		self.objs = objs
		self.size = len(objs)
		self.paddings:list[int] = []

		self.add(Text(f"struct {name} {{", font_size=fontSize))

		for obj in self.objs:
			self.add(obj)
			

		self.add(Text("};", font_size=fontSize))

		self.arrange(DOWN, aligned_edge=LEFT)

		for i in range(1, len(objs)+1):
			self.submobjects[i].shift(RIGHT * 0.2)

		# print(type(struct), type(self))

		# print(len(self.submobjects))

	def __len__(self):
		return self.size

	def __getitem__(self, index) -> Type:
		return self.submobjects[index+1]

	def getSize(self) -> int:
		alignBy = max(prop.sizeof() for prop in self.objs)
		offset = 0

		for prop in self.objs:
			size = prop.sizeof()
			align = size

			padding = (align - (offset % align)) % align
			offset += padding + size

			self.paddings.append(padding)

		finalPadding = (alignBy - (offset % alignBy)) % alignBy
		self.paddings.append(finalPadding)
		# There will always be a padding of 0 at the beginning
		self.paddings.remove(0)
		
		return offset + finalPadding

	def sizeof(self, index:int) -> tuple[int, int]:
		prop:Type = self[index]
		propSize = prop.sizeof()

		padding = self.paddings[index]

		return propSize, padding

	def highlightProperty(self, index:int, color:ManimColor) -> Type:
		_type:Type = self.submobjects[index+1]

		return _type.animate.set_color(color)
	
	def dehighlightProperty(self, index:int) -> Type:
		_type:Type = self.submobjects[index+1]
		originalColor = _type._color

		return _type.animate.set_color(originalColor)