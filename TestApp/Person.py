import Ada_Utilities as au
from sqlalchemy.orm import sessionmaker, session
from ObjectsFile import Color, Person, ENGINE, BASE, APPNAME

class PersonController:
	def __init__(self):
		self.session = sessionmaker(bind=ENGINE)
	def selectAll(self):
		allPerson = self.session.query(Person).all()
		return allPerson
	def selectbyID(self, send_id):
		onePerson = self.session.query(Person).filter(Person.ada_id == send_id)
		return onePerson
	def selectbyID(self, send_id):
		onePerson = self.session.query(Person).filter(Person.ada_id == send_id).delete()
		self.session.commit()
