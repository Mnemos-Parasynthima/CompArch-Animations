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

		self.lib.executeInstr.argtypes = [c.c_void_p]
		self.lib.executeInstr.restype = None

		self.lib.memoryInstr.argtypes = [c.c_void_p]
		self.lib.memoryInstr.restype = None

		self.lib.wbackInstr.argtypes = [c.c_void_p, c.c_void_p]
		self.lib.wbackInstr.restype = None

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

		self.lib.getValBSel.argtypes = [c.c_void_p]
		self.lib.getValBSel.restype = c.c_bool

		self.lib.getValEx.argtypes = [c.c_void_p]
		self.lib.getValEx.restype = c.c_uint64

		self.lib.getValHw.argtypes = [c.c_void_p]
		self.lib.getValHw.restype = c.c_uint8

		self.lib.getAluOp.argtypes = [c.c_void_p]
		self.lib.getAluOp.restype = c.c_int

		self.lib.getSetCC.argtypes = [c.c_void_p]
		self.lib.getSetCC.restype = c.c_bool

		self.lib.getCond.argtypes = [c.c_void_p]
		self.lib.getCond.restype = c.c_int

		self.lib.getCondVal.argtypes = [c.c_void_p]
		self.lib.getCondVal.restype = c.c_bool

		self.lib.getMemRead.argtypes = [c.c_void_p]
		self.lib.getMemRead.restype = c.c_bool

		self.lib.getMemWrite.argtypes = [c.c_void_p]
		self.lib.getMemWrite.restype = c.c_bool

		self.lib.getRVal.argtypes = [c.c_void_p]
		self.lib.getRVal.restype = c.c_uint64

		self.lib.getWvalSel.argtypes = [c.c_void_p]
		self.lib.getWvalSel.restype = c.c_bool

		self.lib.getWriteDstSel.argtypes = [c.c_void_p]
		self.lib.getWriteDstSel.restype = c.c_bool

		self.lib.getWEnable.argtypes = [c.c_void_p]
		self.lib.getWEnable.restype = c.c_bool

		self.lib.getNextPC.argtypes = [c.c_void_p]
		self.lib.getNextPC.restype = c.c_uint64


		self.lib.getRegisters.argtypes = [c.c_void_p]
		self.lib.getRegisters.restype = c.POINTER(c.c_uint64*31)

		self.lib.getSP.argtypes = [c.c_void_p]
		self.lib.getSP.restype = c.c_uint64

		self.lib.getPC.argtypes = [c.c_void_p]
		self.lib.getPC.restype = c.c_uint64

		self.lib.getNZCV.argtypes = [c.c_void_p]
		self.lib.getNZCV.restype = c.c_uint8



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

	def executeInstr(self, guest:c.c_void_p) -> None:
		self.lib.executeInstr(guest)

	def memoryInstr(self, guest:c.c_void_p) -> None:
		self.lib.memoryInstr(guest)

	def wbackInstr(self, guest:c.c_void_p, _globals:c.c_void_p) -> None:
		self.lib.wbackInstr(guest, _globals)


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
	
	def getValBSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getValBSel(guest)
	
	def getValEx(self, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.getValEx(guest)
	
	def getValHw(self, guest:c.c_void_p) -> c.c_uint8:
		return self.lib.getValHw(guest)

	def getAluOp(self, guest:c.c_void_p) -> c.c_int:
		return self.lib.getAluOp(guest)
	
	def getSetCC(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getSetCC(guest)
	
	def getCond(self, guest:c.c_void_p) -> c.c_int:
		return self.lib.getCond(guest)
	
	def getCondVal(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getCondVal(guest)

	def getMemRead(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getMemRead(guest)

	def getMemWrite(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getMemWrite(guest)

	def getRVal(self, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.getRVal(guest)
	
	def getWvalSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getWvalSel(guest)

	def getWriteDstSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getWriteDstSel(guest)

	def getWEnable(self, guest:c.c_void_p) -> c.c_bool:
		return self.lib.getWEnable(guest)

	def getNextPC(self, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.getNextPC(guest)


	def getRegisters(self, guest:c.c_void_p) -> c._Pointer:
		return self.lib.getRegisters(guest)
	
	def getSP(self, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.getSP(guest)
	
	def getPC(self, guest:c.c_void_p) -> c.c_uint64:
		return self.lib.getPC(guest)
	
	def getNZCV(self, guest:c.c_void_p) -> c.c_uint8:
		return self.lib.getNZCV(guest)



__all__ = ["SELib"]