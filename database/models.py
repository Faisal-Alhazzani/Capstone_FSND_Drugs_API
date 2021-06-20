import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ.get('DATABASE_URL')
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


# ------------------------------------------------------------#
# Models.
# ------------------------------------------------------------#

class Drug(db.Model):
    __tablename__ = 'Drug'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String(120))
    side_effects = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    price = db.Column(db.String)
    Drug_Availability = db.relationship('Drug_Availability', backref='venue',
                                        lazy=True)

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'side_effects': self.side_effects,
            'image_link': self.image_link,
            'price': self.price
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Pharmacy(db.Model):
    __tablename__ = 'Pharmacy'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    location_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    Drug_Availability = db.relationship('Drug_Availability',
                                        backref='Pharmacy', lazy=True)

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'phone': self.phone,
            'location_link': self.location_link,
            'image_link': self.image_link
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Drug_Availability(db.Model):
    __tablename__ = 'Drug_Availability'

    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('Drug.id'), nullable=False)
    pharmcy_id = db.Column(db.Integer, db.ForeignKey('Pharmacy.id'),
                           nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
