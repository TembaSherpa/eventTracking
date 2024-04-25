import datetime
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save

# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.IntegerField( null=True, blank=True)

    def __str__(self):
        return self.name


class MyClass(models.Model):
    name = models.CharField(max_length=100)
    profile = models.FileField(upload_to='addclass/', null=True, blank=True)
    date = models.DateField()
    Duration = models.IntegerField(null=True, blank=True)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)
    syllabus = models.FileField(upload_to='syllabus/', blank=True, null= True)
    status = models.CharField(max_length=20, choices=[('running', 'Running'), ('off', 'Off')], default='Upcoming')
    time = models.TimeField(default=timezone.now)
   


    def __str__(self):
        return self.name
    
    def update_status(self):
        current_datetime = datetime.datetime.combine(self.date, self.time)
        one_hour_later = current_datetime + datetime.timedelta(hours=1)
        now = datetime.datetime.now()

        if now < current_datetime:
            if self.status != "Off":
                self.status = "Off"
                self.save()
        elif current_datetime <= now < one_hour_later:
            if self.status != "Running":
                self.status = "Running"
                self.save()
        else:
            if self.status != "Off":
                self.status = "Off"
                self.save()

@receiver(pre_save, sender=MyClass)
def update_class_status(sender, instance, **kwargs):
    instance.update_status()

class Student(models.Model):
    my_class = models.ForeignKey(MyClass, on_delete=models.CASCADE, default=None)
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_number = models.IntegerField()
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    attendance = models.CharField(max_length=10, blank=True, null=True)