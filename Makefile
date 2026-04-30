LIB_SRC_DIR = ./src/lib
LIB_DIR = ./lib
LIB_FILES = $(addprefix $(LIB_DIR)/,libc.a crtso.o head.o end.o)

.PHONY: all
all: libc kernel mm fs

.PHONY: dev86
dev86:
	$(MAKE) -C ./vendor/dev86

.PHONY: kernel
kernel:
	$(MAKE) -C ./src/kernel

.PHONY: mm
mm:
	$(MAKE) -C ./src/mm

.PHONY: fs
fs:
	$(MAKE) -C ./src/fs

.PHONY: libc
libc: $(LIB_FILES)

$(LIB_DIR)/libc.a: $(LIB_SRC_DIR)/libc.a
$(LIB_DIR)/crtso.o: $(LIB_SRC_DIR)/crtso.o
$(LIB_DIR)/end.o: $(LIB_SRC_DIR)/end.o
$(LIB_DIR)/head.o: $(LIB_SRC_DIR)/head.o

$(LIB_DIR)/%: | libc_build
	cp $< $@

.PHONY: libc_build
libc_build:
	mkdir -p $(LIB_DIR)
	$(MAKE) -C $(LIB_SRC_DIR)

.PHONY: clean
clean:
	$(MAKE) -C ./src/fs clean
	$(MAKE) -C ./src/mm clean
	$(MAKE) -C ./src/kernel clean
	$(MAKE) -C ./src/lib clean
	rm -f $(LIB_FILES)
	rm -rf $(LIB_DIR)
