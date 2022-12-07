#pragma once

#include "SX127xRegs.h"
#include "SX12xxDriverCommon.h"

class SX127xHal
{

public:
    static SX127xHal *instance;

    SX127xHal();

    void init();
    void end();
    void reset();

    void ICACHE_RAM_ATTR setNss(uint8_t radioNumber, bool state);

    uint8_t ICACHE_RAM_ATTR readRegisterValue(uint8_t reg, uint8_t msb = 7, uint8_t lsb = 0, SX12XX_Radio_Number_t radioNumber = SX12XX_Radio_1);
    uint8_t ICACHE_RAM_ATTR readRegister(uint8_t reg, SX12XX_Radio_Number_t radioNumber = SX12XX_Radio_1);
    void ICACHE_RAM_ATTR readRegister(uint8_t reg, uint8_t *data, uint8_t numBytes, SX12XX_Radio_Number_t radioNumber = SX12XX_Radio_1);

    void ICACHE_RAM_ATTR writeRegisterValue(uint8_t reg, uint8_t value, uint8_t msb = 7, uint8_t lsb = 0, SX12XX_Radio_Number_t radioNumber = SX12XX_Radio_1);
    void ICACHE_RAM_ATTR writeRegister(uint8_t reg, uint8_t data, SX12XX_Radio_Number_t radioNumber = SX12XX_Radio_1);
    void ICACHE_RAM_ATTR writeRegister(uint8_t reg, uint8_t *data, uint8_t numBytes, SX12XX_Radio_Number_t radioNumber = SX12XX_Radio_1);

    void ICACHE_RAM_ATTR TXenable(SX12XX_Radio_Number_t radioNumber = SX12XX_Radio_1);
    void ICACHE_RAM_ATTR RXenable();
    void ICACHE_RAM_ATTR TXRXdisable();

    static ICACHE_RAM_ATTR void dioISR_1();
    static ICACHE_RAM_ATTR void dioISR_2();
    void (*IsrCallback_1)(); // function pointer for callback
    void (*IsrCallback_2)(); // function pointer for callback

private:
#if defined(PLATFORM_ESP32)
    uint64_t txrx_disable_clr_bits;
    uint64_t tx1_enable_set_bits;
    uint64_t tx1_enable_clr_bits;
    uint64_t tx2_enable_set_bits;
    uint64_t tx2_enable_clr_bits;
    uint64_t rx_enable_set_bits;
    uint64_t rx_enable_clr_bits;
#else
    bool rx_enabled;
    bool tx1_enabled;
    bool tx2_enabled;
#endif
};