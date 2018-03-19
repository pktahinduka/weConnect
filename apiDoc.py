from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='weConnect RESTful API',
    description='A documentation of the backend flask RESTful API for weConnect.',
)

ns = api.namespace('api/', description='weConnect operations')

business = api.model('Business', {
    'id': fields.Integer(readOnly=True, description='The business unique identifier'),
    'business_name': fields.String(required=True, description='The Business Name'),
    'business_category': fields.String(required=True, description='The Business Category'),
    'business_addr': fields.String(required=True, description='The Business Address'),
    'business_desc': fields.String(required=True, description='A Business Description'),
    'created_by': fields.String(required=True, description='The Author/creator of the business'),
})


class BusinessDAO(object):
    def __init__(self):
        self.counter = 0
        self.businesses = []

    def get(self, id):
        for business in self.businesses:
            if business['id'] == id:
                return business
        api.abort(404, "Business {} doesn't exist".format(id))

    def create(self, data):
        business = data
        business['id'] = self.counter = self.counter + 1
        self.businesses.append(business)
        return business

    def update(self, id, data):
        business = self.get(id)
        business.update(data)
        return business

    def delete(self, id):
        business = self.get(id)
        self.businesses.remove(business)


DAO = BusinessDAO()
DAO.create({'business_name': 'Drarter',
            'business_category': 'Manufacturing Industry',
            'business_addr': 'Kampala, Uganda',
            'business_desc': 'Awesome services in tech',
            'created_by': 'stillPeter'})
DAO.create({'business_name': 'Roofings Ltd',
            'business_category': 'Manufacturing Industry',
            'business_addr': 'Kampala, Uganda',
            'business_desc': 'Awesome services in manufacture',
            'created_by': 'stillPeter'})
DAO.create({'business_name': 'Uzeland Inc.',
            'business_category': 'Agriculture',
            'business_addr': 'Kampala, Uganda',
            'business_desc': 'Farming is the way to go.',
            'created_by': 'stillPeter'})


@ns.route('/businesses')
class BusinessList(Resource):
    '''Shows a list of all businesses, and lets you POST to add new businesses'''
    @ns.doc('list_businesses')
    @ns.marshal_list_with(business)
    def get(self):
        '''List all businesses'''
        return DAO.businesses

    @ns.doc('create_business')
    @ns.expect(business)
    @ns.marshal_with(business, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/businesses/<int:id>')
@ns.response(404, 'Business not found')
@ns.param('id', 'The business identifier')
class Business(Resource):
    '''Show a single business and lets you delete them'''
    @ns.doc('get_business')
    @ns.marshal_with(business)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_business')
    @ns.response(204, 'Business deleted')
    def delete(self, id):
        '''Delete a business given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(business)
    @ns.marshal_with(business)
    def put(self, id):
        '''Update a business given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)