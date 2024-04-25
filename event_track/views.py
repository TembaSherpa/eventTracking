from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import MyClassForm, SignUpForm, StudentForm, TeacherForm
from django.contrib.auth import authenticate, login, logout
from .models import  MyClass, Student, Teacher
from django.views.generic import CreateView
from .utils import send_class_cancel_notification


# https://medium.com/@elijahobara/how-to-send-emails-using-python-django-and-google-smtp-server-at-no-cost-bbcbb8e8638b
# Create your views here.
def dashboard(request):
    teachers = Teacher.objects.all()
    signup_form = SignUpForm()  # Instantiate SignUpForm
    classes = MyClass.objects.all()
    # class_dict = {my_class.pk: my_class for my_class in classes}
    context = {'signup_form': signup_form, 'classes': classes, 'teachers': teachers}
    return render(request, 'dashboard.html', context )


def homepage(request):
    classes = MyClass.objects.all()
    class_dict = {my_class.pk: my_class for my_class in classes}
    context = {'classes': classes, 'class_dict': class_dict}
    return render(request, 'homepage.html', context )
    
def handle_logout(request):
    logout(request)
    return redirect("login")

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def create_class(request):
    if request.method == 'POST':
        form = MyClassForm(request.POST, request.FILES)
        # Check if the room is available at the specified time
        if form.is_valid():
            form.save()
            return redirect('dashboard')    
    else:
        form = MyClassForm()
    return render(request, 'create_class.html', {'form': form})

def class_detail(request, pk):
    # Retrieve the class object from the database based on the pk
    my_class = get_object_or_404(MyClass, pk=pk)
    # Filter students by the class using the ForeignKey relationship
    students = Student.objects.filter(my_class_id=pk)
    form = StudentForm()
  
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Associate the student with the class before saving
            student = form.save(commit=False)
            student.my_class_id = pk
            student.save()
            return redirect('class_detail', pk=pk)   
        
    if my_class.status == 'Running' and my_class.start_time + timezone.timedelta(hours=1) <= timezone.now():
        my_class.status = 'Finished'
        my_class.save()

    return render(request, 'class_detail.html', {'my_class': my_class, 'students': students, 'form': form})

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
    return redirect('class_detail', pk=student.my_class_id)

def delete_class(request, pk):
    # Retrieve the class object
    class_obj = get_object_or_404(MyClass, pk=pk)
    
    if request.method == 'POST':
        # Check if the request method is POST
        class_obj.delete()
        # Delete the class
        return redirect('dashboard')
        # Redirect to the dashboard after deletion
    # Handle the case where the request method is not POST
    return render(request, 'dashboard.html', {'class_obj': class_obj})


def cancel_class(request, class_id):
    myclass = MyClass.objects.get(pk=class_id)
    myclass.status = 'off'
    myclass.save()
    return redirect('dashboard')

def send_email(request):
    send_class_cancel_notification()
    return render(request, 'dashboard')

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to a page showing all teachers
    else:
        form = TeacherForm()
    return render(request, 'add_teacher.html', {'form': form})

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'teacher': teacher})