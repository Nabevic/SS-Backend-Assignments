from flask import jsonify, request
from db import connect_db

conn = connect_db()
cursor = conn.cursor()



def add_product():
  post_data = request.form if request.form else request.json
  required_fields = ['product_name']

  product = {}
  product['company_id'] = post_data['company_id']
  product['product_name'] = post_data['product_name']
  product['description'] = post_data['description']
  product['price'] = post_data['price']
  product['active'] = post_data['active']
  # company_id = post_data['company_id']
  # product_name = post_data['product_name']
  # price = post_data['price']
  # description = post_data['description']

  for field in required_fields:
    if field not in post_data:
      return jsonify({"message": f"{field} is required to add a product"}), 400
    
  if post_data['product_name'].strip("/\\-_., ") == "":
    return  jsonify({"message": "invalid product_name"}), 400
  
  result = cursor.execute("""
    SELECT * FROM Products
    WHERE product_name = %s
  """,(product['product_name'],))

  result = cursor.fetchone()

  if result:
    return jsonify({"message": 'Product name already exists. Product name must be unique',"results": result}), 400
  

  result = cursor.execute("""
    INSERT INTO PRODUCTS
    (company_id, product_name, price, description, active)
    VALUES(%s,%s,%s,%s,%s)
    
  """,(product['company_id'], product['product_name'], product['price'], product['description'], product['active']))
  conn.commit()

  return jsonify({"message": "product added", "result": product}), 201


def add_product_category_association():
  post_data = request.form if request.form else request.json

  product_id = post_data['product_id']
  category_id = post_data['category_id']

  result = cursor.execute("""
    INSERT INTO ProductsCategoriesXref
    (product_id, category_id)
    VALUES(%s,%s)
  """, (product_id, category_id))
  conn.commit()

  return jsonify({"message":"Association added"}), 201


def get_all_products():
  result = cursor.execute("""
    SELECT * FROM Products;
  """)

  result = cursor.fetchall()

  record_list = []

  for record in result:
    record = {
      'product_id': record[0],
      'product_name' : record[1],
      'company_id': record[2],
      'description' : record[3],
      'price' : record[4],
      'active' : record[5],
    }

    record_list.append(record)

  return jsonify({"message": "Products found", "results" : record_list}), 200 

def get_active_products():
  result = cursor.execute("""
    SELECT * FROM Products
    WHERE active = true;
  """)

  result = cursor.fetchall()

  record_list = []

  for record in result:
    record = {
      'product_id': record[0],
      'product_name' : record[1],
      'company_id': record[2],
      'description' : record[3],
      'price' : record[4],
      'active' : record[5],
    }

    record_list.append(record)

  return jsonify({"message": "Active products found", "results" : record_list}), 200 
