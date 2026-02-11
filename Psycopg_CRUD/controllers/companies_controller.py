from flask import jsonify, request
from db import connect_db

conn = connect_db()
cursor = conn.cursor()

def add_company():
  post_data = request.form if request.form else request.get_json()

  company_name = post_data.get('company_name')

  if not company_name:
    return jsonify({"message": "company_name is required"}), 400
  
  result = cursor.execute("""
    SELECT * FROM Companies
    WHERE company_name = %s
  """,(company_name,))

  result = cursor.fetchone()

  if result:
    return jsonify({"message": 'company already exists'}), 400
  
  try:
    cursor.execute("""
      INSERT INTO Companies
        (company_name)
        VALUES(%s)
    """, (company_name,))  
    
    conn.commit()

  except:
      cursor.rollback()
      return jsonify({"message": "Company could not be added"}), 400
  
  return jsonify({"message": f"Company {company_name} added to Database"}), 201


def get_all_companies():
  result = cursor.execute("""
    SELECT * FROM Companies;
  """)

  result = cursor.fetchall()

  record_list = []

  for record in result:
    record = {
      'company_id': record[0],
      'company_name' : record[1]
    }

    record_list.append(record)

  return jsonify({"message": "companies found", "results" : record_list}), 200


def company_by_id(company_id):
  if request.method == 'GET':

    result = cursor.execute("""
      SELECT * FROM Companies
      WHERE company_id = %s
    """,(company_id,))
    result = cursor.fetchone()

    if result:
      return jsonify({"message": "Company found", "results": result}), 200
    else:
      return jsonify({"message": "Company not found"}), 404
    
  elif request.method == 'PUT':
    put_data = request.form if request.form else request.get_json()
    company_name = put_data.get("company_name")

    result = cursor.execute("""
      SELECT * FROM Companies
      WHERE company_id = %s
    """,(company_id,))

    result = cursor.fetchone()

    if not result:
      return jsonify({"message": "Incorrect ID. Unable to find company"}), 404
    
    if not company_name:
      return jsonify({"message": "company_name is required"}), 400
    
    result = cursor.execute("""
      SELECT * FROM Companies
      WHERE company_name = %s
    """,(company_name,))

    result = cursor.fetchone()

    if result:
      return jsonify({"message": 'Company already exists'}), 400
  

  try:
    result = cursor.execute("""
      UPDATE Companies 
      SET company_name = %s
      WHERE company_id = %s
    """, (company_name, company_id))
    conn.commit()

  except:
      cursor.rollback()
      return jsonify({"message": "Company could not be updated"}), 400
  
  return jsonify({"message": "Company updated", "results": company_name}), 200


def delete_company(company_id):
  result = cursor.execute("""
    SELECT * FROM Companies
    WHERE company_id = %s
    """,(company_id,))

  result = cursor.fetchone()

  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find company"}), 404
  
  deleted_company = result
  
  try:
    result = cursor.execute("""
      UPDATE Products
      SET company_id = NULL
      WHERE company_id = %s;
                                                  
      DELETE FROM Companies
      WHERE company_id = %s;
    """, (company_id, company_id ))
    conn.commit()
  
  except:
      cursor.rollback()
      return jsonify({"message": "Company could not be deleted"}), 400

  return jsonify({"message": "company deleted","result": deleted_company}), 200
