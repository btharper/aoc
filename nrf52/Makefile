PREFIX = arm-none-eabi-
CC = $(PREFIX)gcc
AR = $(PREFIX)ar
LD = $(PREFIX)ld
OBJCOPY = $(PREFIX)objcopy

COPY = cp
INSTALL_DIR = /mnt/chromeos/removable/MICROBIT/

V1 = build-v1
V2 = build-v2

CFLAGS += -Wall -pedantic -nostartfiles -nostdlib -ffreestanding -ggdb3
#CFLAGS += -flto -Os -ffunction-sections -fdata-sections
CFLAGS += -Iinclude
#LDFLAGS += -Wl,--relax,--gc-sections
# thumb/v7e-m/fpv4-sp/hard;@mthumb@march=armv7e-m@mfpu=fpv4-sp-d16@mfloat-abi=hard
V2_CFLAGS = -mcpu=cortex-m4 -mthumb -march=armv7e-m -mfpu=fpv4-sp-d16 -mfloat-abi=hard
#LDFLAGS += -T advent.ld

.PHONY: all clean buildv2 ptx_ex prx_ex install_ptx_ex install_prx_ex
all: buildv2 ptx_ex prx_ex

buildv2: $(V2)/ $(V2)/advent.hex $(V2)/advent.bin

ptx_ex: $(V2)/ $(V2)/hello_ptx.hex $(V2)/hello_ptx.bin

prx_ex: $(V2)/ $(V2)/hello_prx.hex $(V2)/hello_prx.bin

install_ptx_ex: $(V2)/ $(V2)/hello_ptx.hex
	$(COPY) build-v2/hello_ptx.hex $(INSTALL_DIR)

install_prx_ex: $(V2)/ $(V2)/hello_prx.hex
	$(COPY) build-v2/hello_prx.hex $(INSTALL_DIR)

$(V2)/%.hex: $(V2)/%.elf
	$(OBJCOPY) -O ihex $< $@

$(V2)/%.bin: $(V2)/%.elf
	$(OBJCOPY) -O binary $< $@

$(V2)/advent.elf: advent.ld $(V2)/startup.o $(V2)/run.o
	$(CC) -o $@ -T $^ $(CFLAGS) $(V2_CFLAGS) $(LDFLAGS)

$(V2)/hello_ptx.elf: advent.ld $(V2)/startup.o $(V2)/hello_radio.o
	$(CC) -o $@ -T $^ $(CFLAGS) $(V2_CFLAGS) $(LDFLAGS)

$(V2)/hello_prx.elf: advent.ld $(V2)/startup.o $(V2)/hello_prx.o
	$(CC) -o $@ -T $^ $(CFLAGS) $(V2_CFLAGS) $(LDFLAGS)


# Use longest stem rule to capture header dependencies with the same name
$(V2)/%.o: %.c %.h
	$(CC) -o $@ -c $< $(CFLAGS) $(V2_CFLAGS) $(CPPFLAGS)

$(V2)/%.o: %.c
	$(CC) -o $@ -c $^ $(CFLAGS) $(V2_CFLAGS) $(CPPFLAGS)

$(V2)/:
	mkdir $(V2)

clean:
	-@ $(RM) $(V2)/*.o $(V2)/*.hex $(V2)/*.elf $(V2)/*.bin $(V2)/*.map
