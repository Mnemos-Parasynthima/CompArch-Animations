from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from Read import Read
from Write import Write
from Intro import Intro


def main():
	pass


if __name__ == "__main__":
	# main()
	# scene = Intro()
	scene = Read()
	scene = Write()
	scene.render()