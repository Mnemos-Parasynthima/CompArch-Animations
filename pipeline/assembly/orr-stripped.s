start:
	movz x0, #0xff00
	movz x1, #0x0ff0, lsl 16
	movz x2, #0x00ff, lsl 32
	movz x3, #0xf00f, lsl 48
	nop
	orr x4, x0, x1
	orr x5, x1, x2
	orr x6, x2, x3
	orr x7, x3, x0
	ret