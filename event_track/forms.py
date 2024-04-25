from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyClass, Student, Teacher
from django.db import models

class SignUpForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField(max_length=254)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    profile = forms.ImageField(label='Profile', widget=forms.FileInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class MyClassForm(forms.ModelForm):
    class Meta:
        model = MyClass
        fields = ('name', 'profile', 'date', 'syllabus',  'time', 'Duration', 'Teacher')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'contact_number']
    # def __str__(self):
    #    return self.name 
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id', 'name', 'contact_number', 'email', 'address', ] 
        