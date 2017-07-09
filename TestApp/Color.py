import Ada_Utilities as au
from sqlalchemy.orm import sessionmaker, session
from ObjectsFile import Color, Person, ENGINE, BASE, APPNAME
class ColorController:
	def __init__(self):
		self.session = sessionmaker(bind=ENGINE)
	def selectAll(self):
		allColor = self.session.query(Color).all()
		return allColor
	def selectbyID(self, send_id):
		oneColor = self.session.query(Color).filter(Color.ada_id == send_id)
		return oneColor
	def selectbyID(self, send_id):
		oneColor = self.session.query(Color).filter(Color.ada_id == send_id).delete()
		self.session.commit()
