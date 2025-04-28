from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from Addition import UnsignedAddition, SignedAddition
from Subtraction import UnsignedSubtraction, SignedSubtraction


def main():
	choice = int(input("What type of Addition or Subtraction? [Unsigned Add:0, Signed Add:1, Unsigned Sub:2, Signed Sub:3, exit:-1]: "))

	while choice != -1:
		scene:UnsignedAddition|UnsignedSubtraction|SignedAddition|SignedSubtraction = None

		if choice == 0:
			scene = UnsignedAddition()
		elif choice == 1:
			scene = SignedAddition()
		elif choice == 2:
			scene = UnsignedSubtraction()
		elif choice == 3:
			scene = SignedSubtraction()
		
		scene.init()
		scene.render()
		# scene.view()

		choice = int(input("What type of Addition or Subtraction? [Unsigned Add:0, Signed Add:1, Unsigned Sub:2, Signed Sub:3, exit:-1] "))


if __name__ == "__main__":
	main()