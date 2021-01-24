from flaskr.shared import db

class Block(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	file = db.Column(db.Text, nullable=False)
	mapBlocks = db.relationship('MapBlock', backref=db.backref('block', lazy=False), cascade='all, delete-orphan')

	def __init__(self, file):
		self.file = file

class Map(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime, default=db.func.now())
	title = db.Column(db.Text, nullable=False)
	width = db.Column(db.Integer, default=7)
	height = db.Column(db.Integer, default=200)
	mapBlocks = db.relationship('MapBlock', backref='map', lazy=False, cascade='all, delete-orphan')

	def __init__(self, title, width, height, mapBlocks = []):
		self.title = title
		self.width = width
		self.height = height
		self.mapBlocks = mapBlocks

class MapBlock(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	x = db.Column(db.Integer, nullable=False)
	y = db.Column(db.Integer, nullable=False)
	mapId = db.Column(db.Integer, db.ForeignKey("map.id"), nullable=False)
	blockId = db.Column(db.Integer, db.ForeignKey("block.id"), nullable=False)

	def __init__(self, x, y, block = None):
		self.x = x
		self.y = y
		self.block = block
