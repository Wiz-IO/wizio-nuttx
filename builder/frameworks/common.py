'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
import os, sys
from os.path import join, exists
from shutil import copyfile
from datetime import datetime
from SCons.Script import (COMMAND_LINE_TARGETS)
from platformio import proc
from frameworks.wiz import MKDIR, CPDIR, ERROR, GET

def INTEGRATION():
    return any(p in COMMAND_LINE_TARGETS for p in ['__idedata', 'idedata', 'menuconfig'])

#################################################

def create_config():
    if exists( join('include', 'nuttx', 'config.h') ): return
    dequote_list = [
# NuttX        
"CONFIG_DEBUG_OPTLEVEL",                # Custom debug level
"CONFIG_EXECFUNCS_NSYMBOLS_VAR",        # Variable holding number of symbols in the table
"CONFIG_EXECFUNCS_SYMTAB_ARRAY",        # Symbol table array used by exec[l|v]
"CONFIG_INIT_ARGS",                     # Argument list of entry point ... "\"-c\", \"ostest;poweroff\""
"CONFIG_INIT_SYMTAB",                   # Global symbol table
"CONFIG_INIT_NEXPORTS",                 # Global symbol table size
"CONFIG_INIT_ENTRYPOINT",               # Name of entry point function
"CONFIG_MODLIB_SYMTAB_ARRAY",           # Symbol table array used by modlib functions
"CONFIG_MODLIB_NSYMBOLS_VAR",           # Variable holding number of symbols in the table
"CONFIG_PASS1_BUILDIR",                 # Pass1 build directory
"CONFIG_PASS1_TARGET",                  # Pass1 build target
"CONFIG_PASS1_OBJECT",                  # Pass1 build object
"CONFIG_TTY_LAUNCH_ENTRYPOINT",         # Name of entry point from tty launch
"CONFIG_TTY_LAUNCH_ARGS",               # Argument list of entry point from tty launch
# NxWidgets/NxWM
"CONFIG_NXWM_BACKGROUND_IMAGE",         # Name of bitmap image class
"CONFIG_NXWM_CALIBRATION_ICON",         # Name of bitmap image class
"CONFIG_NXWM_HEXCALCULATOR_ICON",       # Name of bitmap image class
"CONFIG_NXWM_MINIMIZE_BITMAP",          # Name of bitmap image class
"CONFIG_NXWM_NXTERM_ICON",              # Name of bitmap image class
"CONFIG_NXWM_STARTWINDOW_ICON",         # Name of bitmap image class
"CONFIG_NXWM_STOP_BITMAP",              # Name of bitmap image class
# apps/ definitions
"CONFIG_NSH_SYMTAB_ARRAYNAME",          # Symbol table array name
"CONFIG_NSH_SYMTAB_COUNTNAME",          # Name of the variable holding the number of symbols
    ]
    dir = join('include', 'nuttx')
    if dir and not exists(dir): 
        os.makedirs(dir, exist_ok=True)
    w = open(join( dir, 'config.h' ), 'w')
    r = open('.config', 'r')
    w.write( "/* config.h -- PlatformIO ( %s ) Autogenerated! Do not edit. */\n\n" % datetime.now() )
    w.write(
"#ifndef __INCLUDE_NUTTX_CONFIG_H\n"
"#define __INCLUDE_NUTTX_CONFIG_H\n\n"
"/* Used to represent the values of tristate options */\n\n"
"#define CONFIG_y 1\n"
"#define CONFIG_m 2\n\n"
"/* General Definitions ***********************************/\n")
    for line in r.readlines():
        line = line.strip()
        if line.startswith('#') or len(line) < 3: continue
        var, val = line.split("=")
        var = var.strip()
        val = val.strip()
        if var in dequote_list: 
            val = val[1:-1].replace('\',') # TODO CHECK "\"-c\", \"ostest;poweroff\""
            if val == '': continue
        if val == 'y':
            w.write("#define %s 1\n" % var)
        elif val == 'n':
            w.write("#undef %s\n" % var)
        elif val == 'm':
            w.write("#define %s 2\n" % var)
        else:
            w.write("#define %s %s\n" % (var, val))
    w.write(
"\n/* Sanity Checks *****************************************/\n\n"
"/* If the end of RAM is not specified then it is assumed to be\n"
" * the beginning of RAM plus the RAM size.\n"
" */\n\n"
"#ifndef CONFIG_RAM_END\n"
"#  define CONFIG_RAM_END (CONFIG_RAM_START+CONFIG_RAM_SIZE)\n"
"#endif\n\n"
"#ifndef CONFIG_RAM_VEND\n"
"#  define CONFIG_RAM_VEND (CONFIG_RAM_VSTART+CONFIG_RAM_SIZE)\n"
"#endif\n\n"
"/* If the end of FLASH is not specified then it is assumed to be\n"
" * the beginning of FLASH plus the FLASH size.\n"
" */\n\n"
"#ifndef CONFIG_FLASH_END\n"
"#  define CONFIG_FLASH_END (CONFIG_FLASH_START+CONFIG_FLASH_SIZE)\n"
"#endif\n\n"
"#endif /* __INCLUDE_NUTTX_CONFIG_H */\n")

