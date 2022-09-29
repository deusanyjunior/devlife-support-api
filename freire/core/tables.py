import django_tables2 as tables
from core.models import Answer, Student, Exercise, UserAnswerSummary

class StudentTable(tables.Table):
    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "username", "first_name", "last_name", "email", "is_active", "date_joined")
        row_attrs = {
            'onClick': lambda record: "document.location.href='/freire/student/{0}/';".format(record.id)
        }

class UserAnswerSummaryTable(tables.Table):
    class Meta:
        model = UserAnswerSummary
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "exercise", "max_points", "answer_count", "latest")

class AnswersTable(tables.Table):
    class Meta:
        model = Answer
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "exercise", "points", "submission_date", "test_results")


class ExerciseTable(tables.Table):
    class Meta:
        model = Exercise
        template_name = "django_tables2/bootstrap4.html"
        fields = ("offering", "allow_submissions", "slug", "url", "topic", "group", "type")
        row_attrs = {
            'onClick': lambda record: "document.location.href='/freire/exercise/{0}/';".format(record.id)
        }
