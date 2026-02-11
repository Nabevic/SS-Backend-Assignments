from flask import jsonify, request
from db import connect_db

conn = connect_db()
cursor = conn.cursor()

def add_warranty():
  post_data = request.form if request.form else request.get_json()

  warranty_months = post_data.get('warranty_months')
  product_id = post_data.get('product_id')
  
  try:
    cursor.execute("""
      INSERT INTO Warranties
        (product_id, warranty_months )
        VALUES(%s, %s);
    """, (product_id, warranty_months))  
    conn.commit()

  except:
    cursor.rollback()
    return jsonify({"message": "Warranty could not be added"}), 400

  return jsonify({"message": f"warranty for {warranty_months} months added to product"}), 201


def warranty_by_id(warranty_id):
  if request.method == 'GET':
    result = cursor.execute("""
      SELECT * FROM Warranties
      WHERE warranty_id = %s;
    """,(warranty_id,))
    result = cursor.fetchone()

    if result:
      return jsonify({"message": "warranty found", "results": result}), 200
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
      conn.commit()

    except:
      cursor.rollback()
      return jsonify({"message": "Warranty could not be updated"}), 400
    
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

  try:
    result = cursor.execute("""
      DELETE FROM Warranties
      WHERE warranty_id = %s;
    """, (warranty_id, ))
    conn.commit()

  except:
    cursor.rollback()
    return jsonify({"message": "Warranty could not be deleted"}), 400

  return jsonify({"message": "warranty deleted","results": deleted_warranty}), 200