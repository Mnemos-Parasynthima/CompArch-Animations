from manim import VGroup, Tex, TexTemplate
from manim.opengl import OpenGLVGroup

class Hexadecimal(VGroup):
	def __init__(self, value:str, color:str = None, fontSize:int = 48, **kwargs):
		super().__init__(**kwargs)

		self.value = value
		num = Tex(f"\\verb|{value}|", font_size=fontSize, color=color)

		self.add(num)