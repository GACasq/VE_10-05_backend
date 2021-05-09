import functools
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

from . import db

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    rf = request.form
    print(rf)
    for key in rf.keys():
        data=key
    print(data)
    data_dic=json.loads(data)
    print(type(data_dic))
    #db.dbMongo.create()
    mycol.insert_one(data_dic)
    resp = jsonify(data_dic)
    resp.headers['Access-Control-Allow-Origin']='*'

    return resp
  else:
    abort(404)


      
    




"""
    db = get_db()
    error = None

    if not username:
      error = 'Username is required.'
    elif not password:
      error = 'Password is required.'
    elif not birth_date:
      error = 'Birth date is required.'
    elif not first_name:
      error = 'First name is required.'
    elif password is not request.form['confirmacao-senha']:
      error = 'Password confirmation failed'
    elif db.execute(
      'SELECT id FROM user WHERE username = ?', (username,)
    ).fetchone() is not None:
      error = 'User {} is already registered.'.format(username)

    if error is None:
      db.execute(
        'INSERT INTO user (username, first_name, last_name, birth_date, password) VALUES (?, ?, ?, ?, ?)',
        (username, first_name, last_name, birth_date, generate_password_hash(password))
      )
      db.commit()
      return redirect(url_for('auth.login'))

    flash(error)
  return render_template('user/create/createUser.html')
  """

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['loginInput']
        password = request.form['passwordInput']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index.html'))

        flash(error)

    return render_template('index.html')

@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

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

