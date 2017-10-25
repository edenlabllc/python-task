import webtest
from flask import json
from flask.helpers import url_for
from pytest import raises


class TestAPIWithPagination:
    def test_request_first_page(self, repositories, testapp):
        url = url_for('repository.get_repositories') + '?per_page=1'
        response = testapp.get(url)
        response_data = json.loads(response.body.decode())
        
        assert response.status_code == 200
        assert 'page=2' in response_data['next']
        assert 'page=3' in response_data['last']
        assert '' in response_data['prev']
        assert url_for('repository.get_repositories') in response_data['first']
        assert len(response_data['repositories']) == 1
        assert response_data['repositories'][0]['language'] == 'Python'

    def test_request_middle_page(self, repositories, testapp):
        url = url_for('repository.get_repositories') + '?page=2&per_page=1'
        response = testapp.get(url)
        response_data = json.loads(response.body.decode())
        
        assert response.status_code == 200
        assert 'page=3' in response_data['next']
        assert 'page=3' in response_data['last']
        assert 'page=1' in response_data['prev']
        assert url_for('repository.get_repositories') == response_data['first']
        assert len(response_data['repositories']) == 1  # as we requested one item per page
        assert response_data['repositories'][0]['language'] == 'Ruby'

    def test_request_last_page(self, repositories, testapp):
        url = url_for('repository.get_repositories') + '?page=3&per_page=1'
        response = testapp.get(url)
        response_data = json.loads(response.body.decode())

        assert response.status_code == 200
        assert response_data['next'] == ''
        assert 'page=3' in response_data['last']
        assert 'page=2' in response_data['prev']
        assert url_for('repository.get_repositories') == response_data['first']
        assert len(response_data['repositories']) == 1  # as we requested one item per page
        assert response_data['repositories'][0]['language'] == 'Java'

    def test_with_empty_database(self, db, testapp):
        response = testapp.get(url_for('repository.get_repositories'))
        response_data = json.loads(response.body.decode())

        assert response.status_code == 200
        assert url_for('repository.get_repositories') == response_data['first']
        assert response_data['next'] == ''
        assert response_data['prev'] == ''
        assert response_data['last'] == '{}?{}={}'.format(
            url_for('repository.get_repositories'),
            'page', 1)

    def test_given_page_param_less_than_zero_returns_404(self, db, testapp):
        url = '{}?{}={}'.format(url_for('repository.get_repositories'),
                                'page', -42)
        raises(webtest.app.AppError, testapp.get, url)

    def test_given_per_page_param_less_than_zero_returns_404(self, db, testapp):
        url = '{}?{}={}'.format(url_for('repository.get_repositories'),
                                'per_page', -42)
        raises(webtest.app.AppError, testapp.get, url)

