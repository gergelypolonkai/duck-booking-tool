from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Duck( Base ):
    __tablename__ = 'users'

    duck_id = Column( Integer, primary_key=True )
    name = Column( String )
    color = Column( String )

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)
