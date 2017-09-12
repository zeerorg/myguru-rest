from django.test import TestCase
from rest_framework.authtoken import views as auth_views
from rest_framework.test import APIRequestFactory, force_authenticate

import clear_test_data
from main import views
from main import models
from main.helpers.test_helpers import *


class StudentSaveTest(TestCase):
    def setUp(self):
        self.data = get_student_dict()
        self.factory = APIRequestFactory()

    def testAdd(self):
        self.assertEqual(views.save_student_helper(self.data.copy()), True)
        self.assertEqual(models.Student.objects.filter(email=self.data["email"]).count(), 1)
        self.assertEqual(views.save_student_helper(self.data.copy()), False)

    def tearDown(self):
        clear_test_data.main()


class TeacherSaveTest(TestCase):
    def setUp(self):
        self.data = get_teacher_dict()

    def testAdd(self):
        self.assertEqual(views.save_teacher_helper(self.data.copy()), True)
        self.assertEqual(models.Teacher.objects.get(email=self.data["email"]).phone, self.data["phone"])
        self.assertEqual(views.save_teacher_helper(self.data.copy()), False)

    def testAboutIsOptional(self):
        new_data = self.data.copy()
        new_data["about"] = ""
        new_data["phone"] = "1122334455"
        new_data["email"] = "randomail2@gmail.com"
        new_data["name"] = "Rishabh Gupta New"
        self.assertEqual(views.save_teacher_helper(new_data), True)
        self.assertEqual(models.Teacher.objects.get(email=new_data["email"]).phone, new_data["phone"])

    def tearDown(self):
        clear_test_data.main()


class TestStudentRequest(TestCase):
    def setUp(self):
        self.data = get_student_dict()
        del(self.data["password"])
        self.student = models.Student.objects.create(**self.data)
        self.student.save()
        self.data["password"] = "12345678"
        self.user = models.User.objects.create_user(self.data['email'], self.data['email'], self.data["password"])
        self.token = models.Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

    def testAuthToken(self):
        request = self.factory.post("/api-token-auth/", {"username": self.data["email"], "password": self.data["password"]})
        response = auth_views.obtain_auth_token(request)
        self.assertEqual(response.data["token"], self.token.key)

    def testGet(self):
        request = self.factory.get("/api/get_student")
        force_authenticate(request, user=self.user, token=self.token)
        response = views.get_student(request)
        self.assertEqual(int(response.data["id"]), self.student.id)

    def tearDown(self):
        clear_test_data.main()


class TestTeacherAuthToken(TestCase):
    def setUp(self):
        self.data = get_teacher_dict()
        del(self.data["password"])
        self.teacher = models.Teacher.objects.create(**self.data)
        self.teacher.save()
        self.data["password"] = "12345678"
        self.user = models.User.objects.create_user(self.data['email'], self.data['email'], self.data["password"])
        self.token = models.Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

    def testAuthToken(self):
        request = self.factory.post("/api-token-auth/", {"username": self.data["email"], "password": self.data["password"]})
        response = auth_views.obtain_auth_token(request)
        self.assertEqual(response.data["token"], self.token.key)

    def testGet(self):
        request = self.factory.get("/api/get_teacher")
        force_authenticate(request, user=self.user, token=self.token)
        response = views.get_teacher(request)
        self.assertEqual(int(response.data["id"]), self.teacher.id)

    def tearDown(self):
        clear_test_data.main()


class TestTopic(TestCase):
    def setUp(self):
        self.teacher_data = get_teacher_dict()
        del(self.teacher_data["password"])
        self.teacher = models.Teacher.objects.create(**self.teacher_data)
        self.teacher.save()
        self.teacher_data["password"] = "12345678"
        self.user = models.User.objects.create_user(self.teacher_data['email'], self.teacher_data['email'], self.teacher_data["password"])
        self.token = models.Token.objects.create(user=self.user)
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

    def testTopicRetrieval(self):
        views.save_topic_helper(self.topic_data, self.user.email)

        request = self.factory.get("/api/topic")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = views.add_topic(request)
        all_ids = models.Topic.objects.all()
        all_ids_set = set()
        for x in all_ids:
            all_ids_set.add(x.id)

        all_ids = all_ids_set
        self.assertEqual(len(all_ids) > 0, True)
        for x in response.data:
            self.assertEqual(int(x["id"]) in all_ids, True)
            all_ids.remove(int(x["id"]))

    def tearDown(self):
        clear_test_data.main()
