# -*- coding: utf-8 -*-
#!/usr/bin/python

__doc__ = '''
Reasonable Python
A module for integrating F-logic into Python
	
f.py --- F-logic concepts (rule, query, fact, variable )
	
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

from persistent import Persistent
import string

from py2f import py2f



class Construct:
	'''
        Three possibilities of logical constructs:

        a) h :- b.
        b) _ :- b.
        c) h :- _.

        a) is a rule where h is the head and b is the body (denoted by h :- b. )
        b) is a query where b is the query body (denoted by ?- b. )
        c) is a fact which consists of b (denoted by b. )


	'''

	def __init__( self ):
		'''
			Initializes the logical construct
		'''
		self.head = Formula()
		self.body = Formula()
	
	def __lshift__( self, body ):
		'''
			Adds a formula to the body of the construct.
		'''
		self.body & body
		self.__str__()
		return self.body
	
	def __and__( self, new ):
		'''
			Adds a formula to the head of the construct 
			using the logic operator and (&).
		'''
		self.head & new
		self.__str__()
		return self
		
	def __or__( self, new ):
                '''
                        Adds a formula to the head of the construct
                        using the logic operator or (|).
                '''

		self.head | new
		self.__str__()
		return self
	
	
	def __str__( self ):
                '''
                        Prints the construct
                '''

		has_head = False
		has_body = False
		s = ''
		if self.head.content != []:
			s += str( self.head )
			has_head = True
			self.__class__ = Fact
		if self.body.content != []:
			has_body = True
			if has_head:
				s +=  ' :- ' + str( self.body )
				self.__class__ = Rule
			else:
				s +=  ' ?- ' + str( self.body )
				self.__class__ = Query
		if has_head or has_body:
			s += '.'
		return s

class Rule( Construct ): pass
class Fact( Construct ): pass
class Query( Construct ): pass

class Formula:
	'''
        	Class used for building logical constructs.
        '''

	def __init__( self, first=None ):
		self.content = []
		if first != None:
			self.content.append( first )
	
	def __and__( self, new ):
		if self.content != []:
			self.content.append( '__and__' )
		
		if issubclass( new.__class__, Logical ):
			if len( new.content ) > 1:
				self.content.append( '(' )
			for i in new.content:
				self.content.append( i )
			if len( new.content ) > 1:
				self.content.append( ')' )
			#print 'Logical class detected'
		else:
			self.content.append( new )

		# print 'Anded', str( new )
		return self
		
	def __or__( self, new ):
		if self.content != []:
			self.content.append( '__or__' )
		if issubclass( new.__class__, Logical ):
			if len( new.content ) > 1:
				self.content.append( '(' )
			for i in new.content:
				self.content.append( i )
			if len( new.content ) > 1:
				self.content.append( ')' )

			#print 'Logical class detected'
		else:
			self.content.append( new )
		# print 'Ored', str( new )
		return self
		
	def __str__( self ):
		s = ''
		for i in self.content:
			if i == '__and__':
				s += ', '
			elif i == '__or__':
				s += '; '
			elif i == '(':
				s += '('
			elif i == ')':
				s += ')'
			else:
				if isinstance( i, Logical ):
					s += i.__fstr__()
				else:
					pf = py2f()
					s += pf.translate( i )
		return s

class Logical( Persistent ):
	'''
		Class used for building logical queries.
	'''
	def __init__( self ):
		self.content = [ self ]
		self.__type__ = None
		self.__classtype__ = None
	
	def __and__( self, new ):
		if self.content != []:
			self.content.append( '__and__' )
		self.content.append( new )
		return self

	def __or__( self, new ):
		if self.content != []:
			self.content.append( '__or__' )
		self.content.append( new )
		return self
	
	def __fstr__( self ):
		pf = py2f()
		if issubclass( self.__type__.__class__, Variable ) or issubclass( self.__type__.__class__, str ):
			fs = str( self.__type__ )
		else:
			fs = pf.name( self )
		if not issubclass( self.__classtype__.__class__, Variable ):
			fs += ':' + pf.name( self.__class__ ) + '['
		else:
			fs += ':' + str( self.__classtype__ ) + '[ '
		for i in self.__dict__.keys():
			if i != 'content' and i != '__type__' and i != '__classtype__':
				if not ( isinstance( self.__dict__[ i ], Variable ) ):
					if isinstance( i, Variable ):
						fs += str( i ) + '->' + pf.translate( self.__dict__[ i ] ) + ', '
					else:
						fs += '"' + str( i ) + '"' + '->' + pf.translate( self.__dict__[ i ] ) + ', '
				else:
					if isinstance( i, Variable ):
						fs += str( i ) + '->' + str( self.__dict__[ i ] ) + ', '
					else:
						fs += '"' + str( i ) + '"' + '->' + str( self.__dict__[ i ] ) + ', '

		if fs[ -2 ] != '[':
			fs = fs[ :-2 ] + ']'
		else:
			fs = fs[ :-2 ]
		
		return fs
				
				
	

class Variable( Persistent ):
	'''
		Implementation of logical variables in Python.
	'''
	def __init__( self, name ):
		if not( name[ 0 ] in string.uppercase or name[ 0 ] == '_' ):
			raise ValueError, 'Logical variables have to start with uppercase or \'_\' if they are (named) don\'t care variables.'
		else:
			self.name = name
		
		self.value = None
		
	def __str__( self ):
		if self.value == None:
			return self.name
		else:
			return self.name + ' = ' + str( self.value )
	
	def bind( self, value ):
		self.value = value
		
	def __eq__( self, value ):
		self.value = value

class Bogus( Logical ):
	'''
		Bogus testing class. Ignore!
	'''
	def __init__( self, a=1, b=[ 2, 3 ] ):
		Logical.__init__( self )
		self.a = a
		self.b = b


if __name__ == '__main__':
			
	x = Construct()
	
	X = Variable( 'X' )
	
	h = Bogus( X )
	b1 = Bogus()
	b2 = Bogus()
	
	
	pf = py2f()
	
	print pf.name( h )
	
	( x & h ) 
	# x << b1 & b2
	
	print x
	
	
