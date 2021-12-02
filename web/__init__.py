import os
from flask import Flask
# from config import Config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    print('nolan app init')
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_pyfile('config.py', silent=True)

    from . import db
    db.init_app(app)

    from . import boards_handler
    app.register_blueprint(boards_handler.bp)
    return app


    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app  
