from django import http
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from .models import Answer, Offering, User, Exercise
from .serializers import AnswerSerializer, UserSerializer, ExerciseSerializer
from .permissions import IsAdminOrSelf, IsAdminUser

from datetime import datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]


class ExerciseViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, off_pk=None):
        offering = get_object_or_404(Offering, pk=off_pk)
        
        exercise, new = offering.exercise_set.update_or_create(slug=request.data['slug'], 
            defaults={
                'url': request.data['url'],
                'type': request.data['type']
            })

        s = ExerciseSerializer(exercise)
        return Response(s.data)

    def list(self, request, off_pk=None):
        offering = get_object_or_404(Offering, pk=off_pk)
        exercises_json = ExerciseSerializer(offering.exercise_set.all(), many=True)
        return Response(exercises_json.data)

    @action(detail=False, methods=['POST'])
    def send_answer(self, request, off_pk=None, ex_slug=None):
        offering = get_object_or_404(Offering, pk=off_pk)
        exercise = get_object_or_404(Exercise, slug=ex_slug)

        answer_data = {
            'user': request.user.pk,
            'exercise': exercise.pk,
            'summary': request.data['summary'],
            'long_answer': request.data['long_answer'],
            'points': request.data['points']
        }
    
        answer = AnswerSerializer(data=answer_data)
        if answer.is_valid():
            answer.save()
            return Response(answer.data, status=status.HTTP_201_CREATED)
    
        return Response(answer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def list_answers(self, request, off_pk, ex_slug):
        offering = get_object_or_404(Offering, pk=off_pk)
        exercise = get_object_or_404(Exercise, slug=ex_slug)
        
        all_answers = Answer.objects.filter(exercise=exercise)
        all_answers_json = AnswerSerializer(all_answers, many=True)

        return Response(all_answers_json.data, status=status.HTTP_200_OK)