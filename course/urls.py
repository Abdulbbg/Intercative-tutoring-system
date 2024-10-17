from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('course-selection/', views.course_selection_view, name='course-selection'),
    path('course-content/', views.course_content_view, name='course-content'),
]
