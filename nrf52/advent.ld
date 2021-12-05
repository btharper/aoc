MEMORY
{
    FLASH (rx) : ORIGIN = 0x00000000, LENGTH = 512K
    RAM (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

ENTRY(reset_handler)

SECTIONS
{
    __stack = ORIGIN(RAM) + LENGTH(RAM);

    .isr_vectors 0x00000000 :
    {
        KEEP(*(.isr_vectors*))
        ASSERT(. == ALIGN(4), "Error: isr_vectors must be word aligned values");
        ASSERT(. > 4, "Error: Must have non-zero lenth isr_vectors section");
    }

    .text ADDR(.isr_vectors) + SIZEOF(.isr_vectors) :
    {
        . = ALIGN(4);
        *(.text*)
        *(.rodata*)
        . = ALIGN(4);
        __text_end = .;
    } > FLASH

    .data : AT (__text_end)
    {
        . = ALIGN(4);
        __data_start = .;
        *(.data*)
        *(COMMON)
        . = ALIGN(4);
        __data_end = .;
    } > RAM

    .bss :
    {
        . = ALIGN(4);
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end = .;
    } > RAM

}
