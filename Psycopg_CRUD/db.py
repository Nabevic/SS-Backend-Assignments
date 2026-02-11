from flask import Flask, jsonify, request

import psycopg2
import os


def connect_db():
  
  database_name = os.environ.get("DATABASE_NAME")
  user_name = os.environ.get("USER")
  password = os.environ.get('PASSWORD')
  app_host = os.environ.get('APP_HOST')
  app_port = os.environ.get('APP_PORT')
  local_host = os.environ.get("HOST")

  conn = psycopg2.connect(f"user={user_name} dbname={database_name}  host={app_host} port={app_port} password={password} ")
  return conn

conn = connect_db()
cursor = conn.cursor()

def create_schema():
  print('Creating Table: Companies')
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Companies (
      company_id SERIAL PRIMARY KEY,
      company_name VARCHAR UNIQUE NOT NULL
    );
  """)
  conn.commit()

  print('Creating Table: Products')
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
      product_id SERIAL PRIMARY KEY,
      product_name VARCHAR UNIQUE NOT NULL,
      company_id INTEGER,
      description VARCHAR,
      price REAL,
      active BOOLEAN DEFAULT true,
      FOREIGN KEY (company_id)
        REFERENCES Companies(company_id)
    );
  """)
  conn.commit()

  print('Creating Table: Warranties')
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Warranties (
      warranty_id SERIAL PRIMARY KEY,
      product_id INTEGER,
      warranty_months VARCHAR NOT NULL,
      FOREIGN KEY (product_id)
        REFERENCES Products(product_id)
    );
  """)
  conn.commit()

  print('Creating Table: Categories')
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories (
      category_id SERIAL PRIMARY KEY,
      category_name VARCHAR UNIQUE NOT NULL
    );
  """)
  conn.commit()

  print('Creating Table: ProductsCategoriesXref')
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
      product_id INTEGER,
      category_id INTEGER,
      PRIMARY KEY (product_id, category_id),
      FOREIGN KEY (product_id)
        REFERENCES Products (product_id),
      FOREIGN KEY (category_id)
        REFERENCES Categories (category_id)
    );
  """)
  conn.commit()

