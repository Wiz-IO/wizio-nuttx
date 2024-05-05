'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
from os.path import join
from SCons.Script import (AlwaysBuild, Default, DefaultEnvironment)
from frameworks.wiz import ERROR
ERROR('TEST')

PLATFORM_NAME   = 'wizio-nuttx'
FRAMEWORK_NAME  = 'framework-' + PLATFORM_NAME
env             = DefaultEnvironment()
platform        = env.PioPlatform()
board           = env.BoardConfig()

print( '\n<<< NUTTX - PLATFORM( IO ) WizIO 2024 Georgi Angelov >>>\n' )
env['PLATFORM_DIR' ] = env.platform_dir  = env.PioPlatform().get_dir()
env['FRAMEWORK_DIR'] = env.framework_dir = env.PioPlatform().get_package_dir( FRAMEWORK_NAME )

def mconfig(env):
    print( 'MENU CONFIG' )
    exit(0)
def menuconfig(*args, **kwargs): mconfig(env)
env.AddCustomTarget( "menuconfig", None, menuconfig, title="menuconfig", description="TODO" )

elf = env.BuildProgram()
bin = env.ELF2BIN( join('$BUILD_DIR', '${PROGNAME}'), elf )
hex = env.ELF2HEX( join('$BUILD_DIR', '${PROGNAME}'), elf )
prg = env.Alias( 'buildprog', hex)
AlwaysBuild( hex, bin )
Default( hex, bin )
# print(env.Dump())
