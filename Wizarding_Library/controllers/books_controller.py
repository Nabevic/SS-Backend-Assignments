from flask import Flask, jsonify, request

from db import db
from models.books import Books

def construct_record(query):
  book_record = {
    "book_id": query.book_id,
    "school_id": query.school_id,
    "title": query.title,
    "author": query.author,
    "subject": query.subject,
    "rarity_level": query.rarity_level,
    "magical_properties": query.magical_properties,
    "available": query.available
  }
  return book_record



def add_book():
  post_data = request.form if request.form else request.get_json()

  fields = ["school_id", "title", "author", "subject", "rarity_level", "magical_properties"]
  required_fields = ['school_id','title']

  values = {}

  for field in fields:
    field_data = post_data.get(field)
    if field_data in required_fields and not field_data:
      return jsonify({"message": f'{field} is required'}), 400
    values[field] = field_data
  
  new_book = Books(**values)

  try:
    db.session.add(new_book)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": f"unable to create record. {e}"}), 400 
  
  query = db.session.query(Books).filter(Books.title == values['title']).first()
  book_record = construct_record(query)

  return jsonify({"message": "book created", "result": book_record}), 201
  

def get_books():
  books_query = db.session.query(Books).all()
  if not books_query:
    return jsonify({"message": "no books found"}), 404

  book_list = []
  for book in books_query:
    book_record = construct_record(book)
    book_list.append(book_record)

  return jsonify({"message": "books found", "result": book_list})


def get_available_books():
  books_query = db.session.query(Books).filter(Books.available == True).all()

  book_list = []
  for book in books_query:
    book_record = construct_record(book)
    book_list.append(book_record)

  return jsonify({"message": "books found", "result": book_list})

def update_book(book_id):
  data = request.form if request.form else request.get_json()
  book_query = db.session.query(Books).filter(Books.book_id == book_id).first()

  if not book_query:
    return jsonify({"message": f"book not found with id {book_id}"}), 404 

  book_query.school_id = data.get("school_id", book_query.school_id)
  book_query.title = data.get("title", book_query.title)
  book_query.author = data.get("author", book_query.author)
  book_query.subject = data.get("subject", book_query.subject)
  book_query.rarity_level = data.get("rarity_level", book_query.rarity_level)
  book_query.magical_properties = data.get("magical_properties", book_query.magical_properties)
  book_query.available = data.get("available", book_query.available)

  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message:": f"unable to update record: {e}"}), 400
  
  updated_book = db.session.query(Books).filter(Books.book_id == book_id).first()
  book_record = construct_record(updated_book)

  return jsonify({"message": "book updated", "results": book_record}), 200


def delete_book(book_id):
  book_query = db.session.query(Books).filter(Books.book_id == book_id).first()

  if not book_query:
    return jsonify({"message": f"book not found with id {book_id}"}), 404

  deleted_record = construct_record(book_query)

  try:
    db.session.delete(book_query)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message":f"unable to delete book. {e}"}), 400
  
  return jsonify({"message": "book deleted","results": deleted_record})




