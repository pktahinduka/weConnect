# project/api/views.py

from flask import Blueprint, jsonify, request, render_template
from project.api.user_models import User
from project.api.user_models import BlacklistToken
from project.api.business_models import Business
from project.api.review_models import Review
from project import db
from sqlalchemy import exc, or_

users_blueprint = Blueprint('users_blueprint', __name__, template_folder='./templates')

@users_blueprint.route('/home')
def main():
    return render_template('shopeasy_index.html')

@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(username=username, email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users = users)



@users_blueprint.route('/ping', methods = ['GET'])
def ping_pong():
    return jsonify({
    'status' : 'success',
    'message' : 'pong!'
    })

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(
                username=username,
                email=email,
                password=password))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

@users_blueprint.route('/businesses', methods=['POST'])
def add_business():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    business_name = post_data.get('business_name')
    business_category = post_data.get('business_category')
    business_addr = post_data.get('business_addr')
    business_desc = post_data.get('business_desc')
    created_by = post_data.get('created_by')
    created_at = post_data.get('created_at')

    try:
        business = Business.query.filter_by(business_name=business_name).first()
        if not business:
            db.session.add(Business(
                business_name=business_name,
                business_category=business_category,
                business_addr=business_addr,
                business_desc=business_desc,
                created_by=created_by,
                created_at=created_at))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{business_name} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. The business already exists on the list.'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

@users_blueprint.route('/reviews', methods=['POST'])
def add_review():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    business_name = post_data.get('business_name')
    review_text = post_data.get('review_text')
    created_by = post_data.get('created_by')
    created_at = post_data.get('created_at')

    try:
        review = Review.query.filter_by(review_text=review_text).first()
        if not review:
            db.session.add(Review(
                business_name=business_name,
                review_text=review_text,
                created_by=created_by,
                created_at=created_at))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'A review for {business_name} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. Someone already posted this exact review.'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                  'username': user.username,
                  'email': user.email,
                  'created_at': user.created_at
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/businesses/<biz_id>', methods=['GET'])
def get_single_business(biz_id):
    """Get single business details"""
    response_object = {
        'status': 'fail',
        'message': 'Business does not exist'
    }
    try:
        business = Business.query.filter_by(id=int(biz_id)).first()
        if not business:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                  'business_name': business.business_name,
                  'business_category': business.business_category,
                  'business_addr': business.business_addr,
                  'business_desc': business.business_desc,
                  'created_by': business.created_by,
                  'created_at': business.created_at
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = User.query.all()
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        users_list.append(user_object)
    response_object = {
        'status': 'success',
        'data': {
            'users': users_list
        }
    }
    return jsonify(response_object), 200

@users_blueprint.route('/businesses', methods=['GET'])
def get_all_businesses():
    """Get all businesses"""
    businesses = Business.query.all()
    businesses_list = []
    for business in businesses:
        business_object = {
            'id': business.id,
            'business_name': business.business_name,
            'business_category': business.business_category,
            'business_addr': business.business_addr,
            'business_desc': business.business_desc,
            'created_by': business.created_by,
            'created_at': business.created_at
        }
        businesses_list.append(business_object)
    response_object = {
        'status': 'success',
        'data': {
            'businesses': businesses_list
        }
    }
    return jsonify(response_object), 200

@users_blueprint.route('/reviews', methods=['GET'])
def get_all_reviews():
    """Get all reviews"""
    reviews = Review.query.all()
    reviews_list = []
    for review in reviews:
        review_object = {
            'id': review.id,
            'business_name': review.business_name,
            'review_text': review.review_text,
            'created_by': review.created_by,
            'created_at': review.created_at
        }
        reviews_list.append(review_object)
    response_object = {
        'status': 'success',
        'data': {
            'reviews': reviews_list
        }
    }
    return jsonify(response_object), 200




