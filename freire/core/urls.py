from django.urls import path
from freire.core import views

urlpatterns = [
    path('students/', views.StudentListView.as_view(), name='students'),
    path('exercises/', views.ExerciseListView.as_view(), name='exercises'),
]