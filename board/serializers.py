from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Sprint, Task
from rest_framework.reverse import reverse
from datetime import date
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class SprintSerializers(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail', kwargs={'pk': obj.pk}, request=request),
            'tasks': reverse('task-list', request=request)+ '?sprint={}'.format(obj.pk),
        }

    def validate_end(self, value):
        end_date = value

        if (end_date < date.today()):
            msg = _('End date cannot be in the past.')
            raise serializers.ValidationError(msg)
        return value



class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status', 'status_display',
                'order', 'assigned', 'started', 'due', 'completed', 'links', )

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('task-detail', kwargs={'pk': obj.pk}, request=request),
        }

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model= User
        fields=('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        return {
            'self': reverse('user-detail',
             kwargs={User.USERNAME_FIELD: username }, request=request),
        }
