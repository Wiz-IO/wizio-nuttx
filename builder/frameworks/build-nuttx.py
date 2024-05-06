'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
from SCons.Script import (DefaultEnvironment,COMMAND_LINE_TARGETS)
from frameworks.common import INTEGRATION
from frameworks.wiz import ERROR

if not INTEGRATION():
    print('[BUILD] START', COMMAND_LINE_TARGETS) #[]

    env = DefaultEnvironment()

    print('[BUILD] END')