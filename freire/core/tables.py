import django_tables2 as tables
from core.models import Student, Exercise

class StudentTable(tables.Table):
    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "first_name", "last_name", "email", "is_active", "date_joined")

class ExerciseTable(tables.Table):
    class Meta:
        model = Exercise
        template_name = "django_tables2/bootstrap.html"
        fields = ("offering", "allow_submissions", "slug", "url", "topic", "group", "type")