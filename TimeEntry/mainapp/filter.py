from django.db.models import fields
import django_filters
from .models import *
from django_filters import DateFilter

class TaskFilter(django_filters.FilterSet):
    startTime = DateFilter(field_name='start_time',lookup_expr='icontains')
    class Meta:
        model = UserTask
        fields=['project']
