# -*- coding: utf-8 -*-
#!/usr/bin/python

__doc__ = '''
Reasonable Python
A module for integrating F-logic into Python
	
interface.py --- interface to XSB anf Flora-2
	
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

from xsb_swig.xsb import *
try:
	from libs import *
except:
	print 'Don\'t know where XSB and Flora-2 are but will proceed as requested'
	xsb_home = ''
	flora2_home = ''


class xsb:
	def __init__( self, args=[ xsb_home, '-n' ] ):
		lenght = len( args )
		array = create_string_array( lenght )
		
		i = 0
		for arg in args:
			array = assign_string( array, arg, i )
			i += 1
		
		#print_string_array( array, lenght )
		
		xsb_init( lenght, array )
		
		release_string_array( array, lenght )
	
	def consult( self, file_name ):
		xsb_query_string( 'consult('+file_name+').' )
		xsb_close_query()
	
	def query( self, query ): # add vars to be returned
		xsb_query_string( query )
	
	def close_query( self ):
		xsb_close_query()
	
	def next( self ):
		xsb_next()
	
	def term2string( self, term ):
		termstring = ''
		if is_var( term ) > 0:
			return '_' + str( term )
		elif is_int( term ) > 0:
			return str( p2c_int( term ) )
		elif is_float( term ) > 0:
			return str (p2c_float( term ) )
		elif is_nil( term ) > 0 :
			return str( [] )
		elif is_string( term ) > 0:
			return p2c_string( term )
		elif is_list( term ) > 0:
			save_term = term
			termstring +=  '['
			termstring += self.term2string( p2p_car( term ) )
			li = []
			li.append( self.term2string( p2p_car( term ) ) )
			term = p2p_cdr( term )
			while is_list( term ) > 0:
				termstring += ', '
				termstring += self.term2string( p2p_car( term ) )
				li.append( self.term2string( p2p_car( term ) ) )
				term = p2p_cdr( term )
			if not is_nil( term ) > 0:
				termstring += '|'
				termstring += self.term2string( term )
			termstring += ']'
			if is_charlist( save_term, intpointer( len( li ) ) ) > 0:
				return pcharlist2string( save_term, len( li ) )
			return termstring
		elif is_functor( term ):
			termstring += p2c_functor( term )
			if p2c_arity( term ) > 0:
				termstring += '('
				termstring += self.term2string( p2p_arg( term, 1 ) )
				arity = p2c_arity( term )
				for i in range( 2, arity ):
					termstring += ', '
					termstring += self.term2string( p2p_arg( term, i ) )
				termstring += ')'
				return termstring
		else:
			raise ValueError, 'Unrecognized term type at:' + termstring
	
	def get_ret_args( self, term ):
		if is_functor( term > 0 ):
			if p2c_functor( term ) == 'ret':
				arity = p2c_arity( term )
				args = []
				for i in range ( 1, arity ):
					args.append( self.term2string( p2p_arg( term, i ) ) )
				return args
			else:
				raise ValueError, 'Functor is not of type \'ret\''
		else:
			raise ValueError, 'Term is not a functor.'
		
class Flora2( xsb ):
	def __init__( self, args=[ xsb_home, '-n', '-m', '100000', '-c', '20000', '-e', 
'asserta(library_directory(\'' + flora2_home + '\')). [flora2]. bootstrap_flora.' ] ):
		xsb.__init__( self, args )
	
	def consult( self, file_name ):
		xsb.query( self, "flora_query('[+" + file_name + "].',[],_,_)." )
		xsb.close_query( self )
	
	def query( self, query, var_list ): # add vars to be returned
		if var_list != []:
			mapping = '['
			for i in var_list:
				mapping += "'?" + i + "' = " + i + "1,"
				
			
			mapping = mapping[ :-1 ] + "]"
		else:
			mapping = '[]'
		xsb.query( self, "flora_query('" + query + "'," + mapping + ",_,_)." )
		
		ans = ' '
		
		answer = []
		
		while ans[ 0 ] != '_':
			ans = self.term2string( reg_term( 2 ) )
			if ans[ 0 ] == '_':
				break
			
			args = self.get_ret_args( reg_term( 2 ) )
			args = args[ :-1 ]
			
			answer.append( dict( zip( var_list, args ) ) )
				
			self.next()
		
		return answer
				
		
flArgs = [ xsb_home, '-n', '-m', '100000', '-c', '20000', '-e', 
'asserta(library_directory(" + flora2_home + ")). [flora2]. bootstrap_flora.' ] #flora_shell.

if __name__ == '__main__':
	
	#x = xsb( flArgs )
	#x.consult( 'fammily' )
	#x.query( 'predak( X, lara ),writeln( X ).' )
	#x.query( "flora_query('flLoad(test).',[],A,B), write('A = '), writeln(A), nl, write('B = '), write(B)." )
	#x.close_query()
	#x.query( "flora_query('X[ a -> 10 ].',['X' = Xa],A,B), writeln('Xa ='), writeln(Xa), writeln(A), writeln(B)." )
	#for i in range( 6 ):
	#	x.next()
	#x.close_query()
	f = Flora2()
	f.consult( 'mybase_new' )
	ans = f.query( "X:Z[ Y -> S ].", ['X', 'Z', 'Y', 'S'] ) # OVO RADI
	print ans
