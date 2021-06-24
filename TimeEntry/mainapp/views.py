import json
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from .models import *
from .forms import UserForm
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from .filter import TaskFilter
from .decorators import *

# Create your views here.
@unauth_user
def home(request):
    print(request.user)
    return render(request,'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@unauth_user
def signin(request):
    errmsg = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('task')
        else:
            errmsg="invalid credentials"
        #print(username+" "+password)
    context = {'err':errmsg}
    return render(request,'login.html',context)


@unauth_user
def signup(request):
    form = UserForm()
    errormsg = ""
    if request.method == "POST" :
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            errormsg = form.errors
            
            print(form.errors)
            print(form.error_messages)
        
    context = {
            'form':form,
            'errmsg':errormsg
        }
    return render(request,'signup.html',context)

@auth_user
def dashboard(request):
    user = request.user
    if request.method=="POST" :
        taskname = request.POST.get("taskname")
        project_id = request.POST.get("project")
        project = Project.objects.get(id=project_id)
        task = UserTask(employee=user,project=project,Task_title=taskname)
        task.save()
        return redirect('task')
        # print(taskname)
        # print(project)

    projects = Project.objects.all().filter(status=True)
    tasks = UserTask.objects.all().filter(employee=user)
    task_filter = TaskFilter(request.GET,queryset=tasks)
    print(task_filter.form)
    tasks=task_filter.qs
    task_list=[]
    for task in tasks:
        print(task.end_time)
        #print(task.start_time.strftime("%b %d, %Y %H:%M"))
        end_time=task.end_time
        if task.end_time is not None:
            end_time = task.end_time.strftime("%b %d, %Y %H:%M:%S")
        task_item ={
            'id':task.id,
            'Task_title':task.Task_title,
            'project':task.project,
            'status':task.status,
            'start_time':task.start_time.strftime("%b %d, %Y %H:%M:%S"),
            'end_time':end_time,
        }
        task_list.append(task_item)
    context = {
        'projects':projects,
        'tasks':task_list,
        'filter':task_filter
    }
    return render(request,'dashboard.html',context)

@auth_user
def project_view(request):
    project_list = Project.objects.all()
    if request.method=="POST" :
        projectname = request.POST.get("projectname")
        project = Project(project_name=projectname)
        project.save()
        return redirect('project')
    projects=[]
    for p in project_list:
        count = UserTask.objects.all().filter(project=p).count()
        #print(count,p.id,p.project_name,p.status)
        project = {
            'project_name':p.project_name,
            'status':p.status,
            'id':p.id,
            'count':count
        }
        projects.append(project)
    context = {'projects':projects}
    return render(request,'project.html',context)

@auth_user
def endProject(request):
    dateNow = datetime.today()
    if request.method=="POST" :
        data = json.loads(request.body)
        project_id = data['project_id']
        project = Project.objects.get(id = project_id)
        tasks = UserTask.objects.all().filter(project = project)
        for task in tasks:
            #print(task)
            task.status = False
            task.end_time = dateNow
            task.save()
        project.status = False
        project.save()
        #print(project_id)
    return JsonResponse("project ended",safe=False)

@auth_user
def endTask(request):
    if request.method=="POST" :
        dateNow = datetime.today()
        data = json.loads(request.body)
        task_id = data['task_id']
        task = UserTask.objects.get(id = task_id)
        task.status = False
        task.end_time = dateNow
        task.save()
        # print(task_id,task.start_time,dateNow)
    return JsonResponse("Task ended",safe=False)


