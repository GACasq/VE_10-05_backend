import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
import pymongo
import base64

myclient = pymongo.MongoClient("mongodb+srv://limarcospap:cQ6oyLLGIukkPvnd@cluster0.gahcw.mongodb.net/test?authSource=admin&replicaSet=atlas-708nws-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
bd = myclient["labprog"]
documents_col = bd["documentos"]

bp = Blueprint('document', __name__, url_prefix='/document')

@bp.route('/get-pfc', methods=(['GET','POST'])) 
def getPfc():
  documents = documents_col.find({"titulo": request.form['titulo']}) #query baseada no titulo
  doc = {}
  for key in request.form.keys():
    data_dic[key] = request.form[key]  #salva aqui os dados do pdf
  if (doc != {}):
    return doc
  return "Document not found"

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
    data_dic = {}
    for key in request.form.keys():
      data_dic[key] = request.form[key]

    with open(data_dic['myfile'], "rb") as pdf_file:
        if pdf_file.read()[0:4] != b'%PDF':
          raise ValueError('Missing the PDF file signature')
          return "Documento não é um pdf"
      encoded_string = base64.b64encode(pdf_file.read())
    data_dic['pdfB64'] = encoded_string
    documents_col.insert_one(data_dic)
    return "sucesso"