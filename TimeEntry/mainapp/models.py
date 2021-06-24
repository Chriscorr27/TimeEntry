from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    project_name = models.CharField(max_length= 150)
    status = models.BooleanField(default= True)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = "Project Name"
        verbose_name_plural = "Project lists"


class UserTask(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,null=True,on_delete=models.CASCADE)
    Task_title = models.CharField(max_length= 100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(max_length=60,blank=True,null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.Task_title
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
