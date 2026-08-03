from django.urls import path
from.views import top_students
from.views import average_marks
from.views import student_per_course
from.views import students_course_details

urlpatterns = [
    path('top-students/', top_students, name='top_students'),
    path('average-marks/', average_marks, name='average_marks'),
    path('students-per-course/', student_per_course, name='students_per_course'),
    path('students-course-details/', students_course_details, name='students_course_details')

]