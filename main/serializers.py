from rest_framework import serializers

from main.models import *


class StudentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    study_year = serializers.IntegerField(read_only=True)
    profile_pic = serializers.ImageField(read_only=True)
    verified_phone = serializers.BooleanField(read_only=True)
    verified_email = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass