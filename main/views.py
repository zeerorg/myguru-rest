from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from main.forms import *
from main.models import *


# The first page view
def main_page(request):
    return render(request, 'index.html')


def save_student(data):
    try:
        student = Student(**data)
        student.save()
        user = User.objects.create_user(data['email'], data['email'],
                                        data['password'])
        token = Token.objects.create(user=user)
        print("registered", data)
        return True
    except IntegrityError:
        return False


# Student registration form.
def register_student(request):
    form = None
    error = None
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)

        if len(request.POST['password']) < 8:
            error = "Password too short."
        elif request.POST['password'] != request.POST['password_confirm']:
            error = "Passwords do not match."

        if form.is_valid() and not error:
            data = form.cleaned_data
            data['password'] = request.POST['password']

            if save_student(data):
                return HttpResponse("Yo!! Cool! ")
            else:
                return render(request, 'register_student.html', {'form': form, 'error': error, 'already_present': True})

    if request.method == 'GET':
        form = StudentForm()
    return render(request, 'register_student.html', {'form': form, 'error': error})