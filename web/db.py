import os
import click
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import ARRAY

engine = create_engine(os.environ['DATABASE_URL'])

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

@with_appcontext
def get_db(app):
    if 'db' not in g:
        g.db = SQLAlchemy(app)
        return g.db

    return g.db

def init_db(app):
    db = get_db(app)
    db.create_all()

Model = declarative_base(name='Model')
Model.query = db_session.query_property()

@click.command('init-db')
@with_appcontext
def init_db_command(app):
    """Clear the existing data and create new tables."""
    init_db(app)

def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

class Board(Model):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    squares = Column(ARRAY(String(255)))

    def __repr__(self):
        return '<User %r>' % self.username