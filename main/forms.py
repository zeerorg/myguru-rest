from django import forms


class StudentForm(forms.Form):
    name = forms.CharField(label="Your Name")
    phone = forms.CharField(label="Phone Number")
    email = forms.EmailField(label="Email")
    study_year = forms.ModelChoiceField(queryset=[ x for x in range(11, 13) ])
    profile_pic= forms.ImageField()


class TeacherForm(forms.Form):
    name = forms.CharField(label="Your Name")
    phone = forms.CharField(label="Phone Number")
    email = forms.CharField(label="Email")
    profile_pic = forms.ImageField()
    about = forms.TextInput()