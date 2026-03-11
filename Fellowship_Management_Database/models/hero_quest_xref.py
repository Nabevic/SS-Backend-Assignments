from db import db

hero_quest_association_table = db.Table(
  "HeroesQuestsAssociation",
  db.Model.metadata,
  db.Column('hero_id', db.ForeignKey('Heroes.hero_id', ondelete='CASCADE'), primary_key=True),
  db.Column('quest_id', db.ForeignKey('Quests.quest_id', ondelete='CASCADE'), primary_key=True),
  db.Column('date_joined', db.DateTime())
)