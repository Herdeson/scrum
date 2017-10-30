from django.contrib.auth import get_user_model
from rest_framework import viewsets, authentication, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sprint, Task
from .serializers import SprintSerializers, TaskSerializer, UserSerializer
from .filters import TaskFilter, Sprintfilter
#227191803-0X
User = get_user_model()

# Create your views here.
class DefaultsMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )

    paginate_by = 25
    paginate_by_param ='page_size'
    max_paginate_by = 100



class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializers
    filter_class = Sprintfilter
    search_fields = ('name',)
    ordering_fields = ('end', 'name',)

class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'order', 'started', 'due', 'completed')
    filter_class = TaskFilter

class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields=(User.USERNAME_FIELD)
