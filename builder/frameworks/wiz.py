'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''

import os, sys, shutil, time, click, inspect
from os.path import exists

PLATFORM_NAME  = 'wizio-nuttx'
FRAMEWORK_NAME = 'framework-' + PLATFORM_NAME

MODE_INSTALL   = 0
MODE_INTEGRATE = 1

def LOG(txt = ''):
    txt = '[] %s() %s' % (inspect.stack()[1][3], txt)
    #open('D:/PIO-NUTTX-LOG.txt', 'a+').write(txt + '\n')
    pass

def ERROR(txt = ''):
    txt = '%s() %s' % (inspect.stack()[1][3], txt)
    click.secho( '[ERROR] %s \n' % txt, fg='red') 
    time.sleep(.1)
    sys.exit(-1)

def INFO(txt): 
    click.secho( '   %s' % (txt), fg='blue') # BUG: Windows: 4 same chars

def MKDIR(dir): 
    if dir and not exists(dir): 
        os.makedirs(dir, exist_ok=True)

def RMDIR(dir):  
    if dir and exists(dir): 
        shutil.rmtree( dir, ignore_errors=True )
        timeout = 50
        while exists( dir ) and timeout > 0: 
            time.sleep(.1)  
            timeout -= 1  
        if timeout == 0: 
            ERROR('Delete folder: %s' % dir)

### MAKEFILE ###

def DEF(env, key):
    return key in env.config

def EQU(env, key, val='y'): # and NOT 0
   if DEF(env, key): 
      return env.config[key] != '0' and env.config[key] == val
   return False            

def GET(env, key, dequote=True):
   if DEF(env, key): 
      return env.config[key] if dequote==False else env.config[key].replace('"', '')
   ERROR('Config key [%s] not found' % key)

def FILTER_ADD(env, path):
    if isinstance(path, list):
        env.FILTER.extend(['+<%s>' % p for p in path])
    elif isinstance(path, str):
        env.FILTER.append('+<%s>' % path)
    else:
        ERROR('FILTER_ADD: %s' % print(type(path)))

def FILTER_APPLY(env, conditions):
    def ADD(list):
        if 'else' in list:
            FILTER_ADD(env, list[:list.index('else')])
        else: 
            FILTER_ADD(env, list)
    def ELSE(list):
        if 'else' in list:
            FILTER_ADD(env, list[list.index('else')+1:])           
    for val, key, *list in conditions:  
        val = val.strip()
        key = key.strip()
        if   val == 'I' and DEF(env, key):  env.Append( CPPPATH = [list] ) # -I if KEY       
        elif val == 'I' and key == '':      env.Append( CPPPATH = [list] ) # -I no KEY  
        elif val == ''  and key == '': 
            ADD(list) # add required source files 
        elif key in env.config:
            if val == 0 and env.config[key] != 0:
                ADD(list)    
            elif val == env.config[key]:
                ADD(list)                                         
            elif val == '': # IFDEF(KEY)
                ADD(list)
            else: 
                ELSE(list)            
        else: 
            ELSE(list)
