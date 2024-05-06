'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
import os
from os.path import join, exists
from shutil import copyfile
from SCons.Script import (COMMAND_LINE_TARGETS)
from frameworks.wiz import ERROR

def INTEGRATION():
    return any(p in COMMAND_LINE_TARGETS for p in ['__idedata', 'menuconfig'])

def dev_init_template(env):
    if not exists('config'):
        os.makedirs('config', exist_ok=True)
        # TODO CREATE TEMPLATE MAIN.C

def dev_init_config(env):
    src = join(env.framework_dir, 'nuttx', 'boards', env.ARCH, env.CHIP, env.BOARD, 'configs', env.NSH )
    if not exists(src): 
        ERROR('NuttX Board not found')
        copyfile( join(src, 'defconfig'), join('config', '.config'))
    else: 
        # TODO LOAD CONFIG
        pass

def dev_init(env):
    env.Replace(
        BUILD_DIR = env.subst('$BUILD_DIR'),
        ARFLAGS         = ['rc'],
        ASFLAGS         = ['-x', 'assembler-with-cpp', '-D__ASSEMBLY__'],           
        CPPDEFINES      = ['__NuttX__'],
        CPPPATH         = [],
        CFLAGS          = [],
        CCFLAGS         = [],
        CXXFLAGS        = [],
        LIBS            = [],
        LINKFLAGS       = ['-nostartfiles','-nodefaultlibs','-nostdlib', ], 
        LIBPATH        = [join('$PROJECT_DIR', 'lib')],
        LIBSOURCE_DIRS = [join('$PROJECT_DIR', 'lib')],        
        PROGSUFFIX      = '.elf',       
    )
    if 'arm' == env.ARCH:
        env.Replace(
            AR          = 'arm-none-eabi-ar',
            AS          = 'arm-none-eabi-as',
            CC          = 'arm-none-eabi-gcc',
            GDB         = 'arm-none-eabi-gdb',
            CXX         = 'arm-none-eabi-g++',
            OBJCOPY     = 'arm-none-eabi-objcopy',
            RANLIB      = 'arm-none-eabi-ranlib',
            SIZETOOL    = 'arm-none-eabi-size',
    )
    else: ERROR('Unsupported Architecture')



