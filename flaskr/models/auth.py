from flaskr.shared import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, nullable=False, unique=True)
	password = db.Column(db.Text, nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.setPassword(password)

	def setPassword(self, password):
		self.password = generate_password_hash(password)
	
	def checkPassword(self, password):
		return check_password_hash(self.password, password)