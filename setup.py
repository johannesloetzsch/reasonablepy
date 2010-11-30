from distutils.core import setup, Extension

import sys, os

if __name__ == '__main__':
	xsb_home = '/usr/lib/xsb/3.2'
	filestr = 'xsb_home = \'' + xsb_home + '\'\n'

	flora2_home = '/usr/lib/flora2'
	filestr += 'flora2_home = \'' + flora2_home + '\'\n'

	libfile = open( os.path.join( 'rp', 'libs.py' ), 'w' )
	libfile.write( filestr )
	libfile.close()

	platform = 'i686-pc-linux-gnu-deb'
	
	include1 = os.path.join( xsb_home, 'config', platform )
	include2 = os.path.join( xsb_home, 'emu' )
	xsb_obj  = os.path.join( include1, 'saved.o', 'xsb.o' )


setup(name='ReasonablePython',
	version='0.1.2',
	url='http://reasonablepy.sourcforge.net',
	author='Markus Schatten',
	author_email='markus.schatten@foi.hr',
	py_modules = [ 
		'rp.dbms', 
		'rp.__init__', 
		'rp.f', 
		'rp.interface', 
		'rp.py2f',
		'rp.f2py',
		'rp.reasonable',
		'rp.libs', 
		'rp.xsb_swig.__init__', 
		'rp.xsb_swig.xsb' ],
	ext_modules=[ 	Extension(
				"rp.xsb_swig._xsb", 
				[ "rp/xsb_swig/swig_xsb_wrap.c", "rp/xsb_swig/swig_xsb.c" ], 
				include_dirs = [ include1, include2 ], 
				extra_link_args =[ xsb_obj ]
			)
		]
		   	
      )

