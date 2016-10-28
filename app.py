#!/usr/bin/env python3

import os
import connexion
import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

import models

engine = create_engine( os.environ.get( 'DATABASE_URL', 'sqlite:///:memory:' ), echo=True )

Base.metadata.create_all( engine )

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml',
            arguments={
                'title': 'Rubber Duck Booking Tool'
            })

if __name__ == '__main__':
    app.run(port=8080)
