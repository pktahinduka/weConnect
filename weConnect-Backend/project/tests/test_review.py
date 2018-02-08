import json
from project.tests.base import BaseTestCase
from project.api.review_models import Review 
from project import db, bcrypt
from project.tests.utils import add_review



class TestReviewService(BaseTestCase):

    def test_add_review(self):
        """Ensure a new review can be added to the database."""
        with self.client:
            response = self.client.post(
                '/reviews',
                data=json.dumps(dict(
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
        with self.client:
            response = self.client.post(
            '/reviews',
            data=json.dumps(dict()),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_review_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a business name key."""
        with self.client:
            response = self.client.post(
            '/reviews',
            data=json.dumps(dict(review_text='I like the idea.')),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_review_duplicate_review(self):
        """ Ensure error is thrown if the review already exists."""
        with self.client:
            self.client.post(
            '/reviews',
            data=json.dumps(dict(
                business_name='Drarter Homes',
                review_text = 'I like the idea.',
                created_by ='stillPeter'
            )),
            content_type='application/json',
        )
            response = self.client.post(
            '/reviews',
            data=json.dumps(dict(
                business_name='Drarter Homes',
                review_text = 'I like the idea.',
                created_by ='stillPeter'
            )),
            content_type='application/json',
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Sorry. Someone already posted this exact review.', data['message'])
        self.assertIn('fail', data['status'])

    def test_all_reviews(self):
        """Ensure get all reviews behaves correctly."""
        add_review('Drarter Homes', 'Cool Stuff.','stillPeter')
        add_review('AfroDjango', 'Dream in Python','fletcher')
        with self.client:
            response = self.client.get('/reviews')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['reviews']), 2)
            self.assertTrue('created_at' in data['data']['reviews'][0])
            self.assertTrue('created_at' in data['data']['reviews'][1])
            """self.assertIn('michael', data['data']['users'][0]['username'])
            self.assertIn(
            'michael@realpython.com', data['data']['users'][0]['email'])
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn(
            'fletcher@realpython.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status']) """   

    def test_add_review_invalid_json_keys_no_author(self):
        """Ensure error is thrown if the JSON object does not have an author."""
        with self.client:
            response = self.client.post(
                '/reviews',
                data=json.dumps(dict(
                    business_name='Drarter Homes',
                    review_text='I like the idea.')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])





