'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
from os.path import join
from SCons.Script import DefaultEnvironment
from frameworks.common import INTEGRATION, dev_config
env = DefaultEnvironment()

if not INTEGRATION():
    dev_config(env)
    env.SConscript( join(env.platform_dir, 'scons', 'libs.py') ,  exports=['env'] )
    env.SConscript( join(env.platform_dir, 'scons', 'arch.py') ,  exports=['env'] )
    env.SConscript( join(env.platform_dir, 'scons', 'board.py') , exports=['env'] )
