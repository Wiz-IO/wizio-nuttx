'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
from os.path import join
from SCons.Script import DefaultEnvironment
from frameworks.common import INTEGRATION, dev_begin, dev_end
env = DefaultEnvironment()

if not INTEGRATION():
    dev_begin(env)
    #env.SConscript( join(env.platform_dir, 'scons', 'libs', 'libs.py'),     exports=['env'] )
    env.SConscript( join(env.platform_dir, 'scons', 'arch', 'arch.py'),     exports=['env'] )
    #env.SConscript( join(env.platform_dir, 'scons', 'boards', 'board.py'),  exports=['env'] )
    #env.SConscript( join(env.platform_dir, 'scons', 'mm', 'mm.py'),         exports=['env'] )
    env.SConscript( join(env.platform_dir, 'scons', 'sched', 'sched.py'),   exports=['env'] )
    dev_end(env)
