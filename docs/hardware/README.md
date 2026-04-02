# Hardware & Peripherals Docs

For board integration, firmware flow, and peripheral architecture.

ZeroClaw's hardware subsystem enables direct control of microcontrollers and peripherals via the `Peripheral` trait. Each board exposes tools for GPIO, ADC, and sensor operations, allowing agent-driven hardware interaction on boards like STM32 Nucleo, Raspberry Pi, and ESP32. See [hardware-peripherals-design.md](/docs/hardware/hardware-peripherals-design) for the full architecture.

## Entry Points

- Architecture and peripheral model: [hardware-peripherals-design.md](/docs/hardware/hardware-peripherals-design)
- Add a new board/tool: [../contributing/adding-boards-and-tools.md](/docs/contributing/adding-boards-and-tools)
- Nucleo setup: [nucleo-setup.md](/docs/hardware/nucleo-setup)
- Arduino Uno R4 WiFi setup: [arduino-uno-q-setup.md](/docs/hardware/arduino-uno-q-setup)

## Datasheets

- Datasheet index: [datasheets](datasheets)
- STM32 Nucleo-F401RE: [datasheets/nucleo-f401re.md](/docs/hardware/datasheets/nucleo-f401re)
- Arduino Uno: [datasheets/arduino-uno.md](/docs/hardware/datasheets/arduino-uno)
- ESP32: [datasheets/esp32.md](/docs/hardware/datasheets/esp32)
