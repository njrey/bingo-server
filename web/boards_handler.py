import json
from flask import Blueprint, request, make_response
from web.db import Board, db_session

bp = Blueprint('boards', __name__, url_prefix='/boards')

@bp.route('/')
def hello_world():
  return 'Hello, Docker!'

@bp.route('/boards', methods=["GET", "POST", "OPTIONS"])
def get_boards() :

  if request.method == 'GET':

    results = Board.query.all()
    json_data=[]
    for result in results:
      json_data.append({"name": result.name, "squares": result.squares})
      # json_data.append(dict(zip(row_headers,result)))

    resp = make_response(json.dumps(json_data))
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    return resp
  elif request.method == 'POST':

    print(request.get_json())
    board = Board(name='name', squares=request.get_json())
    db_session.add(board)
    db_session.commit()
    resp = make_response(json.dumps(request.get_json()))
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return resp
  elif request.method == 'PATCH':
      return "ECHO: PACTH\n"

  elif request.method == 'PUT':
      return "ECHO: PUT\n"

  elif request.method == 'DELETE':
        return "ECHO: DELETE"

  elif request.method == 'OPTIONS':
      resp = make_response()
      resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
      resp.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, Accept, Origin, Authorization'
      resp.headers['Access-Control-Allow-Methods'] =  'GET, POST, PUT, DELETE, OPTIONS'
      return resp