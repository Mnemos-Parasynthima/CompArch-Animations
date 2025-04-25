start:
	sub sp, sp, #32
	movz x0, #31
	movz x1, #41
	movz x2, #59
	movz x3, #26
	stur x0, [sp]
	stur x1, [sp, #8]
	stur x2, [sp, #16]
	stur x3, [sp, #24]
	ldur x4, [sp]
	ldur x5, [sp, #8]
	ldur x6, [sp, #16]
	ldur x7, [sp, #24]
	add sp, sp, #32
	ret