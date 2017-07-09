from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

def main():
  db = create_engine('sqlite:///tutorial.db')

  db.echo = True  # Try changing this to True and see what happens

  base = declarative_base()
  metadata = base.metadata

  #base.metadata.create_all(db)
  #metadata.create_all(bind=db)
  users = Table('users', metadata,
      Column('user_id', Integer, primary_key=True),
      Column('name', String(40)),
      Column('age', Integer),
      Column('password', String),
  )

  # users.create(bind=db, checkfirst=True)

  # i = users.insert(bind=db)
  # i.execute(name='Mary', age=30, password='secret')
  # i.execute({'name': 'John', 'age': 42},
  #           {'name': 'Susan', 'age': 57},
  #           {'name': 'Carl', 'age': 33})

  s = users.select(bind=db)
  rs = s.execute()

  #row = rs.fetchone()
  # print 'Id:', row[0]
  # print 'Name:', row['name']
  # print 'Age:', row.age
  # print 'Password:', row[users.c.password]

  for row in rs:
    print row
    #print row.name, 'is', row.age, 'years old'
  print metadata

if __name__ == "__main__": main()