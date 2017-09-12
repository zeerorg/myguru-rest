import os

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate

import clear_test_data
from main import views
from main import models
from main.helpers.test_helper import *


class StudentSaveTest(TestCase):
    def setUp(self):
        self.data = get_student_dict()

    def testAdd(self):
        self.assertEqual(views.save_student(self.data.copy()), True)
        self.assertEqual(models.Student.objects.filter(email=self.data["email"]).count(), 1)
        self.assertEqual(views.save_student(self.data.copy()), False)

    def tearDown(self):
        clear_test_data.main()


class TeacherSaveTest(TestCase):
    def setUp(self):
        self.data = get_teacher_dict()

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

    def tearDown(self):
        clear_test_data.main()


class TestStudentAuthRequest(TestCase):
    def setUp(self):
        self.data = get_student_dict()
        del(self.data["password"])
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

    def tearDown(self):
        clear_test_data.main()


class TestTeacherAuthToken(TestCase):
    def setUp(self):
        self.data = get_teacher_dict()
        del(self.data["password"])
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

    def tearDown(self):
        clear_test_data.main()


class TestTopic(TestCase):
    def setUp(self):
        self.teacher_data = get_teacher_dict()
        del(self.teacher_data["password"])
        self.teacher = models.Teacher.objects.create(**self.teacher_data)
        self.teacher.save()
        self.teacher_data["password"] = "12345678"
        self.user = User.objects.create_user(self.teacher_data['email'], self.teacher_data['email'], self.teacher_data["password"])
        self.token = Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

        self.topic_data = get_topic_dict()

    def testTopicCreation(self):
        request = self.factory.post("/api/topic/", self.topic_data, format="json")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = views.add_topic(request)
        for x in response.data:
            if x != "id" and x != "teacher_id" and x != "detail":
                self.assertEqual(str(response.data[x]), self.topic_data[x])

        # Duplicate insertion
        request = self.factory.post("/api/topic/", self.topic_data, format="json")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = views.add_topic(request)
        self.assertEqual(response.status_code, 409)

    def tearDown(self):
        clear_test_data.main()








