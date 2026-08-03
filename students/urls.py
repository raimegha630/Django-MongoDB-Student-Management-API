from django.urls import path
from .views import *


urlpatterns = [
    path('',create_students),
    path('all/', list_students),

    path('single-index/',single_index),
    path('multi-key/',multi_key_index),
    path('compound-index/',compount_index),

    path('<str:id>/',get_students),
    path('update/<str:id>/',update_student),
    path('delete/<str:id>/',delete_student),
    path('<str:id>/assign-course/',assign_course),
    path('<str:id>/add-profile/',add_profile)
]