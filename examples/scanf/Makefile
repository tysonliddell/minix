DEV86_BIN=../../vendor/bcc/bin
CC=$(DEV86_BIN)/bcc
AS=$(DEV86_BIN)/as86
LD=$(DEV86_BIN)/ld86
AR=$(DEV86_BIN)/ar86

OUT=scanf

CFLAGS=-0 -Di8088 -I../src/include

# use -a flag for MINIX asld compatibility
ASFLAGS=-0 -a

#LD_DEBUG_FLAGS=-m -M -t

# Set default memory allocated to program to max value possible, as the
# compiler on MINIX does. Can later be adjusted with chmem command in MINIX 
MEM_ALLOC = 0xFFFF

$(OUT): main.o
	# crtso needs to reside at address 0 of the text segment for MINIX to be
	# happy, since MINIX does not use the entry point address in the executable
	# header (the 6th long in the header). This means that -Cso needs to be
	# specified before any other files (-lc, xxx.o, end.o, etc.) to make this
	# happen.
	$(LD) $(LD_DEBUG_FLAGS) -0 -s -L../../lib -Cso -lc main.o -Oend.o -o $(OUT) -H $(MEM_ALLOC)

clean:
	rm -f *.o
	rm -f $(OUT)
