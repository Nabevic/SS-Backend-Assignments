from db import db

games_categories_association_table = db.Table(
  "GamesCategoriesAssociation",
  db.Model.metadata,
  db.Column('game_id', db.ForeignKey('BoardGames.game_id', ondelete='CASCADE'), primary_key=True),
  db.Column('category_id', db.ForeignKey('Categories.category_id', ondelete='CASCADE', primary_key=True))
)