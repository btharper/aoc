extern uint32_t __data_start[];
extern uint32_t __data_end[];
extern uint32_t __text_end[];
extern uint32_t __bss_start[], __bss_end[];
extern uint32_t __stack[];

void reset_handler(void) __attribute__((noreturn));
void _default_irq_trap(void) __attribute__((interrupt));
void irq_trap(void) __attribute__((interrupt, weak, alias ("_default_irq_trap")));
void _RADIO_IRQHandler(void) __attribute__((interrupt, weak, alias ("irq_trap")));
void _RNG_IRQHandler(void) __attribute__((interrupt, weak, alias ("irq_trap")));
void _TIMER0_IRQHandler(void) __attribute__((interrupt, weak, alias ("irq_trap")));

typedef void (*IRQ_Handler)(void);

typedef struct {
    /* Arm Cortex-M fields */
    void *StackTop;                     /*  0 */
    IRQ_Handler Reset_Handler;
    IRQ_Handler NMI_Handler;
    IRQ_Handler HardFault_Handler;
    IRQ_Handler MemManage_Handler;      /*  4 */
    IRQ_Handler BusFault_Handler;
    IRQ_Handler UsageFault_Handler;
    IRQ_Handler Reserved_7;
    IRQ_Handler Reserved_8;             /*  8 */
    IRQ_Handler Reserved_9;
    IRQ_Handler Reserved_10;
    IRQ_Handler SVC_Handler;
    IRQ_Handler DebugMon_Handler;       /* 12 */
    IRQ_Handler Reserved_13;
    IRQ_Handler PendSV_Handler;
    IRQ_Handler SysTick_Handler;        /* 15 */

    /* Implementaiton specific interrupts */
    /* The nrf52 series has at most 48 such vectors */
    IRQ_Handler POWER_CLOCK_IRQHandler; /* 16 */
    IRQ_Handler RADIO_IRQHandler;
    IRQ_Handler UARTE0_UART0_IRQHandler;
    IRQ_Handler SERIAL0_IRQHandler;
    IRQ_Handler SERIAL1_IRQHandler;
    IRQ_Handler NFCT_IRQHandler;
    IRQ_Handler GPIOTE_IRQHandler;
    IRQ_Handler SAADC_IRQHandler;
    IRQ_Handler TIMER0_IRQHandler;      /* 24 */
    IRQ_Handler TIMER1_IRQHandler;
    IRQ_Handler TIMER2_IRQHandler;
    IRQ_Handler RTC0_IRQHandler;
    IRQ_Handler TEMP_IRQHandler;
    IRQ_Handler RNG_IRQHandler;
    IRQ_Handler ECB_IRQHandler;
    IRQ_Handler CCM_AAR_IRQHandler;
    IRQ_Handler WDT_IRQHandler;         /* 32 */
    IRQ_Handler RTC1_IRQHandler;
    IRQ_Handler QDEC_IRQHandler;
    IRQ_Handler COMP_LPCOMP_IRQHandler;
    IRQ_Handler SWI0_EGU0_IRQHandler;
    IRQ_Handler SWI1_EGU1_IRQHandler;
    IRQ_Handler SWI2_EGU2_IRQHandler;
    IRQ_Handler SWI3_EGU3_IRQHandler;
    IRQ_Handler SWI4_EGU4_IRQHandler;   /* 40 */
    IRQ_Handler SWI5_EGU5_IRQHandler;
    IRQ_Handler TIMER3_IRQHandler;
    IRQ_Handler TIMER4_IRQHandler;
    IRQ_Handler PWM0_IRQHandler;
    IRQ_Handler PDM_IRQHandler;
    IRQ_Handler NVMC_ACL_IRQHandler;
    IRQ_Handler PPI_IRQHandler;
    IRQ_Handler MWU_IRQHandler;         /* 48 */
    IRQ_Handler PWM1_IRQHandler;
    IRQ_Handler PWM2_IRQHandler;
    IRQ_Handler SERIAL2_IRQHandler;
    IRQ_Handler RTC2_IRQHandler;
    IRQ_Handler I2S_IRQHandler;
    IRQ_Handler FPU_IRQHandler;
    IRQ_Handler USBD_IRQHandler;
    IRQ_Handler UARTE1_IRQHandler;      /* 56 */
    IRQ_Handler Reserved_41;
    IRQ_Handler Reserved_42;
    IRQ_Handler Reserved_43;
    IRQ_Handler Reserved_44;
    IRQ_Handler PWM3_IRQHandler;
    IRQ_Handler Reserved_46;
    IRQ_Handler SPIM3_IRQHandler;
    /* 64 */
} NVIC_Table;

NVIC_Table isr_vectors __attribute__((section(".isr_vectors"))) __attribute__((used));
