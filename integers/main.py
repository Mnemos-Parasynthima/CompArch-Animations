from sys import path
from pathlib import Path

path.append(str(Path(__file__).resolve().parent.parent))

from Addition import UnsignedAddition, SignedAddition
from Subtraction import UnsignedSubtraction, SignedSubtraction

# scene = UnsignedAddition(3, 3, 3)
# scene.render()
# scene.view()


# scene = SignedAddition(3, 3, 3)
# scene.render()
# scene.view()

scene = UnsignedSubtraction(3, 3, 3)
scene.render()
scene.view()