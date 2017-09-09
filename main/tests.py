import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from main import views
from rest import settings
from main import models


class StudentSaveTest(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'rb') as content_file:
            content = content_file.read()
        self.data = {
            "name": "Rishabh Gupta",
            "phone": "9988776655",
            "email": "randomail@outlook.com",
            "study_year": "11",
            "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg"),
            "password": "12345678"
        }

    def testAdd(self):
        self.assertEqual(views.save_student(self.data.copy()), True)
        self.assertEqual(models.Student.objects.filter(email=self.data["email"]).count(), 1)
        self.assertEqual(views.save_student(self.data.copy()), False)


class TeacherSaveTest(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'rb') as content_file:
            content = content_file.read()
        self.data = {
            "name": "Rishabh Gupta",
            "phone": "9988776655",
            "email": "randomail@outlook.com",
            "about": "I teach Physics",
            "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg"),
            "password": "12345678"
        }

    def testAdd(self):
        self.assertEqual(views.save_teacher(self.data.copy()), True)
        self.assertEqual(models.Teacher.objects.get(email=self.data["email"]).phone, self.data["phone"])
        self.assertEqual(views.save_teacher(self.data.copy()), False)

    def testAboutIsOptional(self):
        new_data = self.data.copy()
        new_data["about"] = ""
        new_data["phone"] = "1122334455"
        new_data["email"] = "randomail2@gmail.com"
        new_data["name"] = "Rishabh Gupta New"
        self.assertEqual(views.save_teacher(new_data), True)
        self.assertEqual(models.Teacher.objects.get(email=new_data["email"]).phone, new_data["phone"])


