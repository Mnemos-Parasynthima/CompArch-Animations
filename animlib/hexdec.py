from manim import VGroup, Tex, TexTemplate
from manim.opengl import OpenGLVGroup

class Hexadecimal(VGroup):
	def __init__(self, value:str, color:str = None, fontSize:int = 48, **kwargs):
		super().__init__(**kwargs)

		self.value = value
		self.numval = -1 if (value == "0x" or value == "0b") else int(value, base=16)
		num = Tex(f"\\verb|{value}|", font_size=fontSize, color=color)

		self.add(num)