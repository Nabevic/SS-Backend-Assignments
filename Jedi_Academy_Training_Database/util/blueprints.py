from flask import Flask
import routes



def register_blueprints(app):
  app.register_blueprint(routes.ability)