import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, Docker!'

@app.route('/boards')
def get_boards() :
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

  return json.dumps(json_data)

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
  cursor.execute("CREATE TABLE my_boards (name VARCHAR(255), description VARCHAR(255))")
  cursor.close()
  conn.commit()

  return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')