# -*- coding: utf-8 -*-
"""The flask app module, containing the app factory function."""
from flask import Flask, render_template
from smartmirror import mod_weather, mod_endpoints, mod_splitwise, mod_wolframalpha, mod_uber
from smartmirror.settings import ProdConfig
from smartmirror.extensions import assist

def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    app.secret_key = "asdf"
    register_extensions(app)
    register_blueprints(app)
    print app.url_map
    return app


def register_extensions(app):
    """Register Flask extensions.

    Flask-Assistant does not need to be initalized here if declared as a blueprint.
    Other extensions such as flask-sqlalchemy and flask-migrate are reigstered here.
    If the entire flask app consists of only the Assistant, uncomment the code below.
    """
    # smartmirror.init_app(app, route='/')
    #assist._route = "/apiaiwebhook"
    assist.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints.

    When Flask-Assistant is used to create a blueprint within a standard flask app,
    it must be registered as such, rather that with init_app().

    If the entire flask app consists of only the Assistant, comment out the code below.
    """
    app.register_blueprint(mod_endpoints.views.endpointsBlueprint)
    app.register_blueprint(mod_weather.views.weatherBlueprint, subdomain='weather')
    app.register_blueprint(mod_splitwise.views.splitwiseBlueprint)
    app.register_blueprint(mod_wolframalpha.views.wolframalphaBlueprint)
    app.register_blueprint(mod_uber.views.uberBlueprint)

    return None
