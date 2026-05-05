DEV86_BIN=../../vendor/bcc/bin
CC=$(DEV86_BIN)/bcc
AS=$(DEV86_BIN)/as86
LD=$(DEV86_BIN)/ld86
ASFLAGS=-0 -a
CFLAGS=-0 -Di8088 -I../include -O

h=../h
l=../../lib

obj =	main.o forkexit.o break.o exec.o signal.o getset.o  \
	alloc.o utility.o table.o putc.o 

mm:	Makefile  $l/head.o $(obj) $l/libc.a
	@echo "Start linking MM"
	$(LD) -0 -s -o mm -L../../lib -Ohead.o $(obj) -lc
	@echo "MM done"


alloc.o:	const.h $h/const.h $h/type.h

break.o:	const.h $h/const.h $h/type.h
break.o:	$h/error.h
break.o:	$h/signal.h
break.o:	glo.h
break.o:	mproc.h
break.o:	param.h

exec.o:		const.h $h/const.h $h/type.h
exec.o:		$h/callnr.h
exec.o:		$h/error.h
exec.o:		$h/stat.h
exec.o:		glo.h
exec.o:		mproc.h
exec.o:		param.h

forkexit.o:	const.h $h/const.h $h/type.h
forkexit.o:	$h/callnr.h
forkexit.o:	$h/error.h
forkexit.o:	glo.h
forkexit.o:	mproc.h
forkexit.o:	param.h

getset.o:	const.h $h/const.h $h/type.h
getset.o:	$h/callnr.h
getset.o:	$h/error.h
getset.o:	glo.h
getset.o:	mproc.h
getset.o:	param.h

main.o:		const.h $h/const.h $h/type.h
main.o:		$h/callnr.h
main.o:		$h/com.h
main.o:		$h/error.h
main.o:		glo.h
main.o:		mproc.h
main.o:		param.h

putc.o:		$h/const.h $h/type.h
putc.o:		$h/com.h

signal.o:	const.h $h/const.h $h/type.h
signal.o:	$h/callnr.h
signal.o:	$h/com.h
signal.o:	$h/error.h
signal.o:	$h/signal.h
signal.o:	$h/stat.h
signal.o:	glo.h
signal.o:	mproc.h
signal.o:	param.h

table.o:	const.h $h/const.h $h/type.h
table.o:	$h/callnr.h
table.o:	glo.h
table.o:	mproc.h
table.o:	param.h

utility.o:	const.h $h/const.h $h/type.h
utility.o:	$h/callnr.h
utility.o:	$h/com.h
utility.o:	$h/error.h
utility.o:	$h/stat.h
utility.o:	glo.h
utility.o:	mproc.h

.PHONY: clean
clean:
	rm -f *.o
	rm -f mm
