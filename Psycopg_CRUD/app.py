from flask import Flask, jsonify, request
from db import connect_db, create_schema
import routes


conn = connect_db()
cursor = conn.cursor()

app = Flask(__name__)
app.register_blueprint(routes.category)
app.register_blueprint(routes.company)
app.register_blueprint(routes.product)
app.register_blueprint(routes.warranty)

if __name__ == '__main__':
  result = create_schema()
  app.run()