from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from main.forms import *


# The first page view
def main_page(request):
    return render(request, 'index.html')


# Student registration form. TODO: implement password and authentication
def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            token = Token.objects.create(user=form.cleaned_data['email'])
            return HttpResponse("Yo!! Cool! " + str(token.key))
    if request.method == 'GET':
        form = StudentForm()
    return render(request, 'register_student.html', {'form': form})