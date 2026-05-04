DEV86_BIN=../../vendor/bcc/bin
CC=$(DEV86_BIN)/bcc
AS=$(DEV86_BIN)/as86
LD=$(DEV86_BIN)/ld86
ASFLAGS=-0 -a
CFLAGS=-0 -Di8088 -I../include -O

.PHONY: all
all: bss.lst bss.o

bss.lst: bss.s
	$(AS) $(ASFLAGS) -m -l $@ $<

bss.o: bss.s
	$(AS) $(ASFLAGS) -o $@ $<

.PHONY: clean
clean:
	rm -f bss.lst bss.o
