import Ada_Utilities as au
from sqlalchemy.orm import sessionmaker
from ObjectsFile import Color, Person, ENGINE, BASE, APPNAME

class PersonViews:
  def __init__(self):
    Session = sessionmaker(bind=ENGINE)
    self.session = Session()

  def all_persons(self):
    all_persons = self.session.query(Person).all()
    print all_persons

  

