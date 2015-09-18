from distutils.core import setup, Extension

rewardcoin_momentum_module = Extension('rewardcoin_momentum',
#			       extra_compile_args = ['-Wunused-but-set-variable'],
                               libraries = ['ssl', 'crypto'],
                               sources = ['momentummodule.c',
                                          'momentum.c',
					  'groestl.c'],
                               include_dirs=['.'],
			       language = ['c++'])

setup (name = 'rewardcoin_momentum',
       version = '1.0',
       description = 'Bindings for AES-NI momentum proof of work used by Rewardcoin',
       ext_modules = [rewardcoin_momentum_module])
