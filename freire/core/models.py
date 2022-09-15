from django.db import models

# Create your models here.


# from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


class User(AbstractUser):
    password_email_sent = models.BooleanField(default=False)


class StudentManager(UserManager):
    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = 'Student'


class InstructorManager(UserManager):
    def get_queryset(self):
        return User.objects.filter(is_staff=True)


class Instructor(User):
    objects = InstructorManager()

    class Meta:
        proxy = True
        verbose_name = 'Instructor'

    def save(self, *args, **kwargs):
        self.is_staff = True
        return super().save(*args, **kwargs)


class Course(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Offering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.course.name + self.description


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.student} [{self.offering}]'


class Teaches(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE)


class Exercise(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE)
    allow_submissions = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255)
    url = models.URLField()
    topic = models.CharField(max_length=1024)
    group = models.CharField(max_length=1024)

    class ExerciseType(models.TextChoices):
        CODE = 'CODE', 'Code'
        QUIZ = 'QUIZ', 'Quiz'
        TEXT = 'TEXT', 'Text'
        CSS = 'CSS', 'CSS'
        SELF_ASSESS = 'SELF', 'Self-assess'

    type = models.CharField(max_length=4, choices=ExerciseType.choices)

    def __str__(self) -> str:
        return self.slug


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    points = models.FloatField()
    submission_date = models.DateTimeField(default=timezone.now)
    test_results = models.JSONField()
    student_input = models.JSONField()

    def __str__(self) -> str:
        return f"{self.exercise} -> {self.user.username} ({self.submission_date})"


class UserAnswerSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    max_points = models.FloatField(default=0)
    answer_count = models.IntegerField(default=0)
    latest = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "exercise"], name="unique_user_exercise_summary"
            ),
        ]

    def __str__(self) -> str:
        return f'{self.user} -> {self.exercise} (pts: {self.max_points}, count: {self.answer_count})'
