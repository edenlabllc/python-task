
from django.conf.urls import url
from githubsearch_api import views

urlpatterns = [
    url(r'^$', views.RepositoriesList.as_view(), name='repositories-list'),
]
