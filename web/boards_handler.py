import json
from flask import Blueprint, request, make_response
from web.db import Board, db_session

bp = Blueprint('boards', __name__, url_prefix='/boards/')

@bp.route('/', methods=["GET", "POST", "OPTIONS"])
def get_boards() :

  if request.method == 'GET':

    results = Board.query.all()
    json_data=[]
    for result in results:
      json_data.append({"name": result.name, "squares": result.squares, "id": result.id})

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

@bp.route('/<board_id>', methods=["GET", "POST", "OPTIONS", "DELETE"])
def get_board(board_id) :
  if request.method == 'GET':
    result = Board.query.filter(Board.id == board_id).first()
    board = {
      "id": result.id,
      "name": result.name,
      "squares": result.squares
    }
    return board

  if request.method == 'DELETE':
    print('delete')
    Board.query.filter(Board.id == board_id).delete()
    db_session.commit()
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    resp.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, Accept, Origin, Authorization'
    resp.headers['Access-Control-Allow-Methods'] =  'GET, POST, PUT, DELETE, OPTIONS'
    return resp
  elif request.method == 'OPTIONS':
      resp = make_response()
      resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
      resp.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, Accept, Origin, Authorization'
      resp.headers['Access-Control-Allow-Methods'] =  'GET, POST, PUT, DELETE, OPTIONS'
      return resp
