.arch armv8-a
.text
.align	2
.p2align 3,,7
start:
	// Simple tests for ldur and stur.
	sub sp, sp, #32
	movz x0, #31
	movz x1, #41
	movz x2, #59
	movz x3, #26
	stur x0, [sp]
	stur x1, [sp, #8]
	stur x2, [sp, #16]
	stur x3, [sp, #24]
	ldur x4, [sp]       // 31
	ldur x5, [sp, #8]   // 41
	ldur x6, [sp, #16]  // 59
	ldur x7, [sp, #24]  // 26
	add sp, sp, #32
	ret
	.size	start, .-start
.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
.section	.note.GNU-stack,"",@progbits