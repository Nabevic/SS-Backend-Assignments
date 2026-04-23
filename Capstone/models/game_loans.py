import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class GameLoans(db.Model):
  __tablename__ = "GameLoans"

  loan_id = db.Column(UUID(as_uuid=True), )
  game_id = db.Column(UUID(as_uuid=True))
  borrower_id = db.Column(UUID(as_uuid=True))
  checkout_date = db.Column(db.DateTime(), nullable=False)
  due_date = db.Column(db.DateTime())
  notes = db.Column(db.String())

  board_game = db.relationship("BoardGames", foreign_keys='[GameLoans.game_id]', back_populates='loan')
  user = db.relationship("Users", foreign_keys='[GameLoans.borrower_id]', back_populates='borrower')

  def __init__(self, game_id, borrower_id, checkout_date, due_date, notes):
    self.game_id = game_id
    self.borrower_id = borrower_id
    self.checkout_date = checkout_date
    self.due_date = due_date
    self.notes = notes

  def new_loan_obj():
    return GameLoans('','','','','')
  

class GameLoansSchema(ma.Schema):
  class Meta:
    fields = ['loan_id', 'game_id', 'borrower_id', 'checkout_date', 'due_date', 'notes']

  loan_id = ma.fields.UUID()
  game_id = ma.fields.UUID(required=True)
  borrower_id = ma.fields.UUID(required=True)
  checkout_date = ma.fields.DateTime(required=True)
  due_date = ma.fields.DateTime(allow_none=True)
  notes = ma.fields.String(allow_none=True)

game_loan_schema = GameLoansSchema()
game_loans_schema = GameLoansSchema(many=True)