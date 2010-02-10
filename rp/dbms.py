# -*- coding: utf-8 -*-
#!/usr/bin/python

__doc__ = '''
Reasonable Python
A module for integrating F-logic into Python
	
dbms.py --- easy interface to ZODB
	
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

import ZODB
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction

class Objectbase:
	'''
		Class Objectbase - interface to an object database
	'''
	def __init__( self, dbfile = None ):
		'''
			Initializes the connection to the database located in 'dbfile'. If 
			'dbfile' not supplied, only initalizes and sets opened to False. If 
			database does not exist, creates a new one with the name 'dbfile'
		'''
		if dbfile:
			self.st     = FileStorage( dbfile )
			self.db     = DB( self.st )
			self.cn     = self.db.open()
			self.root   = self.cn.root()
			self.opened = True
		else:
			self.opened = False
			
	def selectByName( self, name ):
		'''
			Returns the object with the key name. If database doesn't contain such an
			object raises ValueError
		'''
		if self.opened:
			if self.root[ name ]:
				return self.root[ name ]
			else:
				error = 'This database has no object with the name ' + name
				raise ValueError, error
		else:
			error = 'Database is closed'
			raise ValueError, error

	def selectByType( self, typ ):
		'''
			Searches the database for a given type and returns a dictionary with
			key:object pairs which match this type. If database doesn't contain any
			object of the given type, returns an empty dictionary.
		'''
		if self.opened:
			objects = {}
			for i in self.root:
				if issubclass( type( self.root[ i ] ), typ ):
					objects[ i ] = self.root[ i ]
			return objects
		else:
			error = 'Database is closed'
			raise ValueError, error
		
	def delete( self, name, cascade = False ):
		'''
			Deletes an object from the database by it's key (name). If database 
			doesn't contain such an object raises ValueError. Parameter cascade is
			used (if True) to delete all relations of this object in other objects.
			Cascade option is not well implemented since it does not roll back the 
			transaction if somewhere in the process an error is raised (e.g. if
			a '1' side of a 1:1 or 1:N relation is being tried to remove). Use it only
			if the object you try to remove does not engage 1:1 relations or is the 
			'1' side of a 1:N relation.
		'''
		error = ''
		if self.opened:
			try:
				if not cascade:
					if False: # NOTE implement a way to check if a object has relations to other objects
						error = 'This object has relations to other objects in the objectbase'
						raise ValueError, error
					else:
						del self.root[ name ]
				else:
					for i in self.root[ name ].relations:
						for j in i[ 0 ]:
							j.removeRelation( self.root[ name ] )
					del self.root[ name ]
			except:
				if error == '':
					error = 'This database has no object with the name ' + name
				print error
				raise ValueError, error
		else:
			error = 'Database is closed'
			raise ValueError, error
	
	def update( self, name, object ):
		'''
			Updates the object with the key 'name' to match the value of 'object'. If
			database doesn't contain such an object raises ValueError. It also raises
			a ValueError if the object is not a subclass of the original object in the
			database.
		'''
		if self.opened:
			try:
				if issubclass( type( self.root[ name ] ), type( object ) ):
					del self.root[ name ]
					self.root[ name ] = object
				else:
					error = 'You cannot change the type of the object ' + name + ' to ' + str( type( object ) )
					raise ValueError, error
			except:
				error = 'This database has no object with the name ' + name
				raise ValueError, error
		else:
			error = 'Database is closed'
			raise ValueError, error
	
	def insert( self, name, object ):
		'''
			Inserts a new object with the key 'name' to the database.
		'''
		if self.opened:
			self.root[ name ] = object
		else:
			error = 'Database is closed'
			raise ValueError, error
	
	def close( self ):
		'''
			Closes the database.
		'''
		if self.opened:
			transaction.commit()
			self.cn.close()
			self.db.close()
			self.st.close()
			self.opened = False
		else:
			error = 'Database is allready closed'
			raise ValueError, error
		
	def open( self, dbfile ):
		'''
			Opens a database stored in 'dbfile' or creates a new one.
		'''
		if not self.opened:
			self.st     = FileStorage( dbfile )
			self.db     = DB( self.st )
			self.cn     = self.db.open()
			self.root   = self.cn.root()
			self.opened = True		
		else:
			error = 'Database is allready open'
			raise ValueError, error
