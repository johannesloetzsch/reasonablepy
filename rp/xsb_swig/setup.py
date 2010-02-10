from distutils.core import setup, Extension

setup(name="swig_xsb", version="0.0",
        ext_modules = [Extension("_swig_xsb", ["swig_xsb_wrap.c", "swig_xsb.c"], include_dirs = [ 
'/home/mschatte/myPackages/XSB/config/i686-pc-linux-gnu', '/home/mschatte/myPackages/XSB/emu'], extra_link_args = 
[ '/home/mschatte/myPackages/XSB/config/i686-pc-linux-gnu/saved.o/xsb.o' ] )])
