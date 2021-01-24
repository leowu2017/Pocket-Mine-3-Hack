# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 21:41:23 2021

@author: user
"""

import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from flaskr.shared import db
from flaskr.models.auth import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

class AuthPropertiesForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = StringField('Password', validators=[DataRequired()])

@bp.route('/register', methods=('GET', 'POST'))
def register():
	form = AuthPropertiesForm(request.form)
	if request.method == 'POST' and form.validate():
		username = request.form['username']
		password = request.form['password']

		user = User.query.filter_by(username=username).first()
		if user is not None:
			flash('User {} is already registered.'.format(username))
		else:
			user = User(username, password)
			db.session.add(user)
			db.session.commit()

			return redirect(url_for('auth.login'))

	for error in form.username.errors:
		flash('Username: ' + error)
	for error in form.password.errors:
		flash('Password: ' + error)

	return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
	form = AuthPropertiesForm(request.form)
	if request.method == 'POST' and form.validate():
		username = request.form['username']
		password = request.form['password']

		user = User.query.filter_by(username=username).first()
		if user is None:
			flash('Incorrect username.')
		elif not user.checkPassword(password):
			flash('Incorrect password.')
		else:
			session.clear()
			session['user_id'] = user.id
			return redirect(url_for('index'))

	return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = User.query.filter_by(id=user_id).first()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view
