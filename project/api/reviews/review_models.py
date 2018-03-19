# project/api/review_models.py

import datetime
from project import db


class Review(db.Model):
    """Create Table for Reviews"""
    __tablename__ = "Reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(db.Integer, nullable=False)
    business_name = db.Column(db.String(80), nullable=False)
    review_text = db.Column(db.String(120), 	nullable=False)
    created_by = db.Column(db.String(80), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

    def __init__(self, business_id, business_name, review_text, created_by, created_at=datetime.datetime.utcnow()):

        self.business_id = business_id
        self.business_name = business_name
        self.review_text = review_text
        self.created_by = created_by
        self.created_at = datetime.datetime.utcnow()
