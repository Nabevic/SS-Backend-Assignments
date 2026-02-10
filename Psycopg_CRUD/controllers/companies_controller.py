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
  
  cursor.execute("""
    INSERT INTO Companies
      (company_name)
      VALUES(%s)
  """, (company_name,))  
  
  conn.commit()
  return jsonify({"message": f"company {company_name} added to Database"}), 201


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


def get_company_by_id(company_id):
  result = cursor.execute("""
    SELECT * FROM Companies
    WHERE company_id = %s
  """,(company_id,))
  result = cursor.fetchone()

  if result:
    return jsonify({"message": "Company found", "results": result}), 200
  else:
    return jsonify({"message": "Company not found"}), 404
  

def update_company(company_id):
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
  


  result = cursor.execute("""
    UPDATE Companies 
    SET company_name = %s
    WHERE company_id = %s
  """, (company_name, company_id))
  conn.commit()
  
  return jsonify({"message": "Company updated", "results": company_name}), 200


def delete_company(company_id):
  result = cursor.execute("""
    SELECT * FROM Companies
    WHERE company_id = %s
    """,(company_id,))

  result = cursor.fetchone()

  if not result:
    return jsonify({"message": "Incorrect ID. Unable to find company"}), 404
  
    # DELETE FROM ProductsCompaniesXref
    # WHERE company_id = %s;
  result = cursor.execute("""
    DELETE FROM Companies
    WHERE company_id = %s;
  """, (company_id, ))
  conn.commit()

  return jsonify({"message": "company deleted"}), 200
