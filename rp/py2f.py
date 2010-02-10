# -*- coding: utf-8 -*-
#!/usr/bin/python



__doc__ = '''
Reasonable Python
A module for integrating F-logic into Python

py2f.py --- converting Python objects into Flora2 F-molecules

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
	
import re, types
	
from dbms import Objectbase
from persistent import Persistent

class py2f:
	def __init__( self, base=None, insert=False ):
		self.classdefs = []
		self.insert = insert
		self.count = 0
		if self.insert:
			if base == None:
				self.ob = Objectbase( 'p2f.fs' )
			else:
				self.ob = base
		else:
			self.ob = None
				
	def store( self, object ):
		if self.insert:
			try:
				key = self.name( object )
			except:
				raise ValueError, 'Don\'t know how to translate ' + str( object ) + ' to FLORA-2 syntax'
			try:
				self.ob.insert( key, object )
			except:
				self.ob.insert( key, 'unpickable_object' )
				print 'WARNING: inserting unpickable object ' + str( object ) + 'into objectbase'
	
	def delete( self, object ):
		if self.insert:
			try:
				key = self.name( object )
			except:
				raise ValueError, 'Don\'t know how to translate ' + str( object ) + ' to FLORA-2 syntax'
			try:
				self.ob.delete( key )
			except:
				raise ValueError, 'No such object in the object base: ' + str( object )
		
	def translate( self, object ):
		if isinstance( object, types.NoneType ):
			return '_'.replace( '\x00', '' )
		elif isinstance( object, bool ):
			return str( object ).lower().replace( '\x00', '' )
		elif isinstance( object, int ):
			return str( object ).replace( '\x00', '' )
		elif isinstance( object, float ):
			return str( object ).replace( '\x00', '' )
		elif isinstance( object, long ):
			return str( object ).replace( '\x00', '' )
		elif isinstance( object, complex ):
			return '"' + str( object ) + '"'.replace( '\x00', '' )
		elif isinstance( object, str ):
			return '"' + object + '"'.replace( '\x00', '' )
		elif isinstance( object, unicode ):
			return '"' + object + '"'.replace( '\x00', '' )
		elif isinstance( object, types.BufferType ):
			return '"' + str( object ) + '":pybuffer'.replace( '\x00', '' )
		elif isinstance( object, types.BuiltinFunctionType ):
			return '"' + str( object ) + '":pybuiltinfunction'.replace( '\x00', '' )
		elif isinstance( object, types.BuiltinMethodType ):
			return '"' + str( object ) + '":pybuiltinmethod'.replace( '\x00', '' )
		elif isinstance( object, types.CodeType ):
			return '"' + str( object ) + '":pycode'.replace( '\x00', '' )
		elif isinstance( object, types.DictProxyType ):
			return '"' + str( object ) + '":pydictproxy'.replace( '\x00', '' )
		elif isinstance( object, types.EllipsisType ):
			return '"' + str( object ) + '":pyellipsis'.replace( '\x00', '' )
		elif isinstance( object, types.FileType ):
			return '"' + str( object ) + '":pyfile'.replace( '\x00', '' )
		elif isinstance( object, types.FrameType ):
			return '"' + str( object ) + '":pyframe'.replace( '\x00', '' )
		elif isinstance( object, types.FunctionType ):
			return '"' + str( object ) + '":pyfunction'.replace( '\x00', '' )
		elif isinstance( object, types.GeneratorType ):
			return '"' + str( object ) + '":pygenerator'.replace( '\x00', '' )
		elif isinstance( object, types.LambdaType ):
			return '"' + str( object ) + '":pylambda'.replace( '\x00', '' )
		elif isinstance( object, types.MethodType ):
			return '"' + str( object ) + '":pymethod'.replace( '\x00', '' )
		elif isinstance( object, types.NotImplementedType ):
			return '"' + str( object ) + '":pynotimplemented'.replace( '\x00', '' )
		elif isinstance( object, types.SliceType ):
			return '"' + str( object ) + '":pyslice'.replace( '\x00', '' )
		elif isinstance( object, types.TracebackType ):
			return '"' + str( object ) + '":pytraceback'.replace( '\x00', '' )
		elif isinstance( object, types.UnboundMethodType ):
			return '"' + str( object ) + '":pyunboundmethod'.replace( '\x00', '' )
		elif isinstance( object, types.XRangeType ):
			return '"' + str( object ) + '":pyxrange'.replace( '\x00', '' )
		elif isinstance( object, list ):
			retstr = '['
			ok = False
			for i in object:
				if self.insert:
					key = self.name( i )				
					if self.ob.root.has_key( key ):
						retstr += key + ', '
					else:
						retstr += self.translate( i ) + ', '
				else:
					retstr += self.translate( i ) + ', '
				ok = True
			if not ok:
				return '[]:list'.replace( '\x00', '' )
			retstr = retstr[ :-2 ]
			retstr += ']:list'
			return retstr.replace( '\x00', '' )
		elif isinstance( object, tuple ):
			retstr = '['
			ok = False
			for i in object:
				if self.insert:
					key = self.name( i )
					if self.ob.root.has_key( key ):
						retstr += key + ', '
					else:
						retstr += self.translate( i ) + ', '
				else:
					retstr += self.translate( i ) + ', '
				ok = True
			if not ok:
				return '[]:tuple'.replace( '\x00', '' )
			retstr = retstr[ :-2 ]
			retstr += ']:tuple'
			return retstr.replace( '\x00', '' )
		elif isinstance( object, dict ):
			retstr = '_:dict['			
			ok = False
			for i in object.keys():
				if self.insert:
					key = self.name( i )
					val = self.name( object[ i ] )
					if self.ob.root.has_key( key ):
						retstr += key + '->'
					else:
						retstr += self.translate( i ) + '->'
					if self.ob.root.has_key( val ):
						retstr += val + ', '
					else:
						retstr += self.translate( object[ i ] ) + ', '
				else:					
					retstr += self.translate( i ) + '->'
					retstr += self.translate( object[ i ] ) + ', '
				ok = True
			if not ok:
				return '_:dict'.replace( '\x00', '' )
			retstr = retstr[ :-2 ]
			retstr += ']'
			return retstr.replace( '\x00', '' )
		elif isinstance( object, types.ClassType ) or isinstance( object, types.TypeType ):
			retstr = self.name( object )
			retstr += '['
			ok = False
			for i in dir( object ):
				if self.insert:
					key = self.name( i )
					val = self.name( eval( 'object.' + i ) )
					if self.ob.root.has_key( key ):
						retstr += key + '->'
					else:
						vv = self.translate( i )
						retstr += vv + '->'
					if self.ob.root.has_key( val ):
						retstr += val + ', '
					else:
						kk = self.translate( eval( 'object.' + i )  )
						retstr += kk + ', '
					if self.ob.root.has_key( key ):
						retstr += key + '=>'
					else:
						retstr += vv + '=>'
					if self.ob.root.has_key( val ):
						retstr += val + ', '
					else:
						retstr += kk + ', '
				else:
					t_i = self.translate( i )
					v_i = self.translate( eval( 'object.' + i ) )
					retstr += t_i + '=>'
					retstr += v_i + ', '
					retstr += t_i + '->'
					retstr += v_i + ', '
				ok = True
			if not ok:
				return retstr[ :-1 ].replace( '\x00', '' )
			retstr = retstr[ :-2 ]
			retstr += ']'
			if retstr not in self.classdefs:
				self.classdefs.append( retstr )
			return retstr.replace( '\x00', '' )
		elif isinstance( object, types.ObjectType ) or isinstance( object, types.InstanceType ):
			clname = self.name( object.__class__ )
			if clname not in self.classdefs:
				self.classdefs.append( clname )
			retstr = self.name( object )
			retstr += ':' + clname + '['
			ok = False
			for i in dir( object ):
				if i[ :1 ] != '_' and i[ :-2 ] != '__' :
					if self.insert:
						key = self.name( i )
						val = self.name( eval( 'object.' + i ) )
						if self.ob.root.has_key( key ):
							retstr += key + '->'
						else:
							vv = self.translate( i )
							retstr += vv + '->'
						if self.ob.root.has_key( val ):
							retstr += val + ', '
						else:
							kk = self.translate( eval( 'object.' + i )  )
							retstr += kk + ', '
					else:
						retstr += self.translate( i ) + '->'
						retstr += self.translate( eval( 'object.' + i ) ) + ', '
					ok = True
			if not ok:
				return retstr[ :-1 ].replace( '\x00', '' )
			retstr = retstr[ :-2 ]
			retstr += ']'
			return retstr.replace( '\x00', '' )
		elif isinstance( object, types.ModuleType ):
			retstr = self.name( object ) + '['
			ok = False
			for i in dir( object ):
				if self.insert:
					key = self.name( i )
					val = self.name( eval( 'object.' + i ) )
					if self.ob.root.has_key( key ):
						retstr += key + '->'
					else:
						vv = self.translate( i )
						retstr += vv + '->'
					if self.ob.root.has_key( val ):
						retstr += val + ', '
					else:
						kk = self.translate( eval( 'object.' + i )  )
						retstr += kk + ', '
				else:
					retstr += self.translate( i ) + '->'
					retstr += self.translate( eval( 'object.' + i ) ) + ', '
				ok = True
			if not ok:
				return retstr[ :-1 ].replace( '\x00', '' )
			retstr = retstr[ :-2 ]
			retstr += ']'
			return retstr.replace( '\x00', '' )
		else:
			retstr = self.translate( str( object ) ) + ':pyunknown'
			return retstr.replace( '\x00', '' )
	
	def name( self, object ):		
		if isinstance( object, types.NoneType ):
			return '_'.replace( '\x00', '' )
		elif isinstance( object, bool ):
			return str( object ).lower().replace( '\x00', '' )
		elif isinstance( object, int ):
			return str( object ).replace( '\x00', '' )
		elif isinstance( object, float ):
			return str( object ).replace( '\x00', '' )
		elif isinstance( object, long ):
			return str( object ).replace( '\x00', '' )
		elif isinstance( object, complex ):
			return '"' + str( object ) + '"'.replace( '\x00', '' )
		elif isinstance( object, str ):
			return '"' + object + '"'.replace( '\x00', '' )
		elif isinstance( object, unicode ):
			return '"' + object + '"'.replace( '\x00', '' )
		elif isinstance( object, types.ModuleType ):
			return 'pymodule' + self.findname( object )	
		elif isinstance( object, types.ClassType ):
			return 'pyclass' + self.findname( object )
		elif isinstance( object, types.TypeType ):
			return 'pytype' + self.findname( object )
		elif isinstance( object, types.ObjectType ):
			return 'pyobject' + self.findname( object )
		elif isinstance( object, types.InstanceType ):
			return 'pyinstance' + self.findname( object )
		else:
			return self.translate( object )
		
	def findname( self, object ):
		retstr = ''
		x = []
		for i in str( object ).split( '.' ):
			x += i.split()
		y = []
		for i in x:
			a = i.replace( '<', '' )
			a = a.replace( '>', '' )
			a = a.replace( '"', '' )
			a = a.replace( '\'', '' )
			a = a.replace( '/', 'xxxmarexxx' )
			a = a.replace( '\\', '' )
			
			y.append( a )
		
		for i in y:
			retstr += 'xxxmarexxx' + i

		return retstr
	
if __name__ == '__main__':
	pf = py2f()
	
	a = 1
	b = 1.0
	c = True
	d = "Wazaaap"
	e = [ a, b, 3, 4, d ]
	f = ( 1, 2, b, c, e )
	g = { a:b, c:d, d:f }
	
	class h:
		'''
		A little funny class
		'''
		def __init__( self, i, j ):
			self.i = i
			self.j = j
			
	k = h( e, f )
	
	l = re
	
	test = [ a, b, c, d, e, f, g, h, k, l ]
	
	for i in test:
		print 'translating: ' + str( i )
		print pf.translate( i ) + '\n'
	
	for i in pf.classdefs:
		print i
	