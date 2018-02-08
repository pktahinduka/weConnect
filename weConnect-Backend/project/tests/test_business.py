# project/tests/test_items.py

import json
from project.tests.base import BaseTestCase
from project.api.business_models import Business 
from project import db, bcrypt
from project.tests.utils import add_business



class TestBusinessService(BaseTestCase):

    def test_add_business(self):
        """Ensure a new business can be added to the database."""
        with self.client:
            response = self.client.post(
                '/businesses',
                data=json.dumps(dict(
                    business_name='Drarter Homes',
                    business_category = 'Merchandise',
                    business_addr='Garden City Mall',
                    business_desc='Dealers in smart home technology.',
                    created_by='junekid'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Drarter Homes was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_business_invalid_json_object(self):
        """ Ensure error is thrown if the json object is empty """
        with self.client:
            response = self.client.post(
                '/businesses',
                data = json.dumps(dict()),
                content_type = 'json/application'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_business_invalid_json_object_quoted(self):
        """ Ensure error is thrown if the json object has empty quotes """
        with self.client:
            response = self.client.post(
                '/businesses',
                data = json.dumps(dict(
                    business_name='',
                    business_category='',
                    business_addr='',
                    business_desc='' 
                    )),
                content_type = 'json/application'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_business_invalid_json_key(self):
        """ Ensure error is thrown if the json object has no business id """
        with self.client:
            response = self.client.post(
                '/businesses',
                data = json.dumps(dict(business_name='Drarter Homes')),
                content_type = 'json/application'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_business_duplicate_business_name(self):
        """ Ensure error is thrown if the business name already exists."""
        with self.client:
            self.client.post(
            '/businesses',
            data=json.dumps(dict(
                business_name='Drarter Homes',
                business_category = 'Merchandise',
                business_addr='Garden City Mall',
                business_desc='Dealers in smart home technology.',
                created_by='junekid'
            )),
            content_type='application/json',
        )
            response = self.client.post(
            '/businesses',
            data=json.dumps(dict(
                business_name='Drarter Homes',
                business_category = 'Merchandise',
                business_addr='Garden City Mall',
                business_desc='Dealers in smart home technology.',
                created_by='junekid'
            )),
            content_type='application/json',
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Sorry. The business already exists on the list.', data['message'])
        self.assertIn('fail', data['status'])

    def test_single_business(self):
        """ Ensure that the get business route behaves correctly """
        business = add_business('Drarter Homes', 'Merchandise','Garden City Mall', 'Dealers in smart home technology.', 'junekid')
        db.session.add(business)
        db.session.commit()

        with self.client:
            response = self.client.get(f'/businesses/{business.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('Drarter Homes', data['data']['business_name'])
            self.assertEqual('Merchandise', data['data']['business_category'])
            self.assertIn('success', data['status'])         
    
    def test_single_business_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/businesses/nada')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Business does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_business_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/businesses/911')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Business does not exist', data['message'])
            self.assertIn('fail', data['status'])
    
    def test_all_businesses(self):
        """Ensure get all businesses route behaves correctly."""
        add_business('Drarter Homes', 'Merchandise','Garden City Mall', 
            'Dealers in smart home technology.', 'junekid')
        add_business('weConnect', 'Services','Freedom City Mall', 
            'Connecting businesses with client feedback', 'stillPeter')
        with self.client:
            response = self.client.get('/businesses')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['businesses']), 2)
            self.assertTrue('created_at' in data['data']['businesses'][0])
            self.assertTrue('created_at' in data['data']['businesses'][1])
            self.assertIn('Drarter Homes', data['data']['businesses'][0]['business_name'])
            self.assertEqual(
            'Merchandise', data['data']['businesses'][0]['business_category'])
            self.assertIn('weConnect', data['data']['businesses'][1]['business_name'])
            self.assertEqual(
            'Services', data['data']['businesses'][1]['business_category'])
            self.assertIn('success', data['status'])