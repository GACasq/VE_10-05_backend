import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
import pymongo
import base64
from werkzeug.utils import secure_filename
import os


myclient = pymongo.MongoClient("mongodb+srv://limarcospap:cQ6oyLLGIukkPvnd@cluster0.gahcw.mongodb.net/test?authSource=admin&replicaSet=atlas-708nws-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
bd = myclient["labprog"]
documents_col = bd["documentos"]

bp = Blueprint('document', __name__, url_prefix='/document')

UPLOAD_FOLDER = '/home/marcos/VE_10-05_backend/files'

@bp.route('/get-pfc', methods=(['GET','POST'])) 
def getPfc():
  cursor = documents_col.find()
  list_cursor = list(cursor)

  for obj in list_cursor:
      obj['_id'] = str(obj['_id'])

  return  {"data": list_cursor}, 200, {'ContentType': 'application/json'}

@bp.route('/download-pfc', methods=(['GET','POST']))   #linkar esta rota a um botão de download para cada registro de documento encontrado pela query da rota /get-pfc
def download():
  b64 = request.form['pdfB64']
  pdf = base64.b64decode(b64)
  if pdf[0:4] != b'%PDF':
    raise ValueError('Missing the PDF file signature')

  f = open(request.form['titulo'], 'wb')   #não sei configurar rota para fazer o download do pdf, na máquina que pediu
  f.write(pdf)
  f.close()

  return "Download concluído"

@bp.route('/upload-pfc', methods=(['GET','POST']))
def uploadPfc():
    print(request.form)
    data_dic = {}
    for key in request.form.keys():
      data_dic[key] = request.form[key]

    documents_col.insert_one(data_dic)

    return "sucesso", 200

@bp.route('/upload-pfc-file', methods=(['GET','POST']))
def uploadPfcFile():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return "sucesso", 200

@bp.route('/search-pfc', methods=(['GET','POST']))
def searchPfc():
  obj = {}
  if request.method == 'GET':
    obj = request.args
  else:
    obj = request.form

  cursor = documents_col.find({'nome': {'$regex': obj['search'], '$options': 'i'}})
  list_cursor = list(cursor)

  for obj in list_cursor:
      obj['_id'] = str(obj['_id'])

  return  json.dumps(list_cursor), 200, {'ContentType': 'application/json'}