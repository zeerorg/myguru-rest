from main import models as main_models
from main import serializers as main_serializers


def save_student_helper(data):
    """
    Creates a new student, inserts it in Student model, creates User and Token for it
    :param data: contains: "name", "phone", "email", "study_year", "profile_pic", "password"
    :rtype bool:
    :return:
    """
    try:
        password = data['password']
        del(data['password'])
        student = main_models.Student(**data)
        student.save()
        user = main_models.User.objects.create_user(data['email'], data['email'], password)
        token = main_models.Token.objects.create(user=user)
        return True
    except main_models.IntegrityError:
        return False


def save_teacher_helper(data):
    """
    Creates a new teacher, inserts it in Teacher model, creates User and Token for it
    :param data: contains: "name", "phone", "email", "profile_pic", "password", "about"
    :rtype bool:
    :return:
    """
    try:
        password = data['password']
        del(data['password'])
        teacher = main_models.Teacher(**data)
        teacher.save()
        user = main_models.User.objects.create_user(data['email'], data['email'], password)
        token = main_models.Token.objects.create(user=user)
        return True
    except main_models.IntegrityError:
        return False


def save_topic_helper(data, teacher_mail):
    teacher_query = main_models.Teacher.objects.filter(email=teacher_mail)
    if not teacher_query.exists():
        return {"detail": "Not Authenticated to create topic."}, False

    data["teacher_id"] = teacher_query.get().id
    serializer = main_serializers.TopicSerializer(data=data)
    if serializer.is_valid():
        topic = serializer.save()
        return serializer.data, True
    return serializer.errors, False


def get_teacher_helper(teacher_email):
    teacher_query = main_models.Teacher.objects.filter(email=teacher_email)
    if teacher_query.exists():
        teacher = teacher_query.first()
        content = main_serializers.TeacherSerializer(teacher)
        return content.data, True
    return {"detail": "Invalid Token"}, False


def get_student_helper(student_email):
    student_query = main_models.Student.objects.filter(email=student_email)
    if student_query.exists():
        student = student_query.first()
        content = main_serializers.StudentSerializer(student)
        return content.data, True
    return {"detail": "Invalid Token"}, False
