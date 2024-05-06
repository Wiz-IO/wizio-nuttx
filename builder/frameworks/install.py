'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
import os, sys, time
from os.path import join, exists, normpath, dirname
from platformio import proc
sys.path.append( dirname( __file__ ) )
from wiz import FRAMEWORK_NAME, ERROR, RMDIR

def install_python_requirements():
    try:
        import kconfiglib
    except ImportError:
        print(' * Installing Python requirements')
        args = [ proc.get_pythonexe_path(), '-m', 'pip', '-q', 'install', '-r', 'requirements.txt' ]
        res = proc.exec_command( args, 
            stdout = sys.stdout, stderr = sys.stderr, stdin = sys.stdin, 
            cwd = normpath( dirname( __file__ ) )
        )
        if 0 == res['returncode']:
            print(' * Python Requirements Done')
        else:
            ERROR('[PIP] Please, try later, result = %d' % res) 

def install_nuttx(url, dir):
    print(' * Cloning NuttX ...')
    begin = time.time()
    args = [ 'git', 'clone', url, dir ] # , '--quiet'
    res = proc.exec_command( args, 
        stdout = sys.stdout, stderr = sys.stderr, stdin = sys.stdin 
    )
    if 0 != res['returncode']:
        RMDIR( dir )
        ERROR('[GIT] Please, try later, result = %d' % res)
    print(' * Cloning took %s seconds' % int( time.time() - begin ) )
    with open( join(dir, 'arch',  'dummy','Kconfig'), "w" ) as f: pass
    with open( join(dir, 'boards','dummy','Kconfig'), "w" ) as f: pass 
    path = join(dir, 'drivers','platform')
    os.makedirs(path, exist_ok=True)
    with open( join(path,'Kconfig'), "w" ) as f: pass 
    path = join(dir, 'apps')
    os.makedirs(path, exist_ok=True)
    with open( join(path,'Kconfig'), "w" ) as f: pass     

def dev_install(var, url):
    ENV = FRAMEWORK_DIR = var
    if isinstance(FRAMEWORK_DIR, str) and not exists( FRAMEWORK_DIR ):
        print(' * [WARNING] FRAMEWORK FOLDER NOT EXISTS')
        return
    if 'SConsEnvironment' in str( type( ENV ) ):
        FRAMEWORK_DIR = ENV.PioPlatform().get_package_dir( FRAMEWORK_NAME )
        url = ENV.PioPlatform().packages[FRAMEWORK_NAME]['nuttx']
    else:
        install_python_requirements()
    dir = join( FRAMEWORK_DIR, 'nuttx' )
    if not exists( dir ): 
        install_nuttx( url, dir ) 
 