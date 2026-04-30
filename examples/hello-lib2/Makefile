CC=../../vendor/dev86/bin/bcc
AS=../../vendor/dev86/bin/as86
LD=../../vendor/dev86/bin/ld86
AR=../../vendor/dev86/bin/ar86

CFLAGS=-0 -Di8088

# use -a flag for MINIX asld compatibility
ASFLAGS=-0 -a

# Set default memory allocated to program to max value possible, as the
# compiler on MINIX does. Can later be adjusted with chmem command in MINIX 
MEM_ALLOC = 0xFFFF

hello: main.o
	# crtso needs to reside at address 0 of the text segment for MINIX to be
	# happy, since MINIX does not use the entry point address in the executable
	# header (the 6th long in the header). This means that -Cso needs to be
	# specified before any other files (-lc, xxx.o, end.o, etc.) to make this
	# happen.
	$(LD) $(LD_DEBUG_FLAGS) -0 -s -L../../lib -Cso -lc main.o -Oend.o -o hello -H $(MEM_ALLOC)

clean:
	rm -f *.o
	rm -f hello
