from rest_framework import serializers

from main import models


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


class TeacherSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    about = serializers.CharField(read_only=True)
    profile_pic = serializers.ImageField(read_only=True)
    verified_phone = serializers.BooleanField(read_only=True)
    verified_email = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class TopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(allow_blank=False)
    subject = serializers.CharField(allow_blank=False)
    year = serializers.IntegerField(min_value=11, max_value=12)
    description = serializers.CharField(allow_blank=True, allow_null=False)
    teacher_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return models.Topic.objects.create(**validated_data)