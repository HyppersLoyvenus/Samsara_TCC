from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os
load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #evitar que toda vez que houver uma modificação ficar checando 

BancoDeDados = SQLAlchemy(app)
migrate = Migrate(app, BancoDeDados)
bcrypt = Bcrypt(app)

from app.routes import homepage
from app.models import LancamentoFinanceiro