CC=/opt/pkg/ack/bin/ack
#CFLAGS=-mpc86 -Di8088 -I./include -w
CFLAGS=-mpc86 -Di8088 -I./src/include -w

LIB_C_SRC=$(wildcard ./src/lib/*.c)
LIB_S_SRC=$(wildcard ./src/lib/*.s)
LIB_C_OBJ=$(LIB_C_SRC:.c=.o)
LIB_S_OBJ=$(LIB_S_SRC:.s=.o)

all:
	@echo TODO

.PHONY: libc
libc: $(LIB_C_OBJ)

.PHONY: clean
clean:
	rm ./src/lib/*.o
