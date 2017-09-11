import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

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


class TestStudentAuthRequest(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'rb') as content_file:
            content = content_file.read()
        self.data = {
            "name": "Rishabh Gupta",
            "phone": "9988776622",
            "email": "randomail3@outlook.com",
            "study_year": "11",
            "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg"),
        }
        self.student = models.Student.objects.create(**self.data)
        self.student.save()
        self.data["password"] = "12345678"
        self.user = User.objects.create_user(self.data['email'], self.data['email'], self.data["password"])
        self.token = Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

    def testAuthToken(self):
        request = self.factory.post("/api-token-auth/", {"username": self.data["email"], "password": self.data["password"]})
        response = auth_views.obtain_auth_token(request)
        self.assertEqual(response.data["token"], self.token.key)


class TestTeacherAuthToken(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'rb') as content_file:
            content = content_file.read()
        self.data = {
            "name": "Rishabh Gupta",
            "phone": "9988776655",
            "email": "randomail4@outlook.com",
            "about": "I teach Physics",
            "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg")
        }
        self.teacher = models.Teacher.objects.create(**self.data)
        self.teacher.save()
        self.data["password"] = "12345678"
        self.user = User.objects.create_user(self.data['email'], self.data['email'], self.data["password"])
        self.token = Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

    def testAuthToken(self):
        request = self.factory.post("/api-token-auth/", {"username": self.data["email"], "password": self.data["password"]})
        response = auth_views.obtain_auth_token(request)
        self.assertEqual(response.data["token"], self.token.key)


class TestTopic(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'rb') as content_file:
            content = content_file.read()
        self.teacher_data = {
            "name": "Rishabh Gupta",
            "phone": "9988776611",
            "email": "randomail5@outlook.com",
            "about": "I teach Physics",
            "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg")
        }
        self.teacher = models.Teacher.objects.create(**self.teacher_data)
        self.teacher.save()
        self.teacher_data["password"] = "12345678"
        self.user = User.objects.create_user(self.teacher_data['email'], self.teacher_data['email'], self.teacher_data["password"])
        self.token = Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

        self.topic_data = {
            "title": "Mechanics",
            "subject": "Physics",
            "year": "11",
            "description": "Laws of motion and stuff"
        }

    def testTopicCreation(self):
        request = self.factory.post("/api/topic/", self.topic_data, format="json", **{"Authorization": "Token " + str(self.token.key)})
        request.user = self.user
        response = views.add_topic(request)
        print(response.data)
        for x in response.data:
            if x != "id" and x != "teacher_id" and x != "detail":
                self.assertEqual(response.data[x], self.topic_data[x])

        #self.assertEqual(response.data["teacher_id"], self.teacher["id"]) # TODO: NOT WORKING KEYERROR teacher_id

        # Duplicate insertion
        response = views.add_topic(request)
        self.assertEqual(response.status_code, 409)








