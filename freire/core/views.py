from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import SingleTableView

from core.models import Student, Exercise
from .tables import StudentTable, ExerciseTable

class StudentListView(SingleTableView):
    model = Student
    table_class = StudentTable
    template_name = 'table.html'

class ExerciseListView(SingleTableView):
    model = Exercise
    table_class = ExerciseTable
    template_name = 'table.html'