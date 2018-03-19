# project/tests/test_business_model.py

from project.tests.base import BaseTestCase
from project.tests.utils import add_business


class TestBusinessModel(BaseTestCase):

    def test_add_business(self):
        business = add_business('Drarter Homes', 'Technology', 'Garden City Mall',
                                'Dealers in smart home technology.', 'junekid')
        self.assertTrue(business.id)
        self.assertEqual(business.business_name, 'Drarter Homes')
        self.assertEqual(business.business_category, 'Technology')
        self.assertTrue(business.business_addr, 'Garden City Mall')
        self.assertTrue(business.business_desc,
                        'Dealers in smart home technology.')
        self.assertTrue(business.created_by, 'junekid')
        self.assertTrue(business.created_at)
