from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, pagination
from githubsearch_api.models import Repository
from githubsearch_api.serializers import RepositorySerializer


class SrandardResultsSetPagination(pagination.PageNumberPagination):
    """
    Pagination for repositories.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 150


class RepositoriesList(generics.ListAPIView):
    """
    List of repositories.

    Return the first 100 repositories ordered by the stargazers_count from lowest value to largest.
    Allow page number pagination.
    """
    queryset = Repository.objects.order_by('stargazers_count')
    serializer_class = RepositorySerializer
    pagination_class = SrandardResultsSetPagination
