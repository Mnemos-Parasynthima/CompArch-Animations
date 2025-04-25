from manim import config

from PIPE import PIPEScene
from SEQ import SEQScene


def main():
	file = input("File to run: ")

	choice = int(input("PIPE (0) or SEQ (1): "))
	while not (choice == 0 or choice == 1):
		choice = int(input("PIPE (0) or SEQ (1): "))

	scene:PIPEScene|SEQScene = None

	if choice == 0:
		scene = PIPEScene(file)
	elif choice == 1:
		scene = SEQScene(file)

	scene.render()



if __name__ == "__main__":
	config.preview = True
	main()

	# scene = SEQScene()
	# scene = PIPEScene()
	# scene.render()