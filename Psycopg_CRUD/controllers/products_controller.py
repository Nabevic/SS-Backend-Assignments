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
  
  try:
    result = cursor.execute("""
      INSERT INTO PRODUCTS
      (company_id, product_name, price, description, active)
      VALUES(%s,%s,%s,%s,%s)
    """,(product['company_id'], product['product_name'], product['price'], product['description'], product['active']))
    conn.commit()

  except:
    cursor.rollback()
    return jsonify({"message": "Product could not be added"}), 400

  return jsonify({"message": "product added", "result": product}), 201


def add_product_category_association():
  post_data = request.form if request.form else request.json

  product_id = post_data['product_id']
  category_id = post_data['category_id']

  try:
    result = cursor.execute("""
      INSERT INTO ProductsCategoriesXref
      (product_id, category_id)
      VALUES(%s,%s)
    """, (product_id, category_id))
    conn.commit()

  except:
    cursor.rollback()
    return jsonify({"message": "Association could not be added"}), 400

  return jsonify({"message":"Association added","result": result}), 201


def get_all_products():
  result = cursor.execute("""
     SELECT p.*, c.category_id, c.category_name, w.warranty_id, w.warranty_months FROM Products p
    LEFT JOIN ProductsCategoriesXref pcx
      ON p.product_id = pcx.product_id
    LEFT JOIN Categories c
      ON c.category_id = pcx.category_id
    LEFT JOIN Warranties w 
      ON p.product_id = w.product_id;
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
      'category_id': record[6],
      'category_name' : record[7],
      'warranty_id' : record[8],
      'warranty_months' : record[9]
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


def product_by_id(product_id):
  if request.method == 'GET':
    result = cursor.execute("""
      SELECT p.*, c.category_id, c.category_name, w.warranty_id, w.warranty_months FROM Products p
      LEFT JOIN ProductsCategoriesXref pcx
        ON p.product_id = pcx.product_id
      LEFT JOIN Categories c
        ON c.category_id = pcx.category_id
      LEFT JOIN Warranties w 
        ON p.product_id = w.product_id  
      WHERE p.product_id = %s;
    """, (product_id,))
    result = cursor.fetchone()
    if result:
      record = {
        'product_id': result[0],
        'product_name' : result[1],
        'company_id': result[2],
        'description' : result[3],
        'price' : result[4],
        'active' : result[5],
        'category_id': result[6],
        'category_name' : result[7],
        'warranty_id' : result[8],
        'warranty_months' : result[9]
      }
      return jsonify({"message": "Product found", "results": record}), 200
    else:
      return jsonify({"message": "Product not found"}), 404
  
  elif request.method == 'PUT':
    put_data = request.form if request.form else request.json
    product = {}
    product['company_id'] = put_data['company_id']
    product['product_name'] = put_data['product_name']
    product['description'] = put_data['description']
    product['price'] = put_data['price']
    product['active'] = put_data['active']

    result = cursor.execute("""
      SELECT * FROM Products
      WHERE product_id = %s;
    """,(product_id,))

    result = cursor.fetchone()

    if not result:
      return jsonify({"message": "Incorrect ID. Unable to find product"}), 404
    
    try:
      result = cursor.execute("""
        UPDATE Products 
        SET company_id = %s,
        product_name = %s,
        description = %s,
        price = %s,
        active = %s
        WHERE product_id = %s;
      """, (product['company_id'], product['product_name'], product['description'], product['price'], product['active'], product_id))
      conn.commit()

    except:
      cursor.rollback()
      return jsonify({"message": "Product could not be updated"}), 400
    
    return jsonify({"message": "Product updated", "results": product}), 200

  
def get_product_by_company(company_id):
  result = cursor.execute("""
    SELECT * FROM Products
    WHERE company_id = %s;
  """, (company_id,))
  result = cursor.fetchall()

  if result:
    return jsonify({"message": "Products found","results": result}), 200
  else:
    return jsonify({"message": "Products not found"}), 404
  

def delete_product(product_id):
  result = cursor.execute("""
    SELECT * FROM Products p
    LEFT JOIN Warranties w
      ON p.product_id = w.product_id
    LEFT JOIN ProductsCategoriesXref pcx
      ON p.product_id = pcx.product_id
    WHERE p.product_id = %s;
    """,(product_id,))

  result = cursor.fetchall()

  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find Product"}), 404
  
  deleted_product = result

  try:
    result = cursor.execute("""
      DELETE FROM Warranties
      WHERE product_id = %s;
      
      DELETE FROM ProductsCategoriesXref
      WHERE product_id = %s;
                                                  
      DELETE FROM Products
      WHERE product_id = %s;
    """, (product_id, product_id, product_id))
    conn.commit()

  except:
    cursor.rollback()
    return jsonify({"message": "Product could not be Deleted"}), 400

  return jsonify({"message": "Product deleted","results": deleted_product}), 200
