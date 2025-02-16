from manim import VGroup, ManimColor, Text

from enum import Enum


class TypeEnum(Enum):
	CHAR = "char"
	SHORT = "short"
	INT = "int"
	LONG = "long"
	POINTER = "*"

class Type(VGroup):
	def __init__(self, symbol:str, value:str, color:ManimColor, _type:TypeEnum, _ptrType:TypeEnum=None, fontSize=14):
		super().__init__()

		self.symbol = symbol
		self.value = value
		self._color = color
		self.type = _type

		self.completeType = _type.value if _type != TypeEnum.POINTER else (_ptrType.value + _type.value)
		typeText = Text(self.completeType + " " + symbol + " = " + value + ";", font_size=fontSize, color=color)

		self.add(typeText)

	def sizeof(self) -> int:
		if self.type == TypeEnum.CHAR: return 1
		elif self.type == TypeEnum.SHORT: return 2
		elif self.type == TypeEnum.INT: return 4
		else: return 8