def dev_run_menuconfig(env):  
    args = [
        proc.get_pythonexe_path(),
        join(env.platform_dir, 'builder', 'frameworks', 'x_menuconfig.py')
    ]
    os.environ['KCONFIG_PROJECT_CONFIG_DIR'] = os.getcwd()
    os.environ['KCONFIG_CONFIG'] = join(os.getcwd(), '.config')
    os.environ['ARCH']        = env.ARCH
    os.environ['APPSDIR']     = './apps'
    os.environ['APPSBINDIR']  = './apps'
    os.environ['BINDIR']      = '.'
    os.environ['EXTERNALDIR'] = './arch/dummy'
    res = proc.exec_command( args, 
        stdout = sys.stdout, stderr = sys.stderr, stdin = sys.stdin, cwd = env.DIR_NUTTX) 
    if 0 == res['returncode']: 
        create_config()

#################################################

def load_config(env):
    env.CONFIG = {}
    if not exists('.config'): 
        ERROR('Project ".config" not exists')
    lines = open('.config', 'r').readlines()
    for line in lines:
        line = line.strip()
        if line.startswith('#') or len(line) < 3: continue
        var, val = line.split("=")
        env.CONFIG[var.strip()] = val.strip()

    #arch\arm
    env.DIR_ARCH = join(env.DIR_NUTTX, 'arch', GET(env, 'CONFIG_ARCH')) 

    #arch\arm\include
    env.DIR_ARCH_INC = join(env.DIR_ARCH, 'include')

    #arch\arm\src
    env.DIR_ARCH_SRC = join(env.DIR_ARCH, 'src')

    #arch\arm\include\armv7-m
    env.DIR_FAMILY_INC = join(env.DIR_ARCH_INC, GET(env, 'CONFIG_ARCH_FAMILY'))

    #arch\arm\src\armv7-m
    env.DIR_FAMILY_SRC = join(env.DIR_ARCH_SRC, GET(env, 'CONFIG_ARCH_FAMILY'))

    #arch\arm\include\stm32
    env.DIR_CHIP_INC = join(env.DIR_ARCH_INC, GET(env, 'CONFIG_ARCH_CHIP'))

    #arch\arm\src\stm32 (-I)
    env.DIR_CHIP_SRC = join(env.DIR_ARCH_SRC, GET(env, 'CONFIG_ARCH_CHIP'))

    #arch\arm\src\common
    env.DIR_COMMON_SRC = join(env.DIR_ARCH_SRC, 'common')

    #boards\arm\stm32\stm32f3discovery
    env.DIR_BOARD = join(env.DIR_NUTTX, 'boards', GET(env, 'CONFIG_ARCH'), 
        GET(env, 'CONFIG_ARCH_CHIP'), GET(env, 'CONFIG_ARCH_BOARD'))

def create_include(env): 
    arch = join('include', 'arch')
    MKDIR(arch)
    CPDIR(env.DIR_ARCH_INC, arch)
    dst = join(arch, 'chip' )
    MKDIR(dst)
    CPDIR(env.DIR_CHIP_INC, dst)
    dst = join(arch, GET(env, 'CONFIG_ARCH_CHIP') )
    MKDIR(dst)
    CPDIR(env.DIR_CHIP_INC, dst)
    dst = join(arch, GET(env, 'CONFIG_ARCH_FAMILY'))
    MKDIR(dst)
    CPDIR(env.DIR_FAMILY_INC, dst)
    dst = join(arch, 'board' )
    MKDIR(dst)
    CPDIR(join(env.DIR_BOARD, 'include'), dst)

