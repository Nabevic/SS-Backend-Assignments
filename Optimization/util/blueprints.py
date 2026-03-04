from flask import Flask
import routes



def register_blueprints(app):
  app.register_blueprint(routes.product)
  app.register_blueprint(routes.category)
  app.register_blueprint(routes.company)
  app.register_blueprint(routes.warranty)
  
