CC=../../vendor/dev86/bin/bcc
AS=../../vendor/dev86/bin/as86
LD=../../vendor/dev86/bin/ld86
AR=../../vendor/dev86/bin/ar86

CFLAGS=-0 -Di8088 -I../include -O

# use -a flag for MINIX asld compatibility
ASFLAGS=-0 -a

LIB_C_SRC=$(wildcard *.c)
LIB_S_SRC=brksize.s  catchsig.s  getutil.s  sendrec.s  setjmp.s
LIB_C_OBJ=$(LIB_C_SRC:.c=.o)
LIB_S_OBJ=$(LIB_S_SRC:.s=.o)
LIBC=libc.a

CRTSO_OBJ=crtso.o
END_OBJ=end.o

.PHONY: all
all: libc c_runtime

.PHONY: libc
libc: $(LIBC)

$(LIBC): $(LIB_C_OBJ) $(LIB_S_OBJ)
	rm -f $(LIBC)
	$(AR) r $(LIBC) $^
	$(MAKE) -C ./bcc
	$(AR) r $(LIBC) ./bcc/*.o

.PHONY: c_runtime
c_runtime: $(CRTSO_OBJ) $(END_OBJ)

.PHONY: clean
clean:
	$(MAKE) -C ./bcc clean
	rm -f *.o
	rm -f libc.a
