# -*- coding: utf-8 -*-
#!/usr/bin/python

__doc__ = '''
Reasonable Python
A module for integrating F-logic into Python
	
f2py.py --- translating F-logic back to Python
	
by Markus Schatten <markus_dot_schatten_at_foi_dot_hr>
Faculty of Organization and Informatics,
Varaždin, Croatia, 2007

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

'''

import types

class f2py:
	def classForName( self, name, ns ):
		return ns[ name ]
		
	
	def translate( self, string, gl ):
		if not isinstance( string, str ):
			raise ValueError, 'Only FLORA-2 strings can be translated back to Python objects'
		if not string[ :2 ] == 'py':			
			raise ValueError, 'The supplied string does not seem to be a FLORA-2 string'
		if string == 'pybuffer':
			return types.BufferType
		if string == 'pybuiltinfunction':
			return types.BuiltinFunctionType
		if string == 'pybuiltinmethod':
			return types.BuiltinMethodType
		if string == 'pycode':
			return types.CodeType
		if string == 'pydictproxy':
			return types.DictProxyType
		if string == 'pyellipsis':
			return types.EllipsisType
		if string == 'pyfile':
			return types.FileType
		if string == 'pyframe':
			return types.FrameType
		if string == 'pyfunction':
			return types.FunctionType
		if string == 'pygenerator':
			return types.GeneratorType
		if string == 'pylambda':
			return types.LambdaType
		if string == 'pymethod':
			return types.MethodType
		if string == 'pynotimplemented':
			return types.NotImplementedType
		if string == 'pyslice':
			return types.SliceType
		if string == 'pytraceback':
			return types.TracebackType
		if string == 'pyunboundmethod':
			return types.UnboundMethodType
		if string == 'pyxrange':
			return types.XRangeType
		if string[ 0 ] == '_':
			return None
		if string[ :6 ] == 'pytype' or string[ :8 ] == 'pyclass':
			classname = string.split( 'xxxmarexxx' )[ -1: ][ 0 ]
			package = string.split( 'xxxmarexxx' )[ -1: ][ : ]
			return self.classForName( classname, gl )
		else:
			return 'pyunknown'
	
	def clean_list( self, lst ):
		retlst = []
		for i in lst:
			if i == 'true':
				retlst.append( True )
			elif i == 'false':
				retlst.append( False )
			try:
				retlst.append( int( i ) )
			except:
				try:
					retlst.append( long( i ) )
				except:
					try:
						retlst.append( float( i ) )
					except:
						try:
							retlst.append( complex( i ) )
						except:
							retlst.append( i )
		return retlst
		