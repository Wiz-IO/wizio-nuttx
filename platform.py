'''
    Copyright 2024 WizIO ( Georgi Angelov )
'''

from os.path import join, dirname, exists
from importlib.machinery import SourceFileLoader
from platformio.managers.platform import PlatformBase

FRAMEWORK_NAME = 'framework-wizio-nuttx'

class WizionuttxPlatform(PlatformBase):

    def is_embedded(self):
        return True

    def get_boards(self, id_=None):
        board = PlatformBase.get_boards(self, id_)
        # TODO: Debuger
        return board

    def get_package_type(self, name):
        Type = self.packages[name].get('type')
        if 'framework' == Type:
            self.install(1) # wiz.MODE_INTEGRATE
        return Type

    def on_installed(self):
        self.install(0) # wiz.MODE_INSTALL

    def install(self, mode):
        filepath = join( dirname( __file__ ), 'builder', 'frameworks', 'install.py' )
        if exists( filepath ):
            SourceFileLoader(
                'module_' +  str(abs(hash(filepath))), 
                filepath).load_module().dev_install(
                    join(self.config.get('platformio', 'core_dir'), 'packages', FRAMEWORK_NAME),
                self.packages[FRAMEWORK_NAME].get('git'),
                mode 
            )