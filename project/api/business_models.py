# project/api/business_models.py

import datetime

from project import db
from flask import current_app

class Business(db.Model):
    __tablename__ = "Businesses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(80), nullable = False, unique = True)
    business_category = db.Column(db.String(80), nullable = False)
    business_addr = db.Column(db.String(80), nullable = False)
    business_desc = db.Column(db.String(80), nullable = False)
    created_by = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow(), nullable = False)

    def __init__(self, business_name, business_category, business_addr, business_desc,
            created_by, created_at=datetime.datetime.utcnow()):
        self.business_name = business_name
        self.business_category = business_category
        self.business_addr = business_addr
        self.business_desc = business_desc
        self.created_by = created_by
        self.created_at = datetime.datetime.now()

    def delete(self):
        """
        Delete a business
        """
        db.session.delete(self)
        db.session.commit()

    def save(self):
        """
        Save a business into the db
        """
        db.session.add(self)
        db.session.commit()
