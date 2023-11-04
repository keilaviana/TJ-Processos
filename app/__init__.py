from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# adicionar usuário e senha na string connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:senha@localhost/db_solicitacoes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from app.models.solicitacoes import Solicitacoes