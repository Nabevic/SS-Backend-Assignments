from db import db

wizard_specializations_table = db.Table(
  "WizardSpecializations",
  db.Model.metadata,
  db.Column('wizard_id',db.ForeignKey('Wizards.wizard_id', ondelete='CASCADE'), primary_key=True),
  db.Column('spell_id',db.ForeignKey('Spells.spell_id', ondelete='CASCADE'), primary_key=True),
  db.Column('proficiency_level',db.Float()),
  db.Column('date_learned',db.DateTime())
)