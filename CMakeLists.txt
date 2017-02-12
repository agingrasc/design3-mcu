cmake_minimum_required(VERSION 3.6)
project(design3-mcu C ASM)

set(CMAKE_C_STANDARD 11)

set(STM_ROOT "/opt/stm32/STM32F4-Discovery_FW_V1.1.0")
set(STM_SRC_ROOT "${STM_ROOT}/Libraries/STM32F4xx_StdPeriph_Driver/src")

#add_compile_options(-DSTM32F4 -DUSE_STDPERIPH_DRIVER)

function(add_bin_from_elf bin elf)
    add_custom_target(${bin} ALL ${CMAKE_OBJCOPY} -Obinary ${elf} ${bin} DEPENDS ${elf})
endfunction()

include_directories("./inc"
        "${STM_ROOT}/Utilities/STM32F4-Discovery"
        "${STM_ROOT}/Libraries/CMSIS/Include"
        "${STM_ROOT}/Libraries/CMSIS/ST/STM32F4xx/Include"
        "${STM_ROOT}/Libraries/STM32F4xx_StdPeriph_Driver/inc")

set(SOURCE_FILES
        src/main.c
        src/manchester.c
        src/system_stm32f4xx.c
        src/CommandHandler.c
        src/delay.c
        src/id.c
        src/LCD.c
        src/MotorController.c
        src/MotorEncoder.c
        src/pid.c
        src/tm_stm32f4_usb_vcp.c
        src/uart.c
        src/usb_bsp.c
        src/usb_core.c
        src/usb_dcd.c
        src/usb_dcd_int.c
        src/usbd_cdc_core.c
        src/usbd_cdc_vcp.c
        src/usbd_core.c
        src/usbd_desc.c
        src/usbd_ioreq.c
        src/usbd_req.c
        src/usbd_usr.c
        src/command.c
        ${STM_SRC_ROOT}/stm32f4xx_gpio.c
        ${STM_SRC_ROOT}/stm32f4xx_tim.c
        ${STM_SRC_ROOT}/stm32f4xx_rcc.c
        ${STM_SRC_ROOT}/stm32f4xx_usart.c
        ${STM_SRC_ROOT}/stm32f4xx_exti.c
        ${STM_SRC_ROOT}/misc.c
        )

# Flags de compilation par source
set(STM32_FLAGS "-mfpu=fpv4-sp-d16 -mthumb -mthumb-interwork -mlittle-endian -mfloat-abi=hard -march=armv7-m")
set(GENERAL_COMPILE_FLAGS"-Wall")
set(GENERAL_COMPILE_DEFINE "-DSTM32F4 -DUSE_STDPERIPH_DRIVER -DSTM32F40XX -DSTM32F40_41xxx")
set_source_files_properties(${SOURCE_FILES} PROPERTY COMPILE_FLAGS "${STM32_FLAGS} ${GENERAL_COMPILE_FLAGS} ${GENERAL_COMPILE_DEFINE}")
set_source_files_properties(startup/startup_stm32.s PROPERTY COMPILE_FLAGS "${STM32_FLAGS}")

# Linker file avec fichier de link
set(LINKER_SCRIPT "../stm32_flash.ld" CACHE STRING "")
# se base sur le toolchain file, ajoute simplement le linker script
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -T ${LINKER_SCRIPT} -nostartfiles --specs=nosys.specs")


add_executable(${PROJECT_NAME} ${SOURCE_FILES} startup/startup_stm32.s)
add_executable(${PROJECT_NAME}.elf ${SOURCE_FILES} startup/startup_stm32.s)
add_bin_from_elf(${PROJECT_NAME}.bin ${PROJECT_NAME}.elf)
