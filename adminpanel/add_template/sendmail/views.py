
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.views.generic.list import BaseListView
from django.core.paginator import Paginator
