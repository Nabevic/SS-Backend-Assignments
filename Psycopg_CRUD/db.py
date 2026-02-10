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
