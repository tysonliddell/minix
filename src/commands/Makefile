DEV86_BIN=../../vendor/bcc/bin
CC=$(DEV86_BIN)/bcc
AS=$(DEV86_BIN)/as86
LD=$(DEV86_BIN)/ld86
ASFLAGS=-0 -a
CFLAGS=-0 -Di8088 -I../include -O

l=../../lib
MEM_ALLOC_FILE = ./STACK_SIZES
DEFAULT_STACK_SIZE = 2048
PROGS = ar basename cat cc chmem chmod chown clr cmp comm cp date dd df \
    dosread echo getlf grep gres head kill libpack libupack ln lpr ls make \
    mkdir mkfs mknod mount mv od passwd pr pwd rev rm rmdir roff \
    shar size sleep sort split stty su sum sync tail tar tee time touch tr \
    umount uniq update wc
BIG_PROGS = mined sh
CHMEM_64 = chmem-64

try_get_stack_size = $(shell awk '/^$(1) / {print $$2}' $(MEM_ALLOC_FILE))
get_stack_size = $(or $(call try_get_stack_size,$(1)), $(DEFAULT_STACK_SIZE))

.PHONY: all $(PROGS) $(BIG_PROGS) clean

# To make 'cp':         make cp
# To make 'ls':         make ls
# To make 'cat':        make cat
# etc.
# To make everything:   make

all: $(PROGS) $(BIG_PROGS)

# "static pattern rule" for GNU make
$(PROGS) $(BIG_PROGS): %: bin/% ;

$(addprefix bin/,$(PROGS)): bin/%: %.o $l/libc.a $(MEM_ALLOC_FILE) $(CHMEM_64)
	@mkdir -p bin
	$(LD) -0 -s -o $@ -L../../lib -Cso $< -lc -Oend.o
	./$(CHMEM_64) =$(call get_stack_size,$*) $@
	@echo "$@ done."

bin/mined:	mined1.o mined2.o mined.h $l/libc.a $(MEM_ALLOC_FILE) $(CHMEM_64)
	@mkdir -p bin
	$(LD) -0 -s -o bin/mined -L../../lib -Cso mined1.o mined2.o -lc -Oend.o
	./$(CHMEM_64) =$(call get_stack_size,mined) $@
	@echo "$@ done."

shobj = sh1.o sh2.o sh3.o sh4.o sh5.o
bin/sh:	$(shobj) sh.h $l/libc.a $(MEM_ALLOC_FILE) $(CHMEM_64)
	@mkdir -p bin
	$(LD) -0 -s -o bin/sh -L../../lib -Cso $(shobj) -lc -Oend.o
	./$(CHMEM_64) =$(call get_stack_size,sh) $@
	@echo "$@ done."

# Configure MINIX cc for a 640K machine. MEM512K is also available.
cc.o: cc.c
	$(CC) $(CFLAGS) -DMEM640K -c -o $@ $<

# a quick and dirty port of chmem to run on the 64-bit host.
$(CHMEM_64): chmem-64.c
	gcc $< -std=gnu89 -o $@

clean:
	rm -f *.o
	rm -f $(addprefix bin/,$(PROGS)) $(addprefix bin/,$(BIG_PROGS))
	rm -f $(CHMEM_64)
	rm -df bin
