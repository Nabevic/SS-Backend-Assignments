from flask import Blueprint

import controllers


gameloan = Blueprint('gameloan', __name__)


@gameloan.route('/gameloan', methods=['POST'])
def add_loan_record_route():
  return controllers.add_loan_record()

@gameloan.route('/gameloans', methods=['GET'])
def get_loan_records_route():
  return controllers.get_loan_records()

@gameloan.route('/gameloans/<borrower_id>', methods=['GET'])
def get_loan_records_by_borrower_route(borrower_id):
  return controllers.get_loan_records_by_borrower(borrower_id)

@gameloan.route('/gameloan/boardgame/<game_id>', methods=['GET'])
def get_loan_records_by_game_route(game_id):
  return controllers.get_loan_records_by_game(game_id)

@gameloan.route('/gameloan/<loan_id>', methods=['GET','PUT'])
def loan_record_by_id_route(loan_id):
  return controllers.loan_record_by_id(loan_id)

@gameloan.route('/gameloan/return/<loan_id>', methods=['PUT'])
def loan_record_return_route(loan_id):
  return controllers.loan_record_return(loan_id)

@gameloan.route('/gameloan/delete', methods=['DELETE'])
def delete_loan_record_route():
  return controllers.delete_loan_record()