import functools
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

import pymongo
myclient = pymongo.MongoClient("mongodb+srv://limarcospap:cQ6oyLLGIukkPvnd@cluster0.gahcw.mongodb.net/test?authSource=admin&replicaSet=atlas-708nws-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
mydb = myclient["labprog"]
users_col = mydb["usuarios"]

@bp.route('/register', methods=('GET', 'POST')) #fazer o login ser unico
def register():
  if request.method == 'POST':
    rf = request.form
    print(rf)
    for key in rf.keys():
        data=key
    print(data)
    print(type(data))
    data_dic=json.loads(data)
    print(type(data_dic))
    data_dic['senha'] = generate_password_hash(data_dic['senha'])
    users_col.insert_one(data_dic)
    return "deu certo"
  else:
    abort(404)

@bp.route('/findall')
def findall():
  resp = ""
  for x in users_col.find():
    resp = resp + str(x)+"\n"
  return resp
      
@bp.route('/insert_one')
def insertall():
  json_obj = {'nome': 'Gustavo', 'sobrenome': 'Testoni', 'nascimento': '15/02/1997', 'login': 'gcasq', 'senha': '123456', 'admin': true}
  x = users_col.insert_one(json_obj)
  return "deu certo"

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print("Chegou no back")
        rf = request.form
        print(rf)
        for key in rf.keys():
            data=key
            print(data)
            data_dic=json.loads(data)

        error = None
        user = users_col.find_one({"login": data_dic["login"]})
        print(user)
        print("")
        print(data_dic)
        if user is None:
            error = 'Inexistent username.'
            print(error)
        elif not check_password_hash(user["senha"], data_dic["senha"]):
            error = 'Incorrect password.'
            print(error)

        if error is None:
            #session.clear()
            #session['user_id'] = user['_id']
            #session['admin'] = user['admin']
            resp = jsonify("true")
            resp.headers['Access-Control-Allow-Origin']='*'
            return resp
        flash(error)
    return "False"

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

