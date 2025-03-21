import ctypes as c


class SELib:
	def __init__(self, lib:str):
		self.lib = c.CDLL(lib)

		self.lib.initMachine.argtypes = None
		self.lib.initMachine.restype = c.c_void_p

		self.lib.initGlobals.argtypes = None
		self.lib.initGlobals.restype = c.c_void_p

		self.lib.shutdownMachine.argtypes = [c.c_void_p]
		self.lib.shutdownMachine.restype = None

		self.lib.loadElf.argtypes = [c.c_char_p, c.c_void_p]
		self.lib.loadElf.restype = c.c_uint64

		self.lib.initRunElf.argtypes = [c.c_uint64, c.c_void_p]
		self.lib.initRunElf.restype = None

		self.lib.postCycle.argtypes = [c.c_void_p, c.c_void_p]
		self.lib.postCycle.restype = None

	def initMachine(self) -> c.c_void_p:
		return self.lib.initMachine()

	def shutdownMachine(self, guest:c.c_void_p) -> None:
		self.lib.shutdownMachine(guest)

	def initGlobals(self) -> c.c_void_p:
		return self.lib.initGlobals()

	def loadElf(self, file:str, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.loadElf(file.encode(), guest)
	
	def initRunElf(self, entry:c.c_uint64, guest:c.c_void_p) -> None:
		self.lib.initRunElf(entry, guest)

	def postCycle(self, guest:c.c_void_p, _globals:c.c_void_p) -> None:
		self.lib.postCycle(guest, _globals)

__all__ = ["SELib"]