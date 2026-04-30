.PHONY: all
all: dev86 libc

.PHONY: dev86
dev86:
	$(MAKE) -C ./vendor/dev86

.PHONY: libc
libc:
	$(MAKE) -C ./src/lib
	cp ./src/lib/libc.a ./lib
	cp ./src/lib/crtso.o ./lib
	cp ./src/lib/end.o ./lib

.PHONY: clean
clean:
	$(MAKE) -C ./src/lib clean
	rm ./lib/libc.a ./lib/crtso.o ./lib/end.o
