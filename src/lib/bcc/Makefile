# Copyright (C) 1995,1996 Robert de Bath <rdebath@cix.compulink.co.uk>
# This file is part of the Linux-8086 C library and is distributed
# under the GNU Library General Public License.

# Support for integer arithmetic
IOBJ=__idiv.o __idivu.o __imod.o __imodu.o __imul.o __isl.o __isr.o __isru.o
ISRC=bcc_int.c

# Support for long arithmetic on little-endian (normal) longs
LSRC=bcc_long.c
LOBJ=__laddl.o __landl.o __lcmpl.o __lcoml.o __ldecl.o __ldivl.o __ldivul.o \
     __leorl.o __lincl.o __lmodl.o __lmodul.o __lmull.o __lnegl.o __lorl.o \
     __lsll.o __lsrl.o __lsrul.o __lsubl.o __ltstl.o

SSRC=string.c
SOBJ=memcpy.o

DEV86_PATH=../../../vendor/dev86
CC=$(DEV86_PATH)/bin/bcc
CFLAGS=-0 -O

.PHONY: all
all: $(IOBJ) $(LOBJ) $(SOBJ) ldiv.o __ldivmod.o

$(IOBJ): $(ISRC)
	$(CC) $(CFLAGS) -DL_$* $< -c -o $*.o

$(LOBJ): $(LSRC)
	$(CC) $(CFLAGS) -DL_$* $< -c -o $*.o

$(SOBJ): $(SSRC)
	$(CC) $(CFLAGS) -DL_$* $< -c -o $*.o

.PHONY: clean
clean:
	rm -f *.o
