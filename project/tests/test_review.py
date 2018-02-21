import json
from project.tests.base import BaseTestCase
from project.api.review_models import Review 
from project import db, bcrypt
from project.tests.utils import add_review
from project.tests.utils import add_user



class TestReviewService(BaseTestCase):

    def test_add_review(self):
        """Ensure a new review can be added to the database."""

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
                '/api/businesses/1/reviews',
                headers=dict(Authorization='Bearer ' + json.loads(
                        resp_login.data.decode())['auth_token']),
                data=json.dumps(dict(
                    business_id='1',
                    business_name='Drarter Homes',
                    review_text = 'I like the idea.',
                    created_by ='stillPeter'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('A review for Drarter Homes was added!', data['message'])
            self.assertIn('success', data['status'])


    def test_add_review_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""

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
            '/api/businesses/1/reviews',
            headers=dict(Authorization='Bearer ' + json.loads(
                resp_login.data.decode())['auth_token']),
            data=json.dumps(dict()),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_review_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a business name key."""
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
            '/api/businesses/1/reviews',
            headers=dict(Authorization='Bearer ' + json.loads(
                resp_login.data.decode())['auth_token']),
            data=json.dumps(dict(review_text='I like the idea.')),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_review_invalid_json_keys_no_author(self):
        """Ensure error is thrown if the JSON object does not have an author."""
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
                '/api/businesses/1/reviews',
            headers=dict(Authorization='Bearer ' + json.loads(
                resp_login.data.decode())['auth_token']),
                data=json.dumps(dict(
                    business_id='1',
                    business_name='Drarter Homes',
                    review_text='I like the idea.')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])





