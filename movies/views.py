from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorSerializer,
    ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter, PaginationMovies


class MovieListView(viewsets.ReadOnlyModelViewSet):

    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter
    pagination_class = PaginationMovies

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Case(
                models.When(ratings__ip=get_client_ip(self.request), then=True),
                default=False,
                output_field=models.BooleanField()
            ),
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class MovieDetailView(generics.RetrieveAPIView):

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(viewsets.ModelViewSet):

    serializer_class = ReviewCreateSerializer


class AddStarRatingView(viewsets.ModelViewSet):

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(viewsets.ReadOnlyModelViewSet):

    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer


class ActorDetailView(generics.RetrieveAPIView):

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
