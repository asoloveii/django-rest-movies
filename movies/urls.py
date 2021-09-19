from django.urls.conf import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *


urlpatterns = format_suffix_patterns([
    path('movie/', MovieListView.as_view({'get': 'list'})),
    path('movie/<int:pk>/', MovieListView.as_view({'get': 'retrieve'})),
    path('review/', ReviewCreateView.as_view({'post': 'create'})),
    path('rating/', AddStarRatingView.as_view({'post': 'create'})),
    path('actors/', ActorsListView.as_view({'get': 'list'})),
    path('actors/<int:pk>/', ActorsListView.as_view({'get': 'retrieve'}))
])
