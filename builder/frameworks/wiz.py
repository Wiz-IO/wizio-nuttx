'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''
import os, sys, shutil, time, click, inspect
from os.path import join, exists

PLATFORM_NAME  = 'wizio-nuttx'
FRAMEWORK_NAME = 'framework-' + PLATFORM_NAME

def LOG(txt = ''):
    txt = '[] %s() %s' % (inspect.stack()[1][3], txt)
    #open('D:/PIO-NUTTX-LOG.txt', 'a+').write(txt + '\n')
    pass

def ERROR(txt = ''):
    txt = '%s() %s' % (inspect.stack()[1][3], txt)
    click.secho( '[ERROR] %s\n' % txt, fg='red')
    time.sleep(.1)
    sys.exit(-1)

def INFO(txt): 
    click.secho('   %s' % (txt), fg='blue') # BUG: Windows: 4 same chars

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

def CPDIR(src, dst, ext = '.h'):
    files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f)) and f.endswith(ext)]
    for f in files:
        shutil.copy(join(src, f), dst)

### MAKEFILE ###

def DEF(env, key):
    return key in env.CONFIG

def EQU(env, key, val='y'): # and NOT 0
   if DEF(env, key): 
      return env.CONFIG[key] != '0' and env.CONFIG[key] == val
   return False            

def GET(env, key, dequote=True):
   if DEF(env, key): 
      return env.CONFIG[key] if dequote==False else env.CONFIG[key].replace('"', '')
   ERROR('Config key [%s] not found' % key)

def FILTER_ADD(env, path):
    if isinstance(path, list):
        #env.FILTER.extend(['+<%s>' % p for p in path])
        for p in path:
            if not exists(p): 
                ERROR('(LIST) File not found:\n%s' % p)
            env.FILTER.append('+<%s>' % p)
    elif isinstance(path, str):
        if not exists(path): 
            ERROR('(STRING) File not found:\n%s' % path)
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
        elif key in env.CONFIG:
            if val == 0 and env.CONFIG[key] != 0:
                ADD(list)    
            elif val == env.CONFIG[key]:
                ADD(list)                                         
            elif val == '': # IFDEF(KEY)
                ADD(list)
            else: 
                ELSE(list)            
        else: 
            ELSE(list)
