include(CMakeForceCompiler)
# info generique
set(CMAKE_SYSTEM_NAME  Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

# toolchain path
set(CROSS_COMPILE arm-none-eabi-)

# binaire pour la compilation
#CMAKE_FORCE_C_COMPILER(/usr/bin/arm-none-eabi-gcc GNU)
set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_ASM_COMPILER arm-none-eabi-as)

set(CMAKE_OBJCOPY arm-none-eabi-objcopy
        CACHE FILEPATH "The toolchain objcopy command" FORCE)

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --specs=nosys.specs" CACHE STRING "")

# sysroot de compilation croisee
set(CMAKE_FIND_ROOT_PATH /usr/arm-none-eabi)

# parametre pour la recherche
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

