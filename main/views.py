from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from main.forms import *
from main.models import *


# The first page view
def main_page(request):
    return render(request, 'index.html')


# Student registration form. TODO: implement password and authentication
def register_student(request):
    form = None
    error = None
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if len(request.POST['password']) < 8:
            error = "Password too short."
        elif request.POST['password'] != request.POST['password_confirm']:
            error = "Passwords do not match."
        print(request.POST['password'], error)
        if form.is_valid() and not error:
            #student = Student(form.cleaned_data)
            #user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], request.POST['password'])
            #token = Token.objects.create(user=user)
            print("registered", form.cleaned_data)
            return HttpResponse("Yo!! Cool! ")
        else:
            print("is form valid", form.is_valid())
            print(form.cleaned_data)
            pass
            #return Http404("Hello!! ??")
    if request.method == 'GET':
        form = StudentForm()
    return render(request, 'register_student.html', {'form': form, 'error': error})