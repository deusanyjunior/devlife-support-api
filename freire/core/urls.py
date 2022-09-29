from django.urls import path
from freire.core import views

urlpatterns = [
    path('students/', views.StudentListView.as_view(), name='students'),
    path('student/<slug:st_slug>/', views.student_info, name='student' ),
    # path('exercises/', views.ExerciseListView.as_view(), name='exercises'),
    path('exercises/', views.exercises, name='exercises'),
    path('exercise/<slug:ex_slug>/', views.exercise_info, name='exercise' )
]