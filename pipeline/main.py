from PIPE import PIPEScene
from SEQ import SEQScene

class Pipeline():
	pass


if __name__ == "__main__":
	# scene = PIPEScene("asm-stripped.s")
	scene = SEQScene("asm-stripped.s")
	scene.render()