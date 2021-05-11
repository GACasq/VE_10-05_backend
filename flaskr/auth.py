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

@bp.route('/register', methods=(['POST'])) #fazer o login ser unico
def register():
    data_dic = {}
    for key in request.form.keys():
        data_dic[key] = request.form[key]
    data_dic['senha'] = generate_password_hash(data_dic['senha'])
    data_dic['admin'] = False
    users_col.insert_one(data_dic)
    return render_template('./user/sucesso.html')
    

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
        rf = request.form
        error = None
        user = users_col.find_one({"login": request.form["login"]})

        if user is None:
            error = 'Inexistent username.'
            print(error)
        if not check_password_hash(user["senha"], request.form["senha"]):
            error = 'Incorrect password.'
            print(error)

        if error is None:
            session.clear()
            print(user['_id'])
            print(user['admin'])
            session['user_id'] = str(user['_id'])
            session['admin'] = user['admin']
            return redirect(url_for('home'))
        #flash(error)
    return "False"

@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')
  if user_id is None:
    g.user = False
  else:
    g.user = users_col.find_one({"_id": user_id})

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

