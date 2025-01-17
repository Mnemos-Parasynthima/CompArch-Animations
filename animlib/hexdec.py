from manim import VGroup, Tex, TexTemplate

class Hexadecimal(VGroup):
	def __init__(self, value:str, color:str = None, fontSize:int = 48, **kwargs):
		super().__init__(**kwargs)

		templ = TexTemplate()
		templ.add_to_preamble(r"\usepackage{verbatim}")

		num = Tex(f"\\verb|{value}|", font_size=fontSize, color=color)

		self.add(num)