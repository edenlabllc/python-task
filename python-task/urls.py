from django.conf.urls import include, url
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='repositories', permanent=False)),
    url(r'^repositories/', include('githubsearch_api.urls')),
]