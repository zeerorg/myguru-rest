from django import forms
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^[1-9][0-9]{9}$',
                             message="Phone number must be entered in the format: '1234567890'.")


class StudentForm(forms.Form):
    name = forms.CharField(label="Your Name")
    phone = forms.CharField(label="Phone Number", validators=[phone_regex])
    email = forms.EmailField(label="Email")
    # study_year = forms.ModelChoiceField(queryset=[ x for x in range(11, 13) ])
    profile_pic= forms.ImageField()


class TeacherForm(forms.Form):
    name = forms.CharField(label="Your Name")
    phone = forms.CharField(label="Phone Number")
    email = forms.CharField(label="Email")
    profile_pic = forms.ImageField()
    about = forms.TextInput()