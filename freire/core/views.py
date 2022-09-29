from typing_extensions import Required
from django.shortcuts import render, get_object_or_404
from django_tables2 import SingleTableView, RequestConfig

from core.models import Answer, Offering, Student, Exercise, UserAnswerSummary
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

def exercises(request):
    offerings = list(Offering.objects.all().values())

    exercises = list(Exercise.objects.all().values())
    groups = []
    topics = []
    types = []
    for exercise in exercises:
        if exercise['group'] not in groups:
            groups.append( exercise['group'] )
        if exercise['topic'] not in topics:
            topics.append( exercise['topic'] )
        if exercise['type'] not in types:
            types.append( exercise['type'] )

    offering = request.POST.get('offering', False)
    if offering == False:
        offering = offerings[len(offerings) -1 ]['id']
    group = request.POST.get('group', False)
    if group == False:
        group = groups[0]
    topic = request.POST.get('topic', False)
    if topic == False:
        topic = topics[0]
    type = request.POST.get('type', False)
    if type == False:
        type = types[0]
    
    filters = {
        'offering': offering,
        'group': group,
        'topic': topic,
        'type': type
    }

    exercises_table = ExerciseTable(Exercise.objects.filter(**filters))
    RequestConfig(request, paginate={"per_page": 10}).configure(exercises_table)
    
    return render(request, 'exercises.html', {
        'offering': offering,
        'offerings': offerings,
        'groups': list(groups),
        'group': group,
        'topics': list(topics),
        'topic': topic,
        'types': list(types),
        'type': type,
        'exercises_table': exercises_table
    })
    
def exercise_info(request, ex_slug):
    scales = ['day','hour','minute']
    scale = request.POST.get('scale', False)
    if scale == False:
        scale = scales[0]

    exercise = get_object_or_404(Exercise, id = ex_slug)
    filters = {
        'exercise': ex_slug
    }
    answers = Answer.objects.filter(**filters)

    # points
    points = {}
    submissions = {}
    for answer in answers.values():
        if answer['points'] not in points.keys():
            points[answer['points']] = 1
        else:
            points[answer['points']] += 1
        if scale == 'day':
            day = answer['submission_date'].strftime("%d/%m/%Y")
            if day not in submissions.keys():
                submissions[ day ] = {
                    answer['points']: 1
                }
            else:
                if answer['points'] not in submissions[ day ].keys():
                    submissions[ day ][answer['points']] = 1
                else:
                    submissions[ day ][answer['points']] += 1

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

    return render(request, 'exercise.html', {
        'exercise': exercise,
        'answers': list(answers.values()),
        'points': points,
        'scales': list(scales),
        'scale': scale,
        'submissions': submissions,
        'days': days,
        'points_list': points_list,
        'dataset': dataset
    })