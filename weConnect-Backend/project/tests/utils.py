# project/tests/utils.py


import datetime


from project import db
from project.api.user_models import User
from project.api.business_models import Business
from project.api.review_models import Review

def add_user(username, email, password, created_at=datetime.datetime.utcnow()):
    user = User(
        username=username, 
        email=email,
        password = password, 
        created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user

def add_business(business_name, business_category, business_addr, business_desc,
            created_by, created_at=datetime.datetime.utcnow()):
    business = Business(
        business_name=business_name, 
        business_category=business_category,
        business_addr = business_addr, 
        business_desc = business_desc,
        created_by = created_by,
        created_at=created_at)
    db.session.add(business)
    db.session.commit()
    return business

def add_review(business_name, review_text, created_by, created_at=datetime.datetime.utcnow()):
    review = Review(
        business_name = business_name,
        review_text = review_text,
        created_by = created_by,
        created_at = created_at)

    db.session.add(review)
    db.session.commit()
    return review