def create_family(env):
    env.SConscript(
        join(env.DIR_SCONS, 'arch', env.ARCH, 'Toolchain-%s.py' % GET(env, 'CONFIG_ARCH_FAMILY')), 
        exports=['env']
    )

def create_version(env):
    # TODO INIT VERSION
    env.CONFIG['CONFIG_VERSION_STRING'] = '0.0.0'
    env.CONFIG['CONFIG_VERSION_MAJOR']  = 0
    env.CONFIG['CONFIG_VERSION_MINOR']  = 0
    env.CONFIG['CONFIG_VERSION_PATCH']  = 0
    env.CONFIG['CONFIG_VERSION_BUILD']  = '0'
    src = join('include', 'nuttx', 'version.h')
    if not exists(src):
        open(src, 'w').write(
'''
/* version.h -- PlatformIO Autogenerated! Do not edit. */\n
#ifndef __INCLUDE_NUTTX_VERSION_H
#define __INCLUDE_NUTTX_VERSION_H

#define CONFIG_VERSION_STRING   "%s"
#define CONFIG_VERSION_MAJOR    %s
#define CONFIG_VERSION_MINOR    %s
#define CONFIG_VERSION_PATCH    %s
#define CONFIG_VERSION_BUILD    "%s"

#define CONFIG_VERSION ((CONFIG_VERSION_MAJOR << 16) |\\
                        (CONFIG_VERSION_MINOR << 8) |\\
                        (CONFIG_VERSION_PATCH))\n
#endif /* __INCLUDE_NUTTX_VERSION_H */''' % (
            env.CONFIG['CONFIG_VERSION_STRING'],
            env.CONFIG['CONFIG_VERSION_MAJOR'],
            env.CONFIG['CONFIG_VERSION_MINOR'], 
            env.CONFIG['CONFIG_VERSION_PATCH'],
            env.CONFIG['CONFIG_VERSION_BUILD']
        ) )

def create_main(env):
    if exists(join('src', 'main.c')): pass 
    elif exists(join('src', 'main.cpp')): pass
    else:
        open(join('src', 'main.c'), 'w').write(
'''
/* PlatformIO Template */

#include <nuttx/config.h>
#include <stdio.h>

int main(int argc, FAR char *argv[])
{
  printf("Hello, World");
  return 0;
}''' )

def dev_begin(env):
    board_dir = join(env.DIR_NUTTX, 'boards', env.ARCH, env.CHIP, env.BOARD)
    env.Replace( LDSCRIPT_PATH = join(board_dir, 'scripts', 'ld.script') )
    create_main(env)
    load_config(env)
    create_include(env)  
    create_family(env)
    create_version(env)

def dev_end(env):
    ENV = env
    env.SConscript( # TODO CHECK FOR APPLICATION
        join(env.DIR_SCONS, 'arch', env.ARCH, 'Toolchain-common.py'), 
        exports=['ENV']
    )
    env.Append( CPPPATH = [ 
        join('$PROJECT_DIR', 'lib'),
        join('$PROJECT_DIR', 'src'),
    ] ) 

def dev_init(env):
    env.Replace(
        BUILD_DIR       = env.subst('$BUILD_DIR'),
        ARFLAGS         = ['rc'],
        ASFLAGS         = ['-x', 'assembler-with-cpp', '-D__ASSEMBLY__'],           
        CPPDEFINES      = ['__NuttX__', '__KERNEL__'],
        CPPPATH         = [
            join('$PROJECT_DIR', 'include'),
            join(env.DIR_NUTTX,  'include'),  
            join(env.DIR_NUTTX,  'sched'),          
        ],
        CFLAGS          = [],
        CCFLAGS         = [],
        CXXFLAGS        = [],
        LIBS            = [],
        LINKFLAGS       = ['-nostartfiles','-nodefaultlibs','-nostdlib', ], 
        LIBPATH         = [join('$PROJECT_DIR', 'lib')],
        LIBSOURCE_DIRS  = [join('$PROJECT_DIR', 'lib')],        
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
