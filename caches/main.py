from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from Read import CacheRead
from Write import CacheWrite
from Intro import Intro


def main():
	pass


if __name__ == "__main__":
	# main()
	scene = Intro()
	scene = CacheRead()
	scene = CacheWrite()
	scene.render()