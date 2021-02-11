# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 21:27:53 2021

@author: user
"""

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from flaskr.models.auth import User
from flaskr.models.map import Block, Map, MapBlock
from .shared import db, migrate, csrf

import wtforms_json

def insert_db_data():
	## User
	db.session.add(User('root', '0000'))

	## Blocks
	blocks = ['question.jpg', 'empty.jpg', 'bedrock.jpg', 'dirt.jpg', 'rock1.jpg', 'rock2.jpg', 'rock3.jpg', 'coal.jpg', 'iron.jpg', 'gold.jpg', 'diamond.jpg', 'bomb.jpg', 'dynamite.jpg', 'grenade.jpg', 'drill.jpg', 'drill.jpg', 'explosive_drill.jpg', 'chain_lightning.jpg', 'firework.jpg', 'gas.jpg', 'blast_range.jpg', 'worm.jpg', 'bank.jpg', 'statue.jpg', 'chest.jpg', 'explosive_coal.jpg', 'explosive_iron.jpg', 'explosive_gold.jpg', 'explosive_diamond.jpg', 'coal_bomb.jpg', 'iron_bomb.jpg', 'gold_bomb.jpg', 'diamond_bomb.jpg', 'shuffle_arrow_up.jpg', 'shuffle_arrow_right.jpg', 'shuffle_arrow_down.jpg', 'shuffle_arrow_left.jpg', 'arrow_up.jpg', 'arrow_right.jpg', 'arrow_down.jpg', 'arrow_down.jpg', 'torch.jpg', 'shuffle_explosive_bomb.jpg', 'shuffle_explosive_dynamite.jpg', 'shuffle_explosive_grenade.jpg', 'shuffle_explosive_gas.jpg', 'monster01.jpg']
	for block in blocks:
		db.session.add(Block(block))

	# ## MapBlocks
	# mapBlock1 = MapBlock(0, 0, dirt)
	# db.session.add(mapBlock1)
	# mapBlock2 = MapBlock(1, 1, iron)
	# db.session.add(mapBlock2)

	# ## Maps
	# db.session.add(Map('Daily', 8, 20, [mapBlock1, mapBlock2]))

	db.session.commit()

def init_db():
	db.drop_all()
	db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo('Initialized the database.')

@click.command('load_default')
@with_appcontext
def load_default():
	"""Add default data to database."""
	insert_db_data()
	click.echo('Default data is saved.')
	
def init_app(app):
	# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/flaskr.sqlite'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:0000@localhost:5432/pm3'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
	db.init_app(app)
	migrate.init_app(app, db)
	csrf.init_app(app)
	wtforms_json.init()
	app.cli.add_command(init_db_command)
	app.cli.add_command(load_default)