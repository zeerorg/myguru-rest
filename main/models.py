from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^[1-9][0-9]{9}$',
                             message="Phone number must be entered in the format: '999999999'. Up to 15 digits allowed.")


# Create your models here
class Student(models.Model):
    id = models.IntegerField(blank=False, unique=True, primary_key=True, db_index=True)
    name = models.CharField(db_index=True, blank=False)
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    profile_pic = models.ImageField(blank=False)
    study_year = models.SmallIntegerField(blank=False)
    verified_phone = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)


class Teacher(models.Model):
    id = models.IntegerField(blank=False, unique=True, primary_key=True, db_index=True)
    name = models.CharField(db_index=True, blank=False)
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True, db_index=True, blank=False)
    email = models.EmailField(unique=True, db_index=True)
    profile_pic = models.ImageField(blank=False)
    about = models.TextField(blank=True)
    linked_in = models.CharField(blank=True)
    verified_phone = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)


# example : Thermodynamics, Physics, class 12
class Topic(models.Model):
    id = models.IntegerField(blank=False, unique=True, primary_key=True, db_index=True)
    title = models.CharField(blank=False)
    subject = models.CharField(blank=False)
    year = models.SmallIntegerField(blank=False)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("title", "subject", "year")


class StudentSubscription(models.Model):
    student_id = models.ForeignKey(Student, db_index=True)
    topic_id = models.ForeignKey(Topic, db_index=True)

    class Meta:
        unique_together = ("email", "subject")


# each class for a single topic
class TopicClass(models.Model):
    topic = models.ForeignKey(Topic, db_index=True)
    end_time = models.TimeField(blank=False)
    start_time = models.TimeField(blank=False)
    date = models.DateField(blank=False)
    description = models.TextField(blank=False)

