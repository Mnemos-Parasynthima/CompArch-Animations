from manim import VGroup, Text, DOWN, LEFT, RIGHT, ManimColor, Table
from .types import Type, TypeEnum

from typing_extensions import Self

class Struct(VGroup):
	def __init__(self, name:str, objs:list[Type], fontSize=14):
		assert(len(objs) != 0)

		super().__init__()

		self.structName = name
		self.objs = objs
		self.size = len(objs)
		self.alignBy = max(prop.sizeof() for prop in self.objs)
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

	def __getitem__(self, index:int) -> Type:
		return self.submobjects[index+1]

	def getAlignBy(self) -> int:
		return self.alignBy

	def getSize(self) -> int:
		'''
		Returns the number of bytes the structure occupies, including padding.
		'''
		offset = 0

		for prop in self.objs:
			size = prop.sizeof()
			align = size

			padding = (align - (offset % align)) % align
			offset += padding + size

			self.paddings.append(padding)

		finalPadding = (self.alignBy - (offset % self.alignBy)) % self.alignBy
		self.paddings.append(finalPadding)
		# There will always be a padding of 0 at the beginning
		self.paddings.remove(0)
		
		return offset + finalPadding

	def sizeof(self, index:int) -> tuple[int, int]:
		'''
		Returns the size of bytes of the property indicated by the given index, as well as the padding it requires.
		'''
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
	
	def swap(self, propIdx1:int, propIdx2:int) -> Self:
		'''
		Swaps two given properties. This might affect padding.
		'''
		pass

class Union(VGroup):
	def __init__(self):
		super().__init__()

class StructTable(Table):
	def __init__(self, struct:Struct):
		self.rows = struct.size + len(struct.paddings) + 1

		table:list[list[str]] = []

		# print(struct.size, len(struct.paddings))
		for m, p in zip(range(struct.size), range(len(struct.paddings))):
			prop = struct[m]
			pad:int = struct.paddings[p]

			print(prop.symbol, pad)
			table.append([prop.symbol, prop.completeType, str(prop.sizeof()), "2"])
			if pad != 0: table.append(["PAD", "char[]", str(pad), "1"])

		super().__init__(table,
											col_labels=[Text("Field"), Text("Type"), Text("Size"), Text("Offset")],
											include_outer_lines=True, arrange_in_grid_config={"cell_alignment": RIGHT})

	def highlightRow(self, index:int, color:ManimColor):
		colors:list[ManimColor] = [None] * self.rows
		colors[index] = color

		return self.animate.set_row_colors(*colors)