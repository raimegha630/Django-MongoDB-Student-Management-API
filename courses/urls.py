from django.urls import path
from .views import *

urlpatterns = [
    path('',create_courses),
    path('all/', list_courses),
    path('<str:id>/',get_courses),
    path('update/<str:id>/',update_course),
    path('delete/<str:id>/',delete_course) 
]