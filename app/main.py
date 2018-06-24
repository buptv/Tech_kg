import os
import logging
import neomodel
from flask import Flask
from grest import global_config
from users_view import UsersView

def create_app():
    # create flask app
    app = Flask(__name__)

    # add a simple endpoint for testing purposes
    @app.route('/')
    def index():
        return "Hello World!"

    # configure connection to database
    neomodel.config.DATABASE_URL = global_config.DB_URL  # The bolt URL of your Neo4j instance
    neomodel.config.AUTO_INSTALL_LABELS = True
    neomodel.config.FORCE_TIMEZONE = True  # default False

    # attach logger to flask's app logger
    app.ext_logger = app.logger

    # register users' view
    UsersView.register(app, route_base="/users", trailing_slash=False)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000)