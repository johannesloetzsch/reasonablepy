# -*- coding: utf-8 -*-
#!/usr/bin/python



__doc__ = '''
Reasonable Python
A module for integrating F-logic into Python
	
reasonable.py --- creates interface to FBase
	
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

from dbms import Objectbase
from interface import Flora2
from f import *
from py2f import py2f
from f2py import f2py

class FBase:
	def __init__( self, filename ):
		self.fn = filename
		ob = Objectbase( self.fn + '.fs' )		
		self.db = py2f( ob, True )
		self.bd = f2py()
		self.f2 = Flora2()
		self.ffa = open( self.fn + '_all.flr', 'ar' )
		
		self.listquery = Construct()
		Type = Variable('Type')
		self.qw = Logical()
		self.qw.__classtype__ = Type
		self.listquery << self.qw
		self.indicator = False
	
	def write_and_load( self, string ):
		self.ffa.write( string + '\n' )
		self.ffa.flush()
		
		string = string.replace( '\x00', '' )
		
		self.f2.query( 'insert{ ' + string[ :-1 ] + '}.', [])
		self.f2.close_query()
		
		
	
	def insert( self, object ):
		if issubclass( object.__class__, Logical ) or issubclass( object.__class__, Variable ) or issubclass( object.__class__, Formula ):
			raise ValueError, 'Only Constructs and non-logical objects can be inserted into the FBase.\n' + str( object )
		if issubclass( object.__class__, Construct ):
			if issubclass( object.__class__, Fact ):
				self.write_and_load( str( object ) )
				self.db.store( object )
			elif issubclass( object.__class__, Rule ):
				self.db.store( object )
				self.write_and_load( str( object ) )
			elif issubclass( object.__class__, Query ):
				raise ValueError, 'Provided object to insert is a query.\n' + str( object )
			else:
				raise ValueError, 'Construct empty. Nothing to insert.'
		else:
			self.write_and_load( self.db.translate( object ) + '.' )
			self.db.store( object )
				
	def delete( self, object ):
		if issubclass( object.__class__, Logical ) or issubclass( object.__class__, Variable ) or issubclass( object.__class__, Formula ):
			raise ValueError, 'Only Constructs and non-logical objects can be deleted from the FBase.\n' + str( object )
		if issubclass( object.__class__, Construct ):
			if issubclass( object.__class__, Fact ):
				self.f2.query( 'deleteall{' + self.db.translate( object ) + '}.', [] )
				self.f2.close_query()
				self.db.delete( object )
			elif issubclass( object.__class__, Rule ):
				raise ValueError, 'Rules cannot be deleted from the FBase.\n' + str( object )
			elif issubclass( object.__class__, Query ):
				raise ValueError, 'Provided object to delete is a query.\n' + str( object )
			else:
				raise ValueError, 'Construct empty, nothing to delete.'
		else:
			self.f2.query( 'deleteall{ ' + self.db.translate( object ) + ' }.', [] )
			self.db.delete( object )
			self.f2.close_query()
		
				
	def query( self, query, gl ):
		if issubclass( query.__class__, Query ):
			vars = []
			for i in query.body.content:
				if not isinstance( i, str ):
					for j in i.__dict__:
						if issubclass( i.__dict__[ j ].__class__, Variable ) and str( i.__dict__[ j ] ) not in vars:
							vars.append( str( i.__dict__[ j ] ) )
			results = self.f2.query( str( query )[ 4: ], vars )
			self.f2.close_query()
			res = []
			for i in results:
				ri = {}
				for j in i.keys():
					try:
						ri[ j ] = self.db.ob.root[ i[ j ] ]
					except:
						if j[ 0 ] != '_':
							if i[ j ][ :2 ] == 'py':
								ri[ j ] = self.bd.translate( i[ j ], gl )
							elif i[ j ][ 0 ] == '[' and not self.indicator:
								self.indicator = True
								self.qw.__type__ = Variable( j )
								query << self.qw
								resu = self.query( query, gl )
								typ = resu[ results.index( i ) ][ 'Type' ]
								lst = i[ j ][ 1:-1 ].split( ',' )
								
								lst = self.bd.clean_list( lst )
								
								if typ == 'list':
									ri[ j ] = lst
								elif typ == 'tuple':
									ri[ j ] = tuple( lst )
								self.indicator = False
							else:
								ri[ j ] = i[ j ]
				res.append( ri )
			
			return res
				
		

if __name__ == '__main__':
	fb = FBase( 'mybase' )
	
	x = Construct()
	y = Construct()
	
	Y = Variable( 'Y' )
	X = Variable( 'E' )
	Z = Variable( 'Z' )
	D = Variable( 'D' )
	
	h = Bogus()
	b1 = Bogus( 1, 2 )
	b1.__type__ = Z
	b1.__classtype__ = X
	b2 = Bogus()
	
	#x << h
	
	y & h
	
	x << b1 
	
	print x
	
	class mali( Persistent ):
		def __init__( self, a=1, b=2 ):
			self.a = a
			self.b = b
			
	
	c = mali()
	d = mali()
	e = mali()
		
	#print x
	fb.insert( c )
	fb.insert( d )
	fb.insert( e )
	
	
	
	
	fb.delete( c )
	
	result = fb.query( x, globals() )
	
	print result
	
	
