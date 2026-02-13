from flask import jsonify, request
from db import connect_db

conn = connect_db()
cursor = conn.cursor()

def add_warranty():
  post_data = request.form if request.form else request.get_json()

  warranty_months = post_data.get('warranty_months')
  product_id = post_data.get('product_id')

  cursor.execute("""
      Select product_id FROM Products
        WHERE product_id = %s
      """, (product_id,))
  result = cursor.fetchone()
  if not result:
    return jsonify({"message":"Invalid product_id. Product not found"}), 404
  
  try:
    cursor.execute("""
      INSERT INTO Warranties
        (product_id, warranty_months)
        VALUES(%s, %s);
    """, (product_id, warranty_months))  

  except Exception as e:
    cursor.execute("ROLLBACK;")
    return jsonify({"message": f"Error: Warranty could not be added. {e}"}), 400
  else:
    conn.commit()
    cursor.execute("""
      Select * FROM Warranties
        WHERE product_id = %s AND warranty_months = %s
    """, (product_id, warranty_months))
    result = cursor.fetchone()
    if result:
      record = {
        "warranty_id": result[0],
        "product_id": result[1],
        "warranty_months": result[2]
      }

  return jsonify({"message": f"Warranty added","result": record }), 201


def warranty_by_id(warranty_id):
  if request.method == 'GET':
    result = cursor.execute("""
      SELECT * FROM Warranties
      WHERE warranty_id = %s;
    """,(warranty_id,))
    result = cursor.fetchone()


    if result:
      record = {
        "warranty_id": result[0],
        "product_id": result[1],
        "warranty_months": result[2]
      }
      return jsonify({"message": "warranty found", "results": record}), 200
    else:
      return jsonify({"message": "warranty not found"}), 404
  
  elif request.method == 'PUT':
    put_data = request.form if request.form else request.get_json()
    warranty_months = put_data.get("warranty_months")

    result = cursor.execute("""
      SELECT * FROM Warranties
      WHERE warranty_id = %s;
    """,(warranty_id,))

    result = cursor.fetchone()

    if not result:
      return jsonify({"message": "Incorrect ID. Unable to find warranty"}), 404
    
    if not warranty_months:
      return jsonify({"message": "warranty_months is required"}), 400
    
    try:  
      result = cursor.execute("""
        UPDATE Warranties 
        SET warranty_months = %s
        WHERE warranty_id = %s;
      """, (warranty_months, warranty_id))

    except Exception as e:
      result = cursor.execute("ROLLBACK;")
      return jsonify({"message": f"Error: Warranty could not be updated. {e}"}), 400
    else:
      conn.commit()
      updated_record = {
        "warranty_months": warranty_months
      }
    
    return jsonify({"message": "warranty updated", "results": updated_record}), 200


def delete_warranty(warranty_id):
  result = cursor.execute("""
    SELECT * FROM Warranties
    WHERE warranty_id = %s;
    """,(warranty_id,))

  result = cursor.fetchone()

  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find warranty"}), 404
  
  deleted_record = {
        "warranty_id": result[0],
        "product_id": result[1],
        "warranty_months": result[2]
      }

  try:
    result = cursor.execute("""
      DELETE FROM Warranties
      WHERE warranty_id = %s;
    """, (warranty_id, ))

  except Exception as e:
    result = cursor.execute("ROLLBACK;")
    return jsonify({"message": f"Error: Warranty could not be deleted. {e}"}), 400
  else:
    conn.commit()

  return jsonify({"message": "warranty deleted","results": deleted_record}), 200