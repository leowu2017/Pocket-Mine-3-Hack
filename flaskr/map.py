from flask import (
	Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms import Form
from wtforms.fields import IntegerField

from flaskr.shared import db, getQeustion
from flaskr.models.map import Map, Block, MapBlock

bp = Blueprint('map', __name__)

class MapPropertiesForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	width = IntegerField('Width', validators=[DataRequired(), NumberRange(0)])
	height = IntegerField('Height', validators=[DataRequired(), NumberRange(0)])

class MapBlockForm(FlaskForm):
	id = IntegerField()
	x = IntegerField()
	y = IntegerField()
	block_id = IntegerField()

def get_map(id):
	map = Map.query.filter_by(id=id).first()
	if map is None:
		abort(404, "Map doesn't exist.")

	return map

@bp.route('/')
def index():
	maps = Map.query.all()
	return render_template('map/index.html', maps=maps)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	form = MapPropertiesForm()
	if request.method == 'POST' and form.validate_on_submit():
		map = Map(form.title.data, form.width.data, form.height.data)
		db.session.add(map)
		db.session.commit()
		return redirect(url_for('map.update_layouts', id=map.id))

	for error in form.title.errors:
		flash('Title: ' + error)
	for error in form.width.errors:
		flash('Width: ' + error)
	for error in form.height.errors:
		flash('Height: ' + error)
	return render_template('map/create.html', form=form)

@bp.route('/<int:id>/view')
def view(id):
	map = get_map(id)
	cellSize = 400 / map.width
	return render_template('map/view.html', map=map, cellSize=cellSize, question=getQeustion())

@bp.route('/<int:id>/update_properties', methods=('GET', 'POST'))
@login_required
def update_properties(id):
	map = get_map(id)
	form = MapPropertiesForm(request.form)

	if request.method == 'POST' and form.validate():
		title = request.form['title']
		width = request.form['width']
		height = request.form['height']

		map.title = title
		map.width = width
		map.height = height
		db.session.commit()
		return redirect(url_for('map.view', id=id))

	for error in form.title.errors:
		flash('Title: ' + error)
	for error in form.width.errors:
		flash('Width: ' + error)
	for error in form.height.errors:
		flash('Height: ' + error)
	return render_template('map/update_properties.html', map=map, form=form)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	map = get_map(id)
	db.session.delete(map)
	db.session.commit()
	return redirect(url_for('map.index'))

@bp.route('/<int:id>/update_layouts', methods=('GET', 'POST'))
@login_required
def update_layouts(id):
	map = get_map(id)

	if request.method == 'POST':
		form = MapBlockForm()
		if form.validate_on_submit():
			if form.block_id.data is None:
				return {
					'result': 'error',
					'err': 'Block ID is not provided.'
				}
			block = Block.query.filter_by(id=form.block_id.data).first()

			if form.id.data is not None:
				## existing block
				mapBlock = MapBlock.query.filter_by(id=form.id.data).first()
				mapBlock.block = block
			elif form.x.data is not None and form.y.data is not None:
				## new block
				mapBlock = MapBlock(form.x.data, form.y.data, block)
				db.session.add(mapBlock)
			else:
				return {
					'result': 'error',
					'err': 'Invalid arguments.'
				}
			mapBlock.map = map
			db.session.commit()
			return {'result': 'success'}
		else:
			return form.errors

	cellSize = 400 / map.width
	blocks = Block.query.all()

	return render_template('map/update_layouts.html', map=map, blocks=blocks, cellSize=cellSize, question=getQeustion())