import os
import unittest

from flask import json

from app import app, db, Repository
from config import BASE_DIR


def create_test_data():
    def insert(**kwargs):
        r = Repository(**kwargs)
        db.session.add(r)
        db.session.commit()

    insert(**{'full_name': 'python-test', 'language': 'Python'})
    insert(**{'full_name': 'ruby-test', 'language': 'Ruby'})
    insert(**{'full_name': 'java-test', 'language': 'Java'})


class TestAPIWithPagination(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['WITH_PAGINATION'] = '1'

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
            os.path.join(BASE_DIR, 'test.db'))
        db.create_all()
        self.client = app.test_client()
        self.path = '/api/v1.0/repositories'

    def tearDown(self):
        db.session.query(Repository).delete()

    def test_request_first_page(self):
        create_test_data()
        response = self.client.open(self.path + '?per_page=1')
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data().decode())
        self.assertTrue('page=2' in response_data['next'])
        self.assertTrue('page=3' in response_data['last'])
        self.assertEqual('', response_data['prev'])
        self.assertEqual(self.path, response_data['first'])

        self.assertEqual(1, len(response_data['repositories']))
        self.assertEqual('Python', response_data['repositories'][0]['language'])

    def test_request_middle_page(self):
        create_test_data()
        response = self.client.open(self.path + '?page=2&per_page=1')
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data().decode())
        self.assertTrue('page=3' in response_data['next'])
        self.assertTrue('page=3' in response_data['last'])
        self.assertTrue('page=1' in response_data['prev'])
        self.assertEqual(self.path, response_data['first'])

        self.assertEqual(1, len(response_data['repositories']))
        self.assertEqual('Ruby', response_data['repositories'][0]['language'])

    def test_request_last_page(self):
        create_test_data()
        response = self.client.open(self.path + '?page=3&per_page=1')
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data().decode())
        self.assertEqual('', response_data['next'])
        self.assertTrue('page=3' in response_data['last'])
        self.assertTrue('page=2' in response_data['prev'])
        self.assertEqual(self.path, response_data['first'])

        self.assertEqual(1, len(response_data['repositories']))
        self.assertEqual('Java', response_data['repositories'][0]['language'])

    def test_with_empty_database(self):
        response = self.client.open(self.path)
        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.get_data().decode())
        self.assertEqual(self.path, response_data['first'])
        self.assertEqual('', response_data['next'])
        self.assertEqual('', response_data['prev'])
        self.assertEqual(self.path + '?page=1', response_data['last'])

    def test_given_page_param_less_than_zero_returns_404(self):
        response = self.client.open(self.path + '?page=-42')
        self.assertEqual(404, response.status_code)

    def test_given_per_page_param_less_than_zero_returns_404(self):
        response = self.client.open(self.path + '?per_page=-42')
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
