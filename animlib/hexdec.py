from manim import VGroup, Tex, TexTemplate, VMobject
from manim.opengl import OpenGLVGroup


class Verbatim(VMobject):
	def __init__(self, value:str, color:str = None, fontSize:int = 48, **kwargs):
		super().__init__(**kwargs)

		self.value = value
		
		verb = Tex(f"\\verb|{value}|", font_size=fontSize, color=color)
		self.add(verb)


class Hexadecimal(Verbatim):
	def __init__(self, value, color = None, fontSize = 48, **kwargs):
		super().__init__(value, color, fontSize, **kwargs)

		self.numval = -1 if (value == "0x" or value == "0b") else int(value, base=16)

# Doing `Verbatim()` for text to be seen as code is too not clear
# Maybe there is a better way to create a different name/alias

class CodeBlock(Verbatim):
	def __init__(self, value, color = None, fontSize = 48, **kwargs):
		super().__init__(value, color, fontSize, **kwargs)