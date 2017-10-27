from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RepositoriesTests(APITestCase):
    fixtures = ['repositories.json']

    def test_list_repositories(self):
        """
        Ensure we can list repositories.
        """
        url = reverse('repositories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Fixture has only 973 repositories.
        self.assertEqual(response.data['count'], 973)

        # This must be the first page.
        self.assertEqual(response.data['previous'], None)

        # This endpoint must return only 100 repositories.
        self.assertEqual(len(response.data['results']), 100)

    def test_list_repositories_paging(self):
        """
        Ensure we can use paging.
        """
        url = reverse('repositories-list')
        response = self.client.get(url + '?page=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 73)