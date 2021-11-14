import json
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__, instance_relative_config=True)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)
db = SQLAlchemy(app)


class Board(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  squares = db.Column(db.ARRAY(db.String(255)))

  def __repr__(self):
      return '<User %r>' % self.username


@app.route('/')
def hello_world():
  return 'Hello, Docker!'

@app.route('/boards', methods=["GET", "POST", "OPTIONS"])
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
    db.session.add(board)
    db.session.commit()
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

@app.route('/initdb')
def create_db():
  db.create_all()
  return "ECHO: Database up"

if __name__ == "__main__":
  app.run(host ='0.0.0.0')