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
    topics = exercises.values_list('topic', flat=True).distinct()
    groups = exercises.values_list('group', flat=True).distinct()
    types = exercises.values_list('type', flat=True).distinct()
    scales = scales_list()

    topic_classes = {}
    for top in topics:
        divider = 0
        try: 
            divider = top.index('/')
        except:
            divider = len(top)
        topclass = top[:divider]
        if divider == len(top): 
            topelem = '-'
        else:
            topelem = top[divider+1:]
        if topclass not in topic_classes.keys():
            topic_classes[topclass] = []
        if topelem not in topic_classes[topclass] :
            topic_classes[topclass].append(topelem)

    offering = request.GET.get('offering', False)
    if offering == False:
        offering = offerings[len(offerings) -1 ]['id']
    group = request.GET.get('group', False)
    if group == False:
        group = groups[0]
    topic_class = request.GET.get('topic_class', False)
    if topic_class == False:
        topic_class = list(topic_classes.keys())[0]
    topic_item = request.GET.get('topic_item', False)
    if topic_item == False:
        topic_item = topic_classes[topic_class][0]
    type = request.GET.get('type', False)
    if type == False:
        type = types[0]
    scale = request.GET.get('scale', False)
    if scale == False:
        scale = scales[0]

    topic_filter = topic_class
    if topic_item != '-':
        topic_filter += '/' + topic_item
    filters = {
        'offering': offering,
        'topic': 'python/for',
        'group': group,
        'type': type
    }

    exercises_list = Exercise.objects.filter(**filters)
    exercises_table = ExerciseTable(exercises_list)
    RequestConfig(request, paginate={"per_page": 10}).configure(exercises_table)

    exercises_data = {}
    for exercise in exercises_list:
        points, days, dataset = get_exercises_answers(exercise, scale)
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
        'topics_items': topic_classes,
        'topic_class': topic_class,
        'topic_item': topic_item,
        'topic_classes': list(topic_classes.keys()),
        'topic_items': list(topic_classes[topic_class]),
        'types': list(types),
        'type': type,
        'scales': list(scales),
        'scale': scale,
        'exercises_table': exercises_table,
        'exercises_list': list(exercises_list.values()),
        'exercises_data': exercises_data
    })

def exercise_info(request, ex_slug):
    scales = scales_list()
    scale = request.GET.get('scale', False)
    if scale == False:
        scale = scales[0]

    exercise = get_object_or_404(Exercise, id = ex_slug)
    points, days, dataset = get_exercises_answers(ex_slug, scale)

    return render(request, 'exercise.html', {
        'exercise': exercise,
        'points': points,
        'days': days,
        'dataset': dataset,
        'scales': scales,
        'scale': scale
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
        if point_adjusted not in points.keys():
            points[point_adjusted] = 1
        else:
            points[point_adjusted] += 1
        
        timescale = ''
        if scale == 'weekly':
            timescale = answer['submission_date'].strftime("%U")
        elif scale == 'dayly':
            timescale = answer['submission_date'].strftime("%d/%m/%Y")
        elif scale == 'hourly':
            timescale = answer['submission_date'].strftime("%d/%m %H")
        elif scale == 'every minute':
            timescale = answer['submission_date'].strftime("%d/%m %H:%M")
        
        if timescale not in submissions.keys():
            submissions[ timescale ] = {
                point_adjusted : 1
            }
        else:
            if point_adjusted not in submissions[ timescale ].keys():
                submissions[ timescale ][point_adjusted] = 1
            else:
                submissions[ timescale ][point_adjusted] += 1

    points = OrderedDict(sorted(points.items()))
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
        return "[1.0]"
    elif point >= 0.7 and point < 1:
        return "[0.9,0.7]"
    elif point >= 0.4 and point < 0.7:
        return "[0.6,0.4]"
    elif point > 0 and point < 0.4:
        return "[0.3,0.1]"
    else:
        return "[0.0]"

def scales_list():
    return ['weekly','dayly','hourly','every minute']
