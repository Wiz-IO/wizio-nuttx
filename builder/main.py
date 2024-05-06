'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
import click
from os.path import join
from SCons.Script import (AlwaysBuild,Default,DefaultEnvironment,Builder,COMMAND_LINE_TARGETS)
from frameworks.common import INTEGRATION, dev_init, dev_run_menuconfig
from frameworks.wiz import ERROR
print('[MAIN] START', COMMAND_LINE_TARGETS ) #['__idedata'],['menuconfig'],['upload'],[]

PLATFORM_NAME        = 'wizio-nuttx'
FRAMEWORK_NAME       = 'framework-' + PLATFORM_NAME
env                  = DefaultEnvironment()
platform             = env.PioPlatform()
board                = env.BoardConfig()
env['PLATFORM_DIR' ] = env.platform_dir  = env.PioPlatform().get_dir()
env['FRAMEWORK_DIR'] = env.framework_dir = env.PioPlatform().get_package_dir( FRAMEWORK_NAME )
env.BOARD            = env.BoardConfig().get("build.board") # 'stm32f3discovery:nsh'
env.NSH              = env.BoardConfig().get("build.nsh")   # 'stm32f3discovery:nsh'
env.ARCH             = env.BoardConfig().get("build.arch")  # 'arm'
env.CHIP             = env.BoardConfig().get("build.chip")  # 'stm32'

click.secho('\n<<< NUTTX - PLATFORMIO WizIO 2024 Georgi Angelov >>>\n', fg='blue')

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

print('[MAIN] END')
# print(env.Dump())

