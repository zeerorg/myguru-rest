from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
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


class StudentRegisterView(APIView):

    def get(self, request):
        return render(request, 'register_student.html', {'form': forms.StudentForm(), 'error': None})

    def post(self, request):
        form = forms.StudentForm(request.POST, request.FILES)
        error = check_password(request.POST["password"], request.POST["password_confirm"])

        if form.is_valid() and not error:
            data = form.cleaned_data
            data['password'] = request.POST['password']

            if save_student_helper(data):
                return HttpResponse("Yo!! Cool! ")
            else:
                return render(request, 'register_student.html', {'form': form, 'error': error, 'already_present': True})

        return render(request, 'register_student.html', {'form': form, 'error': error})


class TeacherRegisterView(APIView):

    def get(self, request, format=None):
        form = forms.TeacherForm()
        return render(request, 'register_teacher.html', {'form': form, 'error': None})

    def post(self, request, *args, **kwargs):
        form = forms.TeacherForm(request.POST, request.FILES)
        error = check_password(request.POST["password"], request.POST["password_confirm"])

        if form.is_valid() and not error:
            data = form.cleaned_data
            data['password'] = request.POST['password']

            if save_teacher_helper(data):
                return HttpResponse("Yo!! Cool! ")
            else:
                return render(request, 'register_teacher.html', {'form': form, 'error': error, 'already_present': True})

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
