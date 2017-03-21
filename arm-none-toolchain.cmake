include(CMakeForceCompiler)
# info generique
set(CMAKE_SYSTEM_NAME  Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

# toolchain path
set(CROSS_COMPILE arm-none-eabi-)

# binaire pour la compilation
CMAKE_FORCE_C_COMPILER(/usr/bin/arm-none-eabi-gcc GNU)
set(CMAKE_C_COMPILER /usr/bin/arm-none-eabi-gcc)
set(CMAKE_ASM_COMPILER /usr/bin/arm-none-eabi-as)

set(CMAKE_OBJCOPY arm-none-eabi-objcopy
        CACHE FILEPATH "The toolchain objcopy command" FORCE)

# sysroot de compilation croisee
#set(CMAKE_SYSROOT /opt/gcc-arm-embedded/gcc-arm-none-eabi-5_4-2016q2)
set(CMAKE_FIND_ROOT_PATH /opt/gcc-arm-embedded/gcc-arm-none-eabi-5_4-2016q2/lib/fpu)

# parametre pour la recherche
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

