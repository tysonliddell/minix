.text
xor     ax,ax

.data
.zerow 10

.bss
; using .zerow in the bss section causes as86 to add zeroes to the data section
; which is not what we want. The BSS should contain uninitialised data and
; should live outside of the data segment.
stack1:
.zerow 1000

; Using a .comm declaration results in the data residing in the bss.
.comm stack2,1000*2
