from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

from flaskr.models.map import Block
def getQeustion():
	question = Block.query.filter_by(file='question.jpg').first()
	return question.file