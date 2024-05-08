from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.group_list),
    path('group-create/', views.group_create),
    path('search/', views.search_groups),
]
