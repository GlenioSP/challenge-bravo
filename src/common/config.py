from os import getenv
from flask import Flask
from dotenv import load_dotenv
from mongoengine import connect

from exception import global_exception_handler

load_dotenv()

mongodb_uri = getenv("MONGODB_URI")

connect(db=f"bravo", host=mongodb_uri)

app = Flask(__name__)

global_exception_handler(app)
