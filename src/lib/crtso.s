; This is the C run-time start-off routine.  It's job is to take the
; arguments as put on the stack by EXEC, and to parse them and set them up the
; way _main expects them.

.globl _main, _exit, crtso, _environ, ___mkargv
.globl begtext, begdata, begbss, endtext, enddata, endbss
entry crtso     ; force ld86 to include crtso label

; Note: BCC Tells the linker to init argv by adding a global reference to its
; ___mkargv label in main. This label will never be used when using MINIX
; crtso.o, but we need to define the label to keep the linker happy.
.text
___mkargv:  ; ___mkargv will never be called
begtext:
crtso:		mov	bx,sp
		mov	cx,(bx)
		add	bx,*2
		mov	ax,cx
		inc	ax
		shl	ax,#1
		add	ax,bx
		mov	_environ,ax	; save envp in environ
		push	ax	; push environ
		push	bx	; push argv
		push	cx	; push argc
		call	_main
		add	sp,*6
		push	ax	; push exit status
		call	_exit

.data
begdata:
_environ:	.word 0
.bss
begbss:
