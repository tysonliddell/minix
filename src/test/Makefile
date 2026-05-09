DEV86_BIN=../../vendor/bcc/bin
CC=$(DEV86_BIN)/bcc
LD=$(DEV86_BIN)/ld86
CFLAGS=-0 -Di8088 -I -I../include -O

l=../../lib
BLANK_DISK_IMG = ../../disks/360k-minix-formatted.img
TEST_DISK_IMG = ./test-disk.img
TEST_DISK_MNT = ./mnt
TEST_SRC = $(wildcard test*.c)
TEST_OBJ = $(TEST_SRC:.c=.o)
TEST_BIN = $(addprefix bin/,$(TEST_SRC:.c=))
CHMEM_64 = ./chmem-64
STACK_SIZE = 8000

.PHONY: tests test-disk clean

tests: $(TEST_BIN)

#$(TEST_BIN): bin/%: %.o $l/libc.a $(CHMEM_64)
bin/%: %.o $l/libc.a $(CHMEM_64)
	mkdir -p bin
	$(LD) -0 -s -o $@ -L../../lib -Cso $< -lc
	$(CHMEM_64) =$(STACK_SIZE) $@

bin/test10: bin/t10a
bin/test11: bin/t11a bin/t11b

test-disk: tests
	cp $(BLANK_DISK_IMG) $(TEST_DISK_IMG)
	mkdir $(TEST_DISK_MNT)
	sudo mount -t minix $(TEST_DISK_IMG) $(TEST_DISK_MNT)
	sudo cp run bin/* $(TEST_DISK_MNT)
	sudo umount $(TEST_DISK_MNT)
	rmdir $(TEST_DISK_MNT)

# a quick and dirty port of chmem to run on the 64-bit host.
$(CHMEM_64): chmem-64.c
	gcc $< -std=gnu89 -o $@

clean:
	rm -rf ./bin
	rm -f $(CHMEM_64)
	rm -f $(TEST_DISK_IMG)
