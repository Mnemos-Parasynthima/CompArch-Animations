import ctypes as c

class Tuple(c.Structure): 
	_fields_ = [("src2sel", c.c_bool), ("src2_1", c.c_uint8), ("src2_2", c.c_uint8), ("src2", c.c_uint8)]

class SELib:
	def __init__(self, lib:str, api:str):
		self.lib = c.CDLL(lib)
		self.api = c.CDLL(api)

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
		self.api.getBranchOffset.argtypes = [c.c_void_p, c.c_void_p]
		self.api.getBranchOffset.restype = c.c_uint64

		self.api.getImmval.argtypes = [c.c_void_p]
		self.api.getImmval.restype = c.c_int64

		self.api.getDecodeDstSel.argtypes = [c.c_void_p]
		self.api.getDecodeDstSel.restype = c.c_bool

		self.api.getDecodeDst.argtypes = [c.c_void_p]
		self.api.getDecodeDst.restype = c.c_uint8

		self.api.getDecodeSrc1.argtypes = [c.c_void_p]
		self.api.getDecodeSrc1.restype = c.c_uint8

		self.api.getDecodeSrc2Data.argtypes = [c.c_void_p]
		self.api.getDecodeSrc2Data.restype = Tuple

		self.api.getDecodeSrc2Sel.argtypes = [Tuple]
		self.api.getDecodeSrc2Sel.restype = c.c_bool

		self.api.getDecodeSrc2_1.argtypes = [Tuple]
		self.api.getDecodeSrc2_1.restype = c.c_uint8

		self.api.getDecodeSrc2_2.argtypes = [Tuple]
		self.api.getDecodeSrc2_2.restype = c.c_uint8

		self.api.getDecodeSrc2.argtypes = [Tuple]
		self.api.getDecodeSrc2.restype = c.c_uint8

		self.api.getValA.argtypes = [c.c_void_p]
		self.api.getValA.restype = c.c_uint64

		self.api.getValB.argtypes = [c.c_void_p]
		self.api.getValB.restype = c.c_uint64

		self.api.getValBSel.argtypes = [c.c_void_p]
		self.api.getValBSel.restype = c.c_bool

		self.api.getValEx.argtypes = [c.c_void_p]
		self.api.getValEx.restype = c.c_uint64

		self.api.getValHw.argtypes = [c.c_void_p]
		self.api.getValHw.restype = c.c_uint8

		self.api.getAluOp.argtypes = [c.c_void_p]
		self.api.getAluOp.restype = c.c_int

		self.api.getSetCC.argtypes = [c.c_void_p]
		self.api.getSetCC.restype = c.c_bool

		self.api.getCond.argtypes = [c.c_void_p]
		self.api.getCond.restype = c.c_int

		self.api.getCondVal.argtypes = [c.c_void_p]
		self.api.getCondVal.restype = c.c_bool

		self.api.getMemRead.argtypes = [c.c_void_p]
		self.api.getMemRead.restype = c.c_bool

		self.api.getMemWrite.argtypes = [c.c_void_p]
		self.api.getMemWrite.restype = c.c_bool

		self.api.getRVal.argtypes = [c.c_void_p]
		self.api.getRVal.restype = c.c_uint64

		self.api.getWvalSel.argtypes = [c.c_void_p]
		self.api.getWvalSel.restype = c.c_bool

		self.api.getWriteDstSel.argtypes = [c.c_void_p]
		self.api.getWriteDstSel.restype = c.c_bool

		self.api.getWEnable.argtypes = [c.c_void_p]
		self.api.getWEnable.restype = c.c_bool

		self.api.getNextPC.argtypes = [c.c_void_p]
		self.api.getNextPC.restype = c.c_uint64

		self.api.getProcStatus.argtypes = [c.c_void_p]
		self.api.getProcStatus.restype = c.c_int


		self.api.getRegisters.argtypes = [c.c_void_p]
		self.api.getRegisters.restype = c.POINTER(c.c_uint64*31)
		self.api.getSP.argtypes = [c.c_void_p]
		self.api.getSP.restype = c.c_uint64
		self.api.getPC.argtypes = [c.c_void_p]
		self.api.getPC.restype = c.c_uint64
		self.api.getNZCV.argtypes = [c.c_void_p]
		self.api.getNZCV.restype = c.c_uint8



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
		return self.api.getBranchOffset(guest, _globals)
	
	def getImmval(self, guest:c.c_void_p) -> c.c_int64:
		return self.api.getImmval(guest)
	
	def getDecodeDstSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getDecodeDstSel(guest)
	
	def getDecodeDst(self, guest:c.c_void_p) ->c.c_uint8:
		return self.api.getDecodeDst(guest)

	def getDecodeSrc1(self, guest:c.c_void_p) ->c.c_uint8:
		return self.api.getDecodeSrc1(guest)

	def getDecodeSrc2Data(self, guest:c.c_void_p) -> "Tuple":
		return self.api.getDecodeSrc2Data(guest)
	
	def getDecodeSrc2Sel(self, _tuple:"Tuple") -> c.c_bool:
		return self.api.getDecodeSrc2Sel(_tuple)
	
	def getDecodeSrc2_1(self, _tuple:"Tuple") -> c.c_uint8:
		return self.api.getDecodeSrc2_1(_tuple)
	
	def getDecodeSrc2_2(self, _tuple:"Tuple") -> c.c_uint8:
		return self.api.getDecodeSrc2_2(_tuple)
	
	def getDecodeSrc2(self, _tuple:"Tuple") -> c.c_uint8:
		return self.api.getDecodeSrc2(_tuple)
	
	def getValA(self, guest:c.c_void_p) -> c.c_uint64:
		return self.api.getValA(guest)

	def getValB(self, guest:c.c_void_p) -> c.c_uint64:
		return self.api.getValB(guest)
	
	def getValBSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getValBSel(guest)
	
	def getValEx(self, guest:c.c_void_p) -> c.c_uint64:
		return self.api.getValEx(guest)
	
	def getValHw(self, guest:c.c_void_p) -> c.c_uint8:
		return self.api.getValHw(guest)

	def getAluOp(self, guest:c.c_void_p) -> c.c_int:
		return self.api.getAluOp(guest)
	
	def getSetCC(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getSetCC(guest)
	
	def getCond(self, guest:c.c_void_p) -> c.c_int:
		return self.api.getCond(guest)
	
	def getCondVal(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getCondVal(guest)

	def getMemRead(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getMemRead(guest)

	def getMemWrite(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getMemWrite(guest)

	def getRVal(self, guest:c.c_void_p) -> c.c_uint64:
		return self.api.getRVal(guest)
	
	def getWvalSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getWvalSel(guest)

	def getWriteDstSel(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getWriteDstSel(guest)

	def getWEnable(self, guest:c.c_void_p) -> c.c_bool:
		return self.api.getWEnable(guest)

	def getNextPC(self, guest:c.c_void_p) -> c.c_uint64:
		return self.api.getNextPC(guest)

	def getProcStatus(self, guest:c.c_void_p) -> c.c_int:
		return self.api.getProcStatus(guest)


	def getRegisters(self, guest:c.c_void_p) -> c._Pointer:
		return self.api.getRegisters(guest)
	
	def getSP(self, guest:c.c_void_p) -> c.c_uint64:
		return self.api.getSP(guest)
	
	def getPC(self, guest:c.c_void_p) -> c.c_uint64:
		return self.api.getPC(guest)
	
	def getNZCV(self, guest:c.c_void_p) -> c.c_uint8:
		return self.api.getNZCV(guest)



__all__ = ["SELib"]