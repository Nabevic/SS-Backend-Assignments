from flask import Flask
import routes



def register_blueprints(app):
  app.register_blueprint(routes.auth)
  app.register_blueprint(routes.user)
  app.register_blueprint(routes.address)
  app.register_blueprint(routes.event)