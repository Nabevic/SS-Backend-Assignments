from flask import Flask
import routes



def register_blueprints(app):
  app.register_blueprint(routes.ability)
  app.register_blueprint(routes.hero)
  app.register_blueprint(routes.location)
  app.register_blueprint(routes.quest)
  app.register_blueprint(routes.race)
  app.register_blueprint(routes.realm)
