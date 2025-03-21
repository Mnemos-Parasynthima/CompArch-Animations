import ctypes as c

class Tuple(c.Structure): 
	_fields_ = [("src2sel", c.c_bool), ("src2_1", c.c_uint8), ("src2_2", c.c_uint8), ("src2", c.c_uint8)]

class SELib:
	def __init__(self, lib:str):
		self.lib = c.CDLL(lib)

		self.lib.initMachine.argtypes = None
		self.lib.initMachine.restype = c.c_void_p

		self.lib.initGlobals.argtypes = None
		self.lib.initGlobals.restype = c.c_void_p

		self.lib.shutdownMachine.argtypes = [c.c_void_p, c.c_void_p]
		self.lib.shutdownMachine.restype = None

		self.lib.loadElf.argtypes = [c.c_char_p, c.c_void_p]
		self.lib.loadElf.restype = c.c_uint64

		self.lib.initRunElf.argtypes = [c.c_uint64, c.c_void_p]
		self.lib.initRunElf.restype = None

		self.lib.postCycle.argtypes = [c.c_void_p, c.c_void_p]
		self.lib.postCycle.restype = None

		self.lib.fetchInstr.argtypes = [c.c_void_p, c.c_void_p]
		self.lib.fetchInstr.restype = None

		self.lib.decodeInstr.argtypes = [c.c_void_p, c.c_void_p]
		self.lib.decodeInstr.restype = None


		# API FUNCTIONS
		self.lib.getBranchOffset.argtypes = [c.c_void_p, c.c_void_p]
		self.lib.getBranchOffset.restype = c.c_uint64

		self.lib.getImmval.argtypes = [c.c_void_p]
		self.lib.getImmval.restype = c.c_int64

		self.lib.getDecodeDstSel.argtypes = [c.c_void_p]
		self.lib.getDecodeDstSel.restype = c.c_bool

		self.lib.getDecodeDst.argtypes = [c.c_void_p]
		self.lib.getDecodeDst.restype = c.c_uint8

		self.lib.getDecodeSrc1.argtypes = [c.c_void_p]
		self.lib.getDecodeSrc1.restype = c.c_uint8

		self.lib.getDecodeSrc2Data.argtypes = [c.c_void_p]
		self.lib.getDecodeSrc2Data.restype = Tuple

		self.lib.getDecodeSrc2Sel.argtypes = [Tuple]
		self.lib.getDecodeSrc2Sel.restype = c.c_bool

		self.lib.getDecodeSrc2_1.argtypes = [Tuple]
		self.lib.getDecodeSrc2_1.restype = c.c_uint8

		self.lib.getDecodeSrc2_2.argtypes = [Tuple]
		self.lib.getDecodeSrc2_2.restype = c.c_uint8

		self.lib.getDecodeSrc2.argtypes = [Tuple]
		self.lib.getDecodeSrc2.restype = c.c_uint8

		self.lib.getValA.argtypes = [c.c_void_p]
		self.lib.getValA.restype = c.c_uint64

		self.lib.getValB.argtypes = [c.c_void_p]
		self.lib.getValB.restype = c.c_uint64



	def initMachine(self) -> c.c_void_p:
		return self.lib.initMachine()

	def shutdownMachine(self, guest:c.c_void_p, _globals:c.c_void_p) -> None:
		self.lib.shutdownMachine(guest, _globals)

	def initGlobals(self) -> c.c_void_p:
		return self.lib.initGlobals()

	def loadElf(self, file:str, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.loadElf(file.encode(), guest)
	
	def initRunElf(self, entry:c.c_uint64, guest:c.c_void_p) -> None:
		self.lib.initRunElf(entry, guest)

	def postCycle(self, guest:c.c_void_p, _globals:c.c_void_p) -> None:
		self.lib.postCycle(guest, _globals)

	def fetchInstr(self, guest:c.c_void_p, _globals:c.c_void_p) -> None:
		self.lib.fetchInstr(guest, _globals)

	def decodeInstr(self, guest:c.c_void_p, _globals:c.c_void_p) -> None:
		self.lib.decodeInstr(guest, _globals)


	def getBranchOffset(self, guest:c.c_void_p, _globals:c.c_void_p) -> c.c_int64:
		return self.lib.getBranchOffset(guest, _globals)
	
	def getImmval(self, guest:c.c_void_p) -> c.c_int64:
		return self.lib.getImmval(guest)
	
	def getDecodeDstSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getDecodeDstSel(guest)
	
	def getDecodeDst(self, guest:c.c_void_p) ->c.c_uint8:
		return self.lib.getDecodeDst(guest)

	def getDecodeSrc1(self, guest:c.c_void_p) ->c.c_uint8:
		return self.lib.getDecodeSrc1(guest)

	def getDecodeSrc2Data(self, guest:c.c_void_p) -> "Tuple":
		return self.lib.getDecodeSrc2Data(guest)
	
	def getDecodeSrc2Sel(self, _tuple:"Tuple") -> c.c_bool:
		return self.lib.getDecodeSrc2Sel(_tuple)
	
	def getDecodeSrc2_1(self, _tuple:"Tuple") -> c.c_uint8:
		return self.lib.getDecodeSrc2_1(_tuple)
	
	def getDecodeSrc2_2(self, _tuple:"Tuple") -> c.c_uint8:
		return self.lib.getDecodeSrc2_2(_tuple)
	
	def getDecodeSrc2(self, _tuple:"Tuple") -> c.c_uint8:
		return self.lib.getDecodeSrc2(_tuple)
	
	def getValA(self, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.getValA(guest)

	def getValB(self, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.getValB(guest)


__all__ = ["SELib"]