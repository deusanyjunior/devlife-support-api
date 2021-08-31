from rest_framework import serializers
from .models import Answer, User, Exercise, UserAnswerSummary


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'is_staff']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['slug', 'url', 'type', 'offering']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'exercise', 'points', 'submission_date', 'summary', 'long_answer']


class UserAnswerSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswerSummary
        fields = ['user', 'exercise', 'max_points', 'answer_count', 'latest']
