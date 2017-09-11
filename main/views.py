from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from main import forms, models, serializers


# The first page view
def main_page(request):
    return render(request, 'index.html')


# Student registration form.
@api_view(['GET', 'POST'])
def register_student(request):
    form = None
    error = None
    if request.method == 'POST':
        form = forms.StudentForm(request.POST, request.FILES)

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
        form = forms.StudentForm()
    return render(request, 'register_student.html', {'form': form, 'error': error})


# Teacher registration form.
@api_view(['GET', 'POST'])
def register_teacher(request):
    form = None
    error = None
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES)

        if len(request.POST['password']) < 8:
            error = "Password too short."
        elif request.POST['password'] != request.POST['password_confirm']:
            error = "Passwords do not match."

        if form.is_valid() and not error:
            data = form.cleaned_data
            data['password'] = request.POST['password']

            if save_teacher(data):
                return HttpResponse("Yo!! Cool! ")
            else:
                return render(request, 'register_teacher.html', {'form': form, 'error': error, 'already_present': True})

    if request.method == 'GET':
        form = forms.TeacherForm()
    return render(request, 'register_teacher.html', {'form': form, 'error': error})


@api_view(["GET"])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def get_student(request):
    student_query = models.Student.objects.filter(email=request.user.email)
    if student_query.exists():
        student = models.Student.objects.get(email=request.user.email)
        content = serializers.StudentSerializer(student)
        return Response(content.data)
    return Response({"detail": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def get_teacher(request):
    teacher_query = models.Teacher.objects.filter(email=request.user.email)
    if teacher_query.exists():
        teacher = teacher_query.first()
        content = serializers.TeacherSerializer(teacher)
        return Response(content.data)
    return Response({"detail": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def add_topic(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        data["teacher_id"] = models.Teacher.objects.get(email=request.user.email).id
        serializer = serializers.TopicSerializer(data=data)
        if serializer.is_valid():
            topic = serializer.save()
            response = Response(serializer.data)
            print(response.data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


def save_student(data):
    try:
        password = data['password']
        del(data['password'])
        student = models.Student(**data)
        student.save()
        user = User.objects.create_user(data['email'], data['email'], password)
        token = Token.objects.create(user=user)
        return True
    except IntegrityError:
        return False


def save_teacher(data):
    try:
        password = data['password']
        del(data['password'])
        teacher = models.Teacher(**data)
        teacher.save()
        user = User.objects.create_user(data['email'], data['email'], password)
        token = Token.objects.create(user=user)
        return True
    except IntegrityError:
        return False
