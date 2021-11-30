from django.urls import path

from .views import *
from . import class_views


urlpatterns = [
    path('', index),
    path('search/', class_views.SearchResultsView.as_view(), name='search-results'),
]
