from typing_extensions import Required
from django.shortcuts import render, get_object_or_404
from django_tables2 import SingleTableView, RequestConfig

from core.models import Answer, Student, Exercise, UserAnswerSummary
from .tables import AnswersTable, StudentTable, ExerciseTable, UserAnswerSummaryTable

class StudentListView(SingleTableView):
    model = Student
    table_class = StudentTable
    template_name = 'table.html'

class ExerciseListView(SingleTableView):
    model = Exercise
    table_class = ExerciseTable
    template_name = 'table.html'

def student_info(request, st_slug):
    student = get_object_or_404(Student, id = st_slug)
    filters = {
        'user': st_slug
    }
    answerssummary_table = UserAnswerSummaryTable(UserAnswerSummary.objects.filter(**filters))
    answers_table = AnswersTable(Answer.objects.filter(**filters))
    RequestConfig(request, paginate={"per_page": 5}).configure(answerssummary_table)
    RequestConfig(request, paginate={"per_page": 5}).configure(answers_table)

    answers = Answer.objects.filter(**filters)
    points = []
    submission_date = []
    for answer in answers.values():
        points.append(answer['points'])
        submission_date.append(answer['submission_date'].strftime("%m/%d/%Y %H:%M:%S"))

    return render(request, 'student.html', {
        'student': student, 
        'answers_table': answers_table, 
        'answerssummary_table': answerssummary_table,
        'answers': list(answers.values()),
        'points': list(points),
        'submission_date': list(submission_date)}
        )
