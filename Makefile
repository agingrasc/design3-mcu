flash:
	st-flash write cmake-build-debug/design3-mcu.bin 0x8000000

debug:
	st-util &
