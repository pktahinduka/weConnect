# project/api/views.py

from functools import wraps

from flask import Blueprint, jsonify, request, render_template, make_response
from project.api.user_models import User
from project.api.business_models import Business
from project.api.review_models import Review
from project import db
from sqlalchemy import exc, or_

users_blueprint = Blueprint('users_blueprint', __name__, template_folder='./templates')

def token_required(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        # Check for the authentication token
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            # If there's no token provided
            response = {
                "message": "Please register or login to access this resource!"
            }
            return make_response(jsonify(response)), 401

        else:
            access_token = auth_header.split(" ")[1]
            if access_token:
                # Attempt to decode the token and get the user id
                user_id = User.decode_auth_token(access_token)

                if isinstance(user_id, str):
                    # User id does not exist so payload is an error message
                    message = user_id
                    response = jsonify({
                        "message": message
                    })

                    response.status_code = 401
                    return response

                else:
                    return func(user_id=user_id, *args, **kwargs)
            else:
                response = {
                    "message": "Register or log in to access this resource"
                }
                return make_response(jsonify(response)), 401

    return func_wrapper

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

@users_blueprint.route('/api/businesses', methods=['POST'])
@token_required
def add_business(user_id):
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

@users_blueprint.route('/api/businesses/<businessId>/reviews', methods=['POST'])
@token_required
def add_review(user_id, businessId):
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    id = post_data.get('id')
    business_id = post_data.get('business_id')
    business_name = post_data.get('business_name')
    review_text = post_data.get('review_text')
    created_by = post_data.get('created_by')
    created_at = post_data.get('created_at')

    try:
        review = Review.query.filter_by(id=id).first()
        if not review:
            db.session.add(Review(
                business_id=business_id,
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


@users_blueprint.route('/api/businesses/<biz_id>', methods=['GET'])
@token_required
def get_single_business(user_id, biz_id):
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

@users_blueprint.route('/api/businesses/<businessId>/reviews', methods=['GET'])
@token_required
def get_single_business_reviews(user_id, businessId):
    """Get all reviews"""
    reviews = Review.query.filter_by(business_id = businessId)
    reviews_list = []
    for review in reviews:
        review_object = {
            'id': review.id,
            'business_id': review.business_id,
            'business_name': review.business_name,
            'review_text': review.review_text,
            'created_by': review.created_by,
            'created_at': review.created_at
        }
        reviews_list.append(review_object)

    if reviews_list == []:
        response_object = {
            'status': 'sucess',
            'message': 'This business currently has no reviews.'
        }    
        return jsonify(response_object), 200
    else:
        response_object = {
            'status': 'success',
            'data': {
                'reviews': reviews_list
            }
        }
        return jsonify(response_object), 200


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

@users_blueprint.route('/api/businesses', methods=['GET'])
@token_required
def get_all_businesses(user_id):
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

@users_blueprint.route("/api/businesses/<biz_id>", methods=['PUT', 'DELETE'])
@token_required
def manipulate_a_business(biz_id, user_id, *args, **kwargs):
    business = Business.query.filter_by(id=biz_id).first()
    if not business:
        response_object = {
        'status': 'fail',
        'message': 'Business does not exist'
        }
        return jsonify(response_object), 404

    if request.method == "DELETE":
        business.delete()
        response_object = {
        'status': 'success',
        'message': 'A business has been successfully deleted'
         }
    
        return jsonify(response_object), 204 

    elif request.method == "PUT":
        all_businesses = Business.query.filter_by(id=biz_id).first()

        business_name = request.get_json()['business_name']
        business_category = request.get_json()['business_category']
        business_addr = request.get_json()['business_addr']
        business_desc = request.get_json()['business_desc']
        created_by = request.get_json()['created_by']

        business.business_name = business_name
        business.business_category = business_category
        business.business_addr = business_addr
        business.business_desc = business_desc
        business.created_by = created_by

        business.save()

        response = jsonify({
            "id": business.id,
            "name": business.business_name,
            "category": business.business_category,
            "address": business.business_addr, 
            "date_created": business.created_at,
            "created_by": business.created_by
        })

        response.status_code = 201
        return response

    else:
        response = jsonify({
            "message": "There is an existing business with the same name. Try again"
                                })
        response.status_code = 409
        return response






    


