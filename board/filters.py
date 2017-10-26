import django_filters
from .models import Task, Sprint

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['sprint', 'status', 'assigned']
