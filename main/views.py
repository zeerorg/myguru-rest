from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from main import forms
from helpers.view_helper import *


def main_page(request):
    """
    The first page
    """
    return render(request, 'index.html')


@api_view(['GET', 'POST'])
def register_student(request):
    """
    Student Registration Form
    """
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

            if save_student_helper(data):
                return HttpResponse("Yo!! Cool! ")
            else:
                return render(request, 'register_student.html', {'form': form, 'error': error, 'already_present': True})

    if request.method == 'GET':
        form = forms.StudentForm()
    return render(request, 'register_student.html', {'form': form, 'error': error})


# Teacher registration form.
@api_view(['GET', 'POST'])
def register_teacher(request):
    """
    Teacher Registration Form
    """
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

            if save_teacher_helper(data):
                return HttpResponse("Yo!! Cool! ")
            else:
                return render(request, 'register_teacher.html', {'form': form, 'error': error, 'already_present': True})

    if request.method == 'GET':
        form = forms.TeacherForm()
    return render(request, 'register_teacher.html', {'form': form, 'error': error})


class StudentView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        data, code = get_student_helper(request.user.email)
        if code:
            return Response(data)
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class TeacherView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        data, code = get_teacher_helper(request.user.email)
        if code:
            return Response(data)
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class TopicView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        data = get_all_topics()
        return Response(data)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data, code = save_topic_helper(data, request.user.email)
        if code:
            return Response(data)
        else:
            return Response(data, status=status.HTTP_409_CONFLICT)
