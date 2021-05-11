import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
import pymongo
myclient = pymongo.MongoClient("mongodb+srv://limarcospap:cQ6oyLLGIukkPvnd@cluster0.gahcw.mongodb.net/test?authSource=admin&replicaSet=atlas-708nws-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
bd = myclient["labprog"]
documents_col = bd["documentos"]

bp = Blueprint('document', __name__, url_prefix='/document')

@bp.route('/get-pfc', methods=(['GET','POST'])) 
def getPfc():
  documents = documents_col.find()
  resp = ""
  return "sucesso"
