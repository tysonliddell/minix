AS=../../vendor/bcc/bin/as86
ASFLAGS=-0 -a

mov.lst: mov.s
	$(AS) $(ASFLAGS) -m -l $@ $<

.PHONY: clean
clean:
	rm -f mov.lst
