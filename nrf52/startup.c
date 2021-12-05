#include <stddef.h>
#include <stdint.h>

#include "startup.h"
#include "run.h"

NVIC_Table isr_vectors = {
    //.StackTop = (void *)(1024 * 16 + 0x20000000),
    .StackTop = __stack,
    .Reset_Handler = reset_handler,
    .NMI_Handler = irq_trap,
    .HardFault_Handler = irq_trap,
    .MemManage_Handler = irq_trap,
    .BusFault_Handler = irq_trap,
    .UsageFault_Handler = irq_trap,
    .SVC_Handler = irq_trap,
    .DebugMon_Handler = irq_trap,
    .PendSV_Handler = irq_trap,
    .SysTick_Handler = irq_trap,
    /* External Interrupts */
    .POWER_CLOCK_IRQHandler = irq_trap,
    .RADIO_IRQHandler = _RADIO_IRQHandler,
    .UARTE0_UART0_IRQHandler = irq_trap,
    .TIMER0_IRQHandler = _TIMER0_IRQHandler,
    .RNG_IRQHandler = _RNG_IRQHandler,
    /* More IRQHandlers below
    .SERIAL0_IRQHandler
    .SERIAL1_IRQHandler
    .NFCT_IRQHandler
    .GPIOTE_IRQHandler
    .SAADC_IRQHandler
    .TIMER1_IRQHandler
    .TIMER2_IRQHandler
    .RTC0_IRQHandler
    .TEMP_IRQHandler
    .RNG_IRQHandler
    .ECB_IRQHandler
    .CCM_AAR_IRQHandler
    .WDT_IRQHandler
    .RTC1_IRQHandler
    .QDEC_IRQHandler
    .COMP_LPCOMP_IRQHandler
    .SWI0_EGU0_IRQHandler
    .SWI1_EGU1_IRQHandler
    .SWI2_EGU2_IRQHandler
    .SWI3_EGU3_IRQHandler
    .SWI4_EGU4_IRQHandler
    .SWI5_EGU5_IRQHandler
    .TIMER3_IRQHandler
    .TIMER4_IRQHandler
    .PWM0_IRQHandler
    .PDM_IRQHandler
    .MWU_IRQHandler
    .PWM1_IRQHandler
    .PWM2_IRQHandler
    .SERIAL2_IRQHandler
    .RTC2_IRQHandler
    .I2S_IRQHandler
    .FPU_IRQHandler
    .USBD_IRQHandler
    .UARTE1_IRQHandler
    .PWM3_IRQHandler
    .SPIM3_IRQHandler
    */
};



void reset_handler(void) {
    uint32_t *to = __data_start;
    uint32_t *from = __text_end;

    while (to < __data_end) {
        *to++ = *from++;
    }

    to = __bss_start;
    while (to < __bss_end) {
        *to++ = 0;
    }

    /* Enter the main program */
    run();

    /* Reset_Handler shouldn't ever return, hang */
    while(1) {
    }
}

void _default_irq_trap() {
    while (1);
}
