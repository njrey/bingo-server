import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
from flask import Flask, request, make_response

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
  return 'Hello, Docker!'

@app.route('/boards', methods=["GET", "POST", "OPTIONS"])
def get_boards() :
  if request.method == 'GET':
    conn = psycopg2.connect(host="db", port = 5432, database="bingo_boards", user="postgres", password="postgres")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "my_boards"')
    row_headers=[x[0] for x in cursor.description] #this will extract row headers

    results = cursor.fetchall()
    print(results)

    json_data=[]
    for result in results:
      json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    resp = make_response(json.dumps(json_data))
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    return resp
  elif request.method == 'POST':
    
    conn = psycopg2.connect(host="db", port = 5432, database="bingo_boards", user="postgres", password="postgres")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "my_boards" (name, squares) VALUES (%s, %s)', ('hey', request.get_json()))
    conn.commit()
    cursor.close()
    conn.close()
    print(request.get_json())
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
def db_init():
  conn = psycopg2.connect(host="db", port = 5432, user="postgres", password="postgres")
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()

  cursor.execute("DROP DATABASE IF EXISTS bingo_boards")
  cursor.execute("CREATE DATABASE bingo_boards")
  cursor.close()

  conn = psycopg2.connect(host="db", port = 5432, database="bingo_boards", user="postgres", password="postgres")
  cursor = conn.cursor()

  cursor.execute("DROP TABLE IF EXISTS my_boards")
  cursor.execute("CREATE TABLE my_boards (name VARCHAR(255), squares VARCHAR(255) ARRAY[25])")
  cursor.close()
  conn.commit()

  return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')