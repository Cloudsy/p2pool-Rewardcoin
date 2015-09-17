from distutils.core import setup, Extension

Rewardcoin_momentum_module = Extension('Rewardcoin_momentum',
                               libraries = ['ssl', 'crypto'],
                               sources = ['momentummodule.c',
                                          'groestl.c',
                                          'keccak.c',
                                          'momentum.cpp'],
                               include_dirs=['.'])

setup (name = 'Rewardcoin_momentum',
       version = '1.0',
       description = 'Bindings for AES-NI momentum proof of work used by Rewardcoin',
       ext_modules = [Rewardcoin_momentum_module])
