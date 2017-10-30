import django_filters
from .models import Task, Sprint

from django.contrib.auth import get_user_model

User = get_user_model()

class NullFilter(django_filters.BooleanFilter):
    """ Filtra de acordo com um campo definodo comonulo ou não."""

    def filter(self,qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name: value})


class TaskFilter(django_filters.FilterSet):
    backlog = NullFilter(name='sprint')

    class Meta:
        model = Task
        fields = ['sprint', 'status', 'assigned', 'backlog' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['assigned'].extra.update({'to_field_name': User.USERNAME_FIELD })

class Sprintfilter(django_filters.FilterSet):
    end_min = django_filters.DateFilter(name='end', lookup_expr='gte')
    end_max = django_filters.DateFilter(name='end', lookup_expr='lte')


    class Meta:
        model = Sprint
        fields =  ('end_min', 'end_max',)
