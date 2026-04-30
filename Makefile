.PHONY: all
all:
	echo TODO

.PHONY: dev86
dev86:
	$(MAKE) -C ./vendor/dev86

.PHONY: libc
libc:
	mkdir -p ./lib
	$(MAKE) -C ./src/lib
	cp ./src/lib/libc.a ./lib
	cp ./src/lib/crtso.o ./lib
	cp ./src/lib/end.o ./lib

.PHONY: clean
clean:
	$(MAKE) -C ./src/lib clean
	rm -f ./lib/libc.a ./lib/crtso.o ./lib/end.o
