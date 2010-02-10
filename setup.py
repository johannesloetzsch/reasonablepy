from distutils.core import setup, Extension

import sys, os

if __name__ == '__main__':
	xsb_ok = False
	platform_ok = False
	flora2_ok = False
	for i in sys.argv:
		if i == '--xsb':
			xsb_home = sys.argv[ sys.argv.index( i ) + 1 ]
			xsb_ok = True
		if i == '--platform':
                        platform = sys.argv[ sys.argv.index( i ) + 1 ]
		if i == '--flora2':
                        flora2_home = sys.argv[ sys.argv.index( i ) + 1 ]
			flora2_ok = True
	if not xsb_ok and 'build' in sys.argv:
		raise ValueError, 'Must supply --xsb /path/to/xsb/ in order to build Reasonable Python'
	if not flora2_ok and 'build' in sys.argv:
		raise ValueError, 'Must supply --flora2 /path/to/flora2/ in order to build Reasonable Python'
	if not xsb_ok:
		xsb_home = 'bogus'
	else:
		filestr = 'xsb_home = \'' + xsb_home + '\'\n'
		sys.argv = sys.argv[ :-2 ]
	if not flora2_ok:
		flora2_home = 'bogus'
	else:
		filestr += 'flora2_home = \'' + flora2_home + '\'\n'
		sys.argv = sys.argv[ :-2 ]

	if xsb_ok and flora2_ok:
		libfile = open( os.path.join( 'rp', 'libs.py' ), 'a' )
		libfile.write( filestr )
		libfile.close()

	if not platform_ok:
		platform = 'i686-pc-linux-gnu'
	else:
		sys.argv = sys.argv[ :-2 ]
	
	include1 = os.path.join( xsb_home, 'config', platform )
	include2 = os.path.join( xsb_home, 'emu' )
	xsb_obj  = os.path.join( include1, 'saved.o', 'xsb.o' )

	
        sys.argv = sys.argv[ :2 ]

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

