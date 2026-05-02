LIB_SRC_DIR = ./src/lib
LIB_DIR = ./lib
LIB_FILES = $(addprefix $(LIB_DIR)/,libc.a crtso.o head.o end.o)
BUILD_BOOTDISK = ./scripts/build-boot-disk.py
BOOTDISK_OUT = ./MINIX-boot.img
DISK_REQS = ./src/tools/bootblok ./src/kernel/kernel ./src/mm/mm ./src/fs/fs \
    ./src/tools/init ./src/tools/fsck

.PHONY: all minix dev86 bootblok kernel mm fs init fsck tools disk libc libc_build clean

all: minix
minix: libc bootblok kernel mm fs init fsck

dev86:
	$(MAKE) -C ./vendor/dev86
	$(MAKE) -C ./vendor/dev86 install

kernel:
	$(MAKE) -C ./src/kernel

mm:
	$(MAKE) -C ./src/mm

fs:
	$(MAKE) -C ./src/fs

bootblok: tools
init: tools
fsck: tools

tools:
	$(MAKE) -C ./src/tools

disk: minix $(BOOTDISK_OUT)

$(BOOTDISK_OUT): $(DISK_REQS)
	@echo TODO: add bookblok to build
	python3 $(BUILD_BOOTDISK) $(DISK_REQS) $(BOOTDISK_OUT)

libc: $(LIB_FILES)

$(LIB_DIR)/libc.a: $(LIB_SRC_DIR)/libc.a
$(LIB_DIR)/crtso.o: $(LIB_SRC_DIR)/crtso.o
$(LIB_DIR)/end.o: $(LIB_SRC_DIR)/end.o
$(LIB_DIR)/head.o: $(LIB_SRC_DIR)/head.o

$(LIB_DIR)/%: | libc_build
	cp $< $@

libc_build:
	mkdir -p $(LIB_DIR)
	$(MAKE) -C $(LIB_SRC_DIR)

clean:
	$(MAKE) -C ./src/tools clean
	$(MAKE) -C ./src/fs clean
	$(MAKE) -C ./src/mm clean
	$(MAKE) -C ./src/kernel clean
	$(MAKE) -C ./src/lib clean
	rm -f $(LIB_FILES)
	rm -rf $(LIB_DIR)
