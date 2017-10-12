from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Task
from ..users_app.models import User
from ..lists_app.models import List

# Create your views here.
def createtask(request, id):
    if request.method == 'POST':
        errors = Task.objects.validation(request.POST)
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='task')
        else:
            this_user = User.objects.get(id=request.session['id'])
            this_list = List.objects.get(id=id)
            this_task = Task.objects.create(title=request.POST['title'], due_date=request.POST['due_date'], assignedlist=this_list, creator=this_user)
            this_task.users.add(this_user)
        return redirect(reverse('lists:add', kwargs={'id': id }))
    else:
        return redirect(reverse('users:index'))

def addusertask(request, id):
    this_task = Task.objects.get(id=id)
    if request.method == 'POST' and 'user' in request.POST:
        if this_task.creator == User.objects.get(id=request.session['id']):
            this_task.users.add(User.objects.get(id=request.POST['user']))
        elif User.objects.get(id=request.session['id']) in this_task.assignedlist.users.all():
            this_task.users.add(User.objects.get(id=request.session['id']))
    return redirect(reverse('lists:add', kwargs={'id': this_task.assignedlist.id }))

def removeusertask(request, id):
    this_task = Task.objects.get(id=id)
    if request.method == 'POST' and 'user' in request.POST:
        if this_task.creator == User.objects.get(id=request.session['id']) and User.objects.get(id=request.POST['user']) != this_task.creator:
            this_task.users.remove(User.objects.get(id=request.POST['user']))
        elif User.objects.get(id=request.session['id']) in this_task.users.all() and User.objects.get(id=request.session['id']) != this_task.creator:
            this_task.users.remove(User.objects.get(id=request.session['id']))
    return redirect(reverse('lists:add', kwargs={'id': this_task.assignedlist.id }))

def changetaskstatus(request, taskid, listid):
    this_task = Task.objects.get(id=taskid)
    this_user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        if this_user in this_task.users.all():
            this_task.completed = not this_task.completed
            this_task.save()
    return redirect(reverse('lists:add', kwargs={'id': listid }))

def deletetask(request, id):
    this_task = Task.objects.get(id=id)
    if this_task.creator == User.objects.get(id=request.session['id']):
        this_task.delete()
    return redirect(reverse('lists:add', kwargs={'id': this_task.assignedlist.id }))
