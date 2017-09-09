import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from main import views
from rest import settings
from main import models


class StudentSaveTest(TestCase):
    def setUpTestData(cls):
        with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'r') as content_file:
            content = content_file.read()
        cls.data = {
            "name": "Rishabh Gupta",
            "phone": "9988776655",
            "email": "randomail@outlook.com",
            "study_year": "11",
            "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg")
        }

    def testAdd(self):
        pass


# Create your tests here.
def student_save_test():
    with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'r') as content_file:
        content = content_file.read()
    data = {
        "name": "Rishabh Gupta",
        "phone": "9711821354",
        "email": "r.g.gupta@outlook.com",
        "study_year": "11",
        "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg")
    }
    views.save_student(data)
    pass
