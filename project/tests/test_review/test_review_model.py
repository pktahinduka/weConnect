# project/tests/test_review_model.py


from project.tests.base import BaseTestCase
from project.tests.utils import add_review


class TestReviewModel(BaseTestCase):

    def test_add_review(self):
        review = add_review('1', 'Drarter Homes',
                            'I like the idea.', 'stillPeter')
        self.assertTrue(review.id)
        self.assertEqual(review.business_name, 'Drarter Homes')
        self.assertTrue(review.review_text, 'I like the idea.')
        self.assertTrue(review.created_by, 'stillPeter')
        self.assertTrue(review.created_at)
