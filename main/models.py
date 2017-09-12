import random

from django.db import models
from django.core.validators import RegexValidator

"""
    All the django model related classes are imported here
    hence other files communicate with django models through this module.

    For example, you'll do `from main import models` instead of `from django.contrib.auth import models`
"""
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.utils import IntegrityError

phone_regex = RegexValidator(regex=r'^[1-9][0-9]{9}$',
                             message="Phone number must be entered in the format: '999999999'. Up to 15 digits allowed.")


# Create your models here
class Student(models.Model):
    id = models.IntegerField(blank=False, unique=True, primary_key=True, db_index=True)
    name = models.CharField(max_length=50, db_index=True, blank=False)
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    profile_pic = models.ImageField(blank=False)
    study_year = models.SmallIntegerField(blank=False)
    verified_phone = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            if "id" not in kwargs:
                kwargs["id"] = random.randint(10000000, 99999999)
                
        super(Student, self).__init__(*args, **kwargs)


class Teacher(models.Model):
    id = models.IntegerField(blank=False, unique=True, primary_key=True, db_index=True)
    name = models.CharField(max_length=50, db_index=True, blank=False)
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True, db_index=True, blank=False)
    email = models.EmailField(unique=True, db_index=True)
    profile_pic = models.ImageField(blank=False)
    about = models.TextField(blank=True)
    linked_in = models.CharField(max_length=50, blank=True)
    verified_phone = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            if "id" not in kwargs:
                kwargs["id"] = random.randint(10000000, 99999999)

        super(Teacher, self).__init__(*args, **kwargs)


# example : Thermodynamics, Physics, class 12
class Topic(models.Model):
    id = models.IntegerField(blank=False, unique=True, primary_key=True, db_index=True)
    title = models.CharField(max_length=100, blank=False)
    subject = models.CharField(max_length=50, blank=False)
    year = models.SmallIntegerField(blank=False)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        if kwargs:
            if "id" not in kwargs:
                kwargs["id"] = random.randint(10000000, 99999999)

        teacher = Teacher.objects.get(id=kwargs["teacher_id"])
        kwargs["teacher_id"] = teacher

        super(Topic, self).__init__(*args, **kwargs)

    class Meta:
        unique_together = ("title", "subject", "year")


class StudentSubscription(models.Model):
    student_id = models.ForeignKey(Student, db_index=True)
    topic_id = models.ForeignKey(Topic, db_index=True)

    class Meta:
        unique_together = ("student_id", "topic_id")


# each class for a single topic
class TopicClass(models.Model):
    topic = models.ForeignKey(Topic, db_index=True)
    end_time = models.TimeField(blank=False)
    start_time = models.TimeField(blank=False)
    date = models.DateField(blank=False)
    description = models.TextField(blank=False)

