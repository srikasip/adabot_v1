from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, create_engine
from sqlalchemy.orm import backref, mapper, relation

BASE = declarative_base()
APPNAME = 'TestApp'

class Color(BASE):
	__tablename__ = 'Color'

	color = Column(String)
	ada_id = Column(Integer, primary_key = True)
	name = Column(String)
	Person = relationship('Person', secondary='PersonColorfavorite_colorslist'))
	

	def __init__(self, color, ada_id, name):
		self.color = color
		self.ada_id = ada_id
		self.name = name
		

	def __repr__(self):
		repr = ''
		repr += 'color: ' + self.color
		repr += 'ada_id: ' + self.ada_id
		repr += 'name: ' + self.name
		
		return repr

class Person(BASE):
	__tablename__ = 'Person'

	favorite_colors = relationship('Color', secondary='PersonColorfavorite_colorslist'))
	age = Column(Integer)
	ada_id = Column(Integer, primary_key = True)
	name = Column(String)
	

	def __init__(self, age, ada_id, name):
		self.age = age
		self.ada_id = ada_id
		self.name = name
		

	def __repr__(self):
		repr = ''
		repr += 'age: ' + self.age
		repr += 'ada_id: ' + self.ada_id
		repr += 'name: ' + self.name
		
		return repr

class PersonColorfavorite_colorslist(BASE):
	__tablename__ = 'PersonColorfavorite_colorslist'

	favorite_colors_id = Column(Integer, ForeignKey('Color.ada_id'))
	Color = relationship(Color, backref=backref('PersonColorfavorite_colorslist'))
	Person_id = Column(Integer, ForeignKey('Person.ada_id'))
	Person = relationship(Person, backref=backref('PersonColorfavorite_colorslist'))
	ada_id = Column(Integer, primary_key = True)
	

	def __init__(self, ada_id):
		self.ada_id = ada_id
		

	def __repr__(self):
		repr = ''
		repr += 'ada_id: ' + self.ada_id
		
		return repr

class ColorhashCodeList(BASE):
	__tablename__ = 'ColorhashCodeList'

	Color_id = Column(Integer, ForeignKey('Color.ada_id'))
	Color = relationship(Color, backref=backref('ColorhashCodeList'))
	ada_id = Column(Integer, primary_key = True)
	hashCode = Column(String)


	def __init__(self, ada_id, hashCode):
		self.ada_id = ada_id
		self.hashCode = hashCode
		

	def __repr__(self):
		repr = ''
		repr += 'ada_id: ' + self.ada_id
		repr += 'hashCode: ' + self.hashCode
		
		return repr


ENGINE = create_engine('sqlite:///adaDB_TestApp.db', echo=False)
BASE.metadata.create_all(ENGINE)

