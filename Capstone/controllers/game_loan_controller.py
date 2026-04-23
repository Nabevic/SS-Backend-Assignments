from flask import jsonify, request
from db import db
from models.game_loans import GameLoans, game_loan_schema, game_loans_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


def add_loan_record():
  pass
def get_loan_records():
  pass
def get_loan_records_by_game(game_id):
  pass
def get_loan_records_by_borrower(borrower_id):
  pass
def loan_record_by_id(loan_id):
  pass
def delete_loan_record():
  pass