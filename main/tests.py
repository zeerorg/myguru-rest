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


