from flask import Flask, request
from flask_restful import Resource, Api

from models import Duck

#app =
def ducks_get():
    return 'do some magic!'

def duck_get( duck_id ):
    return 'do some duck magic!'

def duck_post( name, color ):
    new_duck = Duck( name, color )
    return new_duck
