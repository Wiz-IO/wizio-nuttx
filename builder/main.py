'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
import click
from os.path import join
from SCons.Script import (AlwaysBuild,Default,DefaultEnvironment,Builder)
from frameworks.common import INTEGRATION, dev_init, dev_run_menuconfig
from frameworks.wiz import FRAMEWORK_NAME

env                  = DefaultEnvironment()
platform             = env.PioPlatform()
board                = env.BoardConfig()
env['PLATFORM_DIR' ] = env.platform_dir  = env.PioPlatform().get_dir()
env['FRAMEWORK_DIR'] = env.framework_dir = env.PioPlatform().get_package_dir( FRAMEWORK_NAME )
env.DIR_SCONS        = join(env.platform_dir,  'scons')
env.DIR_NUTTX        = join(env.framework_dir, 'nuttx')
env.BOARD            = env.BoardConfig().get("build.board") # 'stm32f3discovery'
env.ARCH             = env.BoardConfig().get("build.arch")  # 'arm'
env.CHIP             = env.BoardConfig().get("build.chip")  # 'stm32'

click.secho('<<< NUTTX - PLATFORMIO WizIO 2024 Georgi Angelov >>>', fg='blue')

def cb_menuconfig(*args, **kwargs): 
    dev_run_menuconfig(env)
env.AddCustomTarget('menuconfig', None, cb_menuconfig, title = "MENUCONFIG", description = "Edit Project .config" )

dev_init(env) # INIT COMPILER

if not INTEGRATION():
    env.Append( 
        BUILDERS = dict(
            ELF2HEX = Builder(
                action = env.VerboseAction(' '.join([ '$OBJCOPY', '-O',  'ihex', '$SOURCES', '$TARGET', ]), 'Building HEX $TARGET'),
                suffix = '.hex'
            ),
            ELF2BIN = Builder(
                action = env.VerboseAction(' '.join([ '$OBJCOPY', '-O',  'binary', '-S', '$SOURCES', '$TARGET', ]), 'Building BIN $TARGET'),
                suffix = '.bin'
            ),
        )        
    )
    elf = env.BuildProgram()
    bin = env.ELF2BIN( join('$BUILD_DIR', '${PROGNAME}'), elf )
    hex = env.ELF2HEX( join('$BUILD_DIR', '${PROGNAME}'), elf )
    prg = env.Alias( 'buildprog', hex)
    AlwaysBuild( hex, bin )
    Default( hex, bin )

# print(env.Dump())

