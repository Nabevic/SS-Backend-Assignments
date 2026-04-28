import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class GameLoans(db.Model):
  __tablename__ = "GameLoans"

  loan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  game_id = db.Column(UUID(as_uuid=True), db.ForeignKey("BoardGames.game_id"))
  borrower_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"))
  date_borrowed = db.Column(db.DateTime(), nullable=False)
  date_due = db.Column(db.DateTime())
  date_returned = db.Column(db.DateTime())
  notes = db.Column(db.String())

  board_game = db.relationship("BoardGames", foreign_keys='[GameLoans.game_id]', back_populates='loan')
  user = db.relationship("Users", foreign_keys='[GameLoans.borrower_id]', back_populates='borrower')

  def __init__(self, game_id, borrower_id, date_borrowed, date_due, date_returned, notes):
    self.game_id = game_id
    self.borrower_id = borrower_id
    self.date_borrowed = date_borrowed
    self.date_due = date_due
    self.date_returned = date_returned
    self.notes = notes

  def new_loan_obj():
    return GameLoans('','','',None,None,'')
  

class GameLoansSchema(ma.Schema):
  class Meta:
    fields = ['loan_id', 'game_id', 'borrower_id', 'date_borrowed', 'date_due', 'date_returned', 'notes']

  loan_id = ma.fields.UUID()
  game_id = ma.fields.UUID(required=True)
  borrower_id = ma.fields.UUID(required=True)
  date_borrowed = ma.fields.DateTime(required=True)
  date_due =ma.fields.DateTime(allow_none=True)
  date_returned = ma.fields.DateTime(allow_none=True)
  notes = ma.fields.String(allow_none=True)

game_loan_schema = GameLoansSchema()
game_loans_schema = GameLoansSchema(many=True)