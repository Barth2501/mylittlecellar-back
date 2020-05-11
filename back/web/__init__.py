from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from.encoder import NpEncoder
import os

app = Flask('mylittlecellar')
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = 'test'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
app.config['RESTFUL_JSON'] = {'cls': NpEncoder}
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

load_dotenv()

from . import api
from . import auth