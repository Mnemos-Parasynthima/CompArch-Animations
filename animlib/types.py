from manim import VGroup, ManimColor, Text, RIGHT

from .hexdec import Hexadecimal
from .funcs import inttstr

from enum import Enum
# class Char(VGroup):
# 	def __init__(self, symbol, value, color):
# 		super().__init__()

# 		self.symbol:

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

		typeTextVal = _type.value if _type != TypeEnum.POINTER else (_ptrType.value + _type.value)
		typeText = Text(typeTextVal + " " + symbol + " = " + value + ";", font_size=fontSize, color=color)
		# symbolText = Text(symbol, font_size=fontSize)
		# valueText = Text(value, font_size=fontSize)

		# self.line = VGroup(typeText)
		# self.line.arrange(RIGHT)
		# self.add(self.line)
		self.add(typeText)

	def sizeof(self) -> int:
		if self.type == TypeEnum.CHAR: return 1
		elif self.type == TypeEnum.SHORT: return 2
		elif self.type == TypeEnum.INT: return 4
		else: return 8