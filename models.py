import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
#from flask.ext.login import UserMixin
#from sqlalchemy_login_models.model import Base, UserKey, User as SLM_User

__all__ = ['Duck']

Base = declarative_base()

class Duck( Base ):
    __tablename__ = 'duck'
    __name__ = "duck"

    duck_id = sa.Column( sa.Integer, primary_key=True )
    name = sa.Column( sa.String )
    color = sa.Column( sa.String )

    def __repr__(self):
        return '{"duck_id": "'+ ( str( self.duck_id ) or '0' ) +'", "name": "'+ self.name +'", "color": "'+ self.color +'" }'

    def __init__(self, name, color):
        self.name = name
        self.color = color
