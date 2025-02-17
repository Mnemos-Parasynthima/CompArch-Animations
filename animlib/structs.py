from manim import VGroup, Text, DOWN, LEFT, RIGHT, ManimColor, Table, ORIGIN
from .types import Type, TypeEnum

from typing_extensions import Self
from abc import ABC, abstractmethod


class DerivedType(VGroup, ABC):
	def __init__(self, objs:list[type]):
		super().__init__()

		# Potential issue: The objs in self.objs are not the same as the ones stored in the VGroup
		# since later, it does self.add(obj)
		# If a change is done in one (either self.objs[i] or self.submobjects[i]), it won't be reflected on the other
		# Note to self: this behaviour is now used in swap
		# self.objs is to maintain the original order while self.submobjects is to deal with appearance
		self.objs = objs
		self.objsLen = len(objs)
		self.paddings:list[int] = []

	def __len__(self):
		return self.objsLen

	def __getitem__(self, index:int) -> Type:
		return self.submobjects[index+1]
	
	@abstractmethod
	def sizeof(self) -> int:
		'''
		Returns the number of bytes the structure occupies, including padding.
		'''
		pass

	@abstractmethod
	def swap(self, propIdx1:int, propIdx2:int) -> list[Type]:
		'''
		Swaps two given properties. This might affect padding.
		'''
		pass

	def getAlignBy(self) -> int:
		return self.alignBy

	def propSizeof(self, index:int) -> tuple[int, int]:
		'''
		Returns the size of bytes of the property indicated by the given index, as well as the padding it requires.
		'''
		prop:Type = self[index]
		propSize = prop.sizeof()

		padding = self.paddings[index]

		return propSize, padding

	def highlightProperty(self, index:int, color:ManimColor) -> Type:
		_type:Type = self.submobjects[index+1]

		# return _type.animate.set_color(color)
		return _type.animate.scale(1.5)
	
	def dehighlightProperty(self, index:int) -> Type:
		_type:Type = self.submobjects[index+1]
		originalColor = _type._color

		# return _type.animate.set_color(originalColor)
		return _type.animate.scale(0.65, about_edge=ORIGIN)

class Struct(DerivedType):
	def __init__(self, name:str, objs:list[Type], fontSize=14):
		assert(len(objs) != 0)

		super().__init__(objs)

		self.structName = name

		self.add(Text(f"struct {name} {{", font_size=fontSize))

		# To reduce the constant for O(n), do the max alignBy, adding, and padding at the same time
		maxAlign:int = 0
		offset = 0
		for obj in self.objs:
			self.add(obj)

			objSizeof = obj.sizeof()
			if objSizeof > maxAlign: maxAlign = objSizeof

			align = objSizeof

			padding = (align - (offset % align)) % align
			offset += padding + objSizeof

			self.paddings.append(padding)

		self.alignBy = maxAlign
		finalPadding = (self.alignBy - (offset % self.alignBy)) % self.alignBy
		self.paddings.append(finalPadding)
		# There will always be a padding of 0 at the beginning
		self.paddings.remove(0)
		self._sizeof = offset + finalPadding
		
		self.add(Text("};", font_size=fontSize))

		self.arrange(DOWN, aligned_edge=LEFT)

		for i in range(1, len(objs)+1):
			self.submobjects[i].shift(RIGHT * 0.2)

	def sizeof(self) -> int:
		return self._sizeof
	
	def swap(self, propIdx1, propIdx2):
		prop1 = self[propIdx1]
		prop2 = self[propIdx2]

		prop1Pos = prop1.get_left()
		prop2Pos = prop2.get_left()

		swapped:list[Type] = []
		swapped.append(prop2.animate.move_to(prop1Pos, LEFT))
		swapped.append(prop1.animate.move_to(prop2Pos, LEFT))

		# Even though swapping occurs, keep the original order in self.objs
		# However, make the change occur in self.submobjects
		self.submobjects[propIdx1+1] = prop2
		self.submobjects[propIdx2+1] = prop1

		# Note that swapping the order changes the padding
		# This will need to be re-calculated again
		# TODO: find a way to do it without having to do it in O(n)
		self.paddings.clear()

		offset = 0
		for obj in self.submobjects:
			if not isinstance(obj, Type):
				# Since it's working on self.submobjects (refer to earlier comment)
				# Need to skip the initial and last text
				continue

			obj:Type = obj
			objSizeof = obj.sizeof()

			align = objSizeof

			padding = (align - (offset % align)) % align
			offset += padding + objSizeof

			self.paddings.append(padding)

		# self.alignBy = maxAlign
		finalPadding = (self.alignBy - (offset % self.alignBy)) % self.alignBy
		self.paddings.append(finalPadding)
		# There will always be a padding of 0 at the beginning
		self.paddings.remove(0)
		self._sizeof = offset + finalPadding

		return swapped

class Union_(DerivedType):
	def __init__(self, name:str, objs:list[Type], fontSize=14):
		assert(len(objs) != 0)

		super().__init__(objs)

		self.unionName = name

		self.add(Text(f"union {name} {{", font_size=fontSize))
		
		maxAlign:int = 0
		for obj in self.objs:
			self.add(obj)

			objSizeof = obj.sizeof()
			if objSizeof > maxAlign: maxAlign = objSizeof

		self.alignBy = maxAlign

		# Another pass is needed since the max alignment needs to be known
		for obj in self.objs:
			objSizeof = obj.sizeof()
			padding = (maxAlign - objSizeof) % maxAlign
			self.paddings.append(padding)
	
		self.add(Text("};", font_size=fontSize))

		self.arrange(DOWN, aligned_edge=LEFT)

		for i in range(1, len(objs)+1):
			self.submobjects[i].shift(RIGHT * 0.2)

	def sizeof(self) -> int:
		return self.alignBy

	def swap(self, propIdx1, propIdx2):
		prop1 = self[propIdx1]
		prop2 = self[propIdx2]

		prop1Pos = prop1.get_left()
		prop2Pos = prop2.get_left()

		swapped:list[Type] = []
		swapped.append(prop2.animate.move_to(prop1Pos, LEFT))
		swapped.append(prop1.animate.move_to(prop2Pos, LEFT))

		# Even though swapping occurs, keep the original order in self.objs
		# However, make the change occur in self.submobjects
		self.submobjects[propIdx1+1] = prop2
		self.submobjects[propIdx2+1] = prop1

		# Note that swapping the order changes the padding
		# This will need to be re-calculated again
		# TODO: find a way to do it without having to do it in O(n)
		self.paddings.clear()

		for obj in self.submobjects:
			if not isinstance(obj, Type):
				# Since it's working on self.submobjects (refer to earlier comment)
				# Need to skip the initial and last text
				continue

			objSizeof = obj.sizeof()
			padding = (self.alignBy - objSizeof) % self.alignBy
			self.paddings.append(padding)

		return swapped

class StructTable(Table):
	def __init__(self, struct:Struct):
		self.rows = struct.objsLen + len(struct.paddings) + 1

		table:list[list[str]] = []

		# print(struct.size, len(struct.paddings))
		for m, p in zip(range(len(struct)), range(len(struct.paddings))):
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