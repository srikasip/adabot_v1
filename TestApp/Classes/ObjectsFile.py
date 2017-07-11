from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, create_engine
from sqlalchemy.orm import backref, mapper, relation

BASE = declarative_base()
APPNAME = 'TestApp'

class ColorhashCodeList(BASE):
	__tablename__ = '__colorhashcodelist__'

	hashCode = Column(String)
	ada_id = Column(Integer, primary_key = True)
	Color_id = Column(Integer, ForeignKey('__color__.ada_id'))
	Color = relation(Color, backref=backref('ColorhashCodeList'))
	

	def __init__(self, hashCode, ada_id):
		self.hashCode = hashCode
		self.ada_id = ada_id
		

	def __repr__(self):
		repr = ''
		repr += 'hashCode: ' + self.hashCode
		repr += 'ada_id: ' + self.ada_id
		
		return repr

class Color(BASE):
	__tablename__ = '__color__'

	name = Column(String)
	color = Column(String)
	ada_id = Column(Integer, primary_key = True)
	

	def __init__(self, name, color, ada_id):
		self.name = name
		self.color = color
		self.ada_id = ada_id
		

	def __repr__(self):
		repr = ''
		repr += 'name: ' + self.name
		repr += 'color: ' + self.color
		repr += 'ada_id: ' + self.ada_id
		
		return repr

class PersonColorfavorite_colorslist(BASE):
	__tablename__ = '__personcolorfavorite_colorslist__'

	favorite_colors_id = Column(Integer, ForeignKey('__color__.ada_id'))
	Color = relation(Color, backref=backref('PersonColorfavorite_colorslist'))
	ada_id = Column(Integer, primary_key = True)
	Person_id = Column(Integer, ForeignKey('__person__.ada_id'))
	Person = relation(Person, backref=backref('PersonColorfavorite_colorslist'))
	

	def __init__(self, ada_id):
		self.ada_id = ada_id
		

	def __repr__(self):
		repr = ''
		repr += 'ada_id: ' + self.ada_id
		
		return repr

class Person(BASE):
	__tablename__ = '__person__'

	name = Column(String)
	age = Column(Integer)
	ada_id = Column(Integer, primary_key = True)
	favorite_colors = relation('Color', secondary='__personcolorfavorite_colorslist__')
	

	def __init__(self, name, age, ada_id):
		self.name = name
		self.age = age
		self.ada_id = ada_id
		

	def __repr__(self):
		repr = ''
		repr += 'name: ' + self.name
		repr += 'age: ' + self.age
		repr += 'ada_id: ' + self.ada_id
		
		return repr


ENGINE = create_engine('sqlite:///adaDB_TestApp.db', echo=False)
BASE.metadata.create_all(ENGINE)

