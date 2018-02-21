# project/tests/test_items.py

import json
from project.tests.base import BaseTestCase
from project.api.business_models import Business 
from project import db, bcrypt
from project import create_app
from project.tests.utils import add_business
from project.tests.utils import add_user



class TestBusinessService(BaseTestCase):

    def test_add_business(self):
        """Ensure a new business can be added to the database."""

        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

        with self.client:
            response = self.client.post(
                '/api/businesses',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
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


        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

        with self.client:
            response = self.client.post(
                '/api/businesses',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
                data = json.dumps(dict()),
                content_type = 'json/application'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_business_invalid_json_object_quoted(self):
        """ Ensure error is thrown if the json object has empty quotes """

        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

        with self.client:
            response = self.client.post(
                '/api/businesses',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
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
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
        with self.client:
            response = self.client.post(
                '/api/businesses',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
                data = json.dumps(dict(business_name='Drarter Homes')),
                content_type = 'json/application'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_business_duplicate_business_name(self):
        """ Ensure error is thrown if the business name already exists."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
        with self.client:
            self.client.post(
            '/api/businesses',
            headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
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
            '/api/businesses',
            headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
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

        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

        with self.client:
            response = self.client.get(f'/api/businesses/{business.id}',
                       headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('Drarter Homes', data['data']['business_name'])
            self.assertEqual('Merchandise', data['data']['business_category'])
            self.assertIn('success', data['status'])         
    
    def test_single_business_no_id(self):
        """Ensure error is thrown if an id is not provided."""

        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

        with self.client:
            response = self.client.get('/api/businesses/nada',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode())['auth_token']))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Business does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_business_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""

        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

        with self.client:
            response = self.client.get('/api/businesses/911',
                        headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode())['auth_token']))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Business does not exist', data['message'])
            self.assertIn('fail', data['status'])
    
    def test_all_businesses(self):
        """Ensure get all businesses route behaves correctly."""

        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

        add_business('Drarter Homes', 'Merchandise','Garden City Mall', 
            'Dealers in smart home technology.', 'junekid')
        add_business('weConnect', 'Services','Freedom City Mall', 
            'Connecting businesses with client feedback', 'stillPeter')
        with self.client:
            response = self.client.get('/api/businesses',
                        headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode())['auth_token']))
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

    def test_business_editing(self):
        """
        Test that we can edit the name of a business
        """
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
        with self.client:
            response = self.client.post(
                '/api/businesses',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
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

        with self.client:
            response = self.client.put(
                '/api/businesses/1',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
                data=json.dumps(dict(
                    business_name='Drarter Homes, Inc.',
                    business_category = 'Merchandise Services',
                    business_addr='Garden City Mall',
                    business_desc='Dealers in smart home technology.',
                    created_by='junekid'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)


    def test_business_deletion(self):
        """
        Test that a business list can be deleted
        """
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
        with self.client:
            response = self.client.post(
                '/api/businesses',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']),
                data=json.dumps(dict(
                    business_name='Drarter Homes, Inc.',
                    business_category = 'Merchandise Services',
                    business_addr='Garden City Mall',
                    business_desc='Dealers in smart home technology.',
                    created_by='junekid'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

        # Confirm that the business has been deleted
        with self.client:
            response = self.client.delete(
                '/api/businesses/1',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']))
            self.assertEqual(response.status_code, 204)


