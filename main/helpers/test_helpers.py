import os

from django.core.files.uploadedfile import SimpleUploadedFile

from rest import settings


def get_student_dict():
    with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'rb') as content_file:
        content = content_file.read()
    data = {
        "name": "Rishabh Gupta",
        "phone": "9988776655",
        "email": "randomail@outlook.com",
        "study_year": "11",
        "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg"),
        "password": "12345678"
    }
    return data


def get_teacher_dict():
    with open(os.path.join(settings.BASE_DIR, "test_dir", "images.jpe"), 'rb') as content_file:
        content = content_file.read()
    data = {
        "name": "Rishabh Gupta",
        "phone": "9988776655",
        "email": "randomail@outlook.com",
        "about": "I teach Physics",
        "profile_pic": SimpleUploadedFile("yo.jpg", content, content_type="images/jpeg"),
        "password": "12345678"
    }
    return data


def get_topic_dict():
    topic_data = {
        "title": "Mechanics",
        "subject": "Physics",
        "year": "11",
        "description": "Laws of motion and stuff"
    }
    return topic_data
