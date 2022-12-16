from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskFormCreate
from .models import Task
from django.utils import timezone
# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            'error': ''
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                 return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })
        else:
            return render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': 'Password no coincide'
            })

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': ''
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required       
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def task_detail(request, id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk = id, user = request.user)
        form = TaskFormCreate(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk = id, user = request.user)
            form = TaskFormCreate(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })           
    
@login_required
def task_create(request):
    if request.method == "GET":
        return render(request, 'task_create.html', {
            'form': TaskFormCreate
        })
    else:
        try:
            form = TaskFormCreate(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_create.html', {
                'form': TaskFormCreate,
                'error': 'Please provide valid data'
            })

@login_required
def task_create(request):
    if request.method == "GET":
        return render(request, 'task_create.html', {
            'form': TaskFormCreate
        })
    else:
        try:
            form = TaskFormCreate(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_create.html', {
                'form': TaskFormCreate,
                'error': 'Please provide valid data'
            })

@login_required
def task_detail(request, id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk = id, user = request.user)
        form = TaskFormCreate(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk = id, user = request.user)
            form = TaskFormCreate(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })

@login_required            
def task_delete(request, id):
    task = get_object_or_404(Task, pk = id, user = request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')

@login_required           
def task_complete(request, id):
    task = get_object_or_404(Task, pk = id, user = request.user)
    if request.method == "POST":
        task.datecomplited = timezone.now()
        task.save()
        return redirect('tasks')