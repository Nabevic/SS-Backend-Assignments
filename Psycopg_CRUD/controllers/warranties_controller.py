from flask import jsonify, request
from db import connect_db

conn = connect_db()
cursor = conn.cursor()

def add_warranty():
  post_data = request.form if request.form else request.get_json()

  warranty_months = post_data.get('warranty_months')
  product_id = post_data.get('product_id')
  
  cursor.execute("""
    INSERT INTO Warranties
      (product_id, warranty_months )
      VALUES(%s, %s);
  """, (product_id, warranty_months))  
  
  conn.commit()
  return jsonify({"message": f"warranty for {warranty_months} months added to product"}), 201


def get_warranty_by_id(warranty_id):
  result = cursor.execute("""
    SELECT * FROM Warranties
    WHERE warranty_id = %s;
  """,(warranty_id,))
  result = cursor.fetchone()
  # This doesn't show the column names, just the values. add something to see them

  if result:
    return jsonify({"message": "warranty found", "results": result}), 200
  else:
    return jsonify({"message": "warranty not found"}), 404
  

def update_warranty(warranty_id):
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
  
  result = cursor.execute("""
    UPDATE Warranties 
    SET warranty_months = %s
    WHERE warranty_id = %s;
  """, (warranty_months, warranty_id))
  conn.commit()
  
  return jsonify({"message": "warranty updated", "results": warranty_months}), 200


def delete_warranty(warranty_id):
  result = cursor.execute("""
    SELECT * FROM Warranties
    WHERE warranty_id = %s;
    """,(warranty_id,))

  result = cursor.fetchone()

  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find warranty"}), 404
  
  deleted_warranty = result
  # this technically works, but you don't see the column names
  result = cursor.execute("""
    DELETE FROM Warranties
    WHERE warranty_id = %s;
  """, (warranty_id, ))
  conn.commit()

  return jsonify({"message": "warranty deleted","results": deleted_warranty}), 200