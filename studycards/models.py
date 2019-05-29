"""The Models module is used to create the tables for the SQLAlchemy database.
They also have specific lines that determine their relationship to each other.
They are are in a 1 to many relationship with 1 CardSet relating to many Cards."""

from studycards import db

class CardSet(db.Model):
    __tablename__ = 'cardset'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    #cards is a relationship to the Card table.  mycardset is a reference in Card back to CardSet
    cards = db.relationship('Card', backref='mycardset', lazy=True)
    def __repr__(self):
        return f"{self.title}"

class Card (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword_one = db.Column(db.String(20), nullable=False)
    keyword_two = db.Column(db.String(20), nullable=False)
    text_one = db.Column(db.String(100), nullable=False)
    image_one = db.Column(db.String(20), nullable=False, default='default.png')
    #cardset_id stores the id of the CardSet this Card is related to.
    cardset_id = db.Column(db.Integer, db.ForeignKey('cardset.id'), nullable=False)
    def __repr__(self):
        return f"Kywrd1=('{self.keyword_one}')"
