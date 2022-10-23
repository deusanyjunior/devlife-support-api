from typing_extensions import Required
from django.shortcuts import render, get_object_or_404
from django_tables2 import SingleTableView, RequestConfig

from core.models import Answer, Offering, Student, Exercise, UserAnswerSummary
from .tables import AnswersTable, StudentTable, ExerciseTable, UserAnswerSummaryTable

from collections import OrderedDict

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

def exercises(request):
    offerings = list(Offering.objects.all().values())

    exercises = Exercise.objects.all().values()
    groups = exercises.values_list('group', flat=True).distinct()
    topics = exercises.values_list('topic', flat=True).distinct()
    types = exercises.values_list('type', flat=True).distinct()

    offering = request.GET.get('offering', False)
    if offering == False:
        offering = offerings[len(offerings) -1 ]['id']
    group = request.GET.get('group', False)
    if group == False:
        group = groups[0]
    topic = request.GET.get('topic', False)
    if topic == False:
        topic = topics[0]
    type = request.GET.get('type', False)
    if type == False:
        type = types[0]

    filters = {
        'offering': offering,
        'topic': topic,
        'group': group,
        'type': type
    }

    exercises_table = ExerciseTable(Exercise.objects.filter(**filters))
    RequestConfig(request, paginate={"per_page": 10}).configure(exercises_table)

    exercises_list = Exercise.objects.filter(**filters)
    exercises_data = {}
    for exercise in exercises_list:
        points, days, dataset = get_exercises_answers(exercise, 'day')
        exercises_data[exercise] = {
            'id': exercise.id,
            'points': points,
            'days': days,
            'dataset': dataset
        }

    return render(request, 'exercises.html', {
        'offering': offering,
        'offerings': offerings,
        'groups': list(groups),
        'group': group,
        'topics': list(topics),
        'topic': topic,
        'types': list(types),
        'type': type,
        'exercises_table': exercises_table,
        'exercises_list': list(exercises_list.values()),
        'exercises_data': exercises_data
    })

def exercise_info(request, ex_slug):
    scales = ['day','hour','minute']
    #TODO: consider scale
    scale = request.POST.get('scale', False)
    if scale == False:
        scale = scales[0]

    exercise = get_object_or_404(Exercise, id = ex_slug)
    points, days, dataset = get_exercises_answers(ex_slug, scale)

    return render(request, 'exercise.html', {
        'exercise': exercise,
        'points': points,
        'days': days,
        'dataset': dataset
    })

def get_exercises_answers(ex_slug, scale):
    filters = {
        'exercise': ex_slug
    }
    answers = Answer.objects.filter(**filters)

    # points
    points = {}
    submissions = {}
    for answer in answers.values():
        point_adjusted = adjust_point(answer['points'])
        if answer['points'] not in points.keys():
            points[point_adjusted] = 1
        else:
            points[point_adjusted] += 1
        if scale == 'day':
            day = answer['submission_date'].strftime("%d/%m/%Y")
            if day not in submissions.keys():
                submissions[ day ] = {
                    point_adjusted : 1
                }
            else:
                if answer['points'] not in submissions[ day ].keys():
                    submissions[ day ][point_adjusted] = 1
                else:
                    submissions[ day ][point_adjusted] += 1
    
    points = OrderedDict(sorted(points.items(),reverse=True))
    days = list(submissions.keys())
    points_list = []
    for submission in submissions.values():
        for point in submission.keys():
            if point not in points_list:
                points_list.append(point)
                
    points_list.sort(reverse=True)
    dataset = {}
    for point in points_list:
        dataset[ point ] = []
    for day in days:
        for point in points_list:
            if point in submissions[ day ].keys():
                dataset[ point ].append( submissions[day][point] )
            else:
                dataset[ point ].append( 0 )
    return points, days, dataset


def adjust_point(point):
    if point >= 1:
        return "1.0"
    elif point > 0.66 and point < 1:
        return "0.99"
    elif point > 0.33 and point <= 0.66:
        return "0.66"
    elif point > 0 and point <= 0.33:
        return "0.33"
    else: 
        return "0.0"

def points_scale():
    return "1,"
