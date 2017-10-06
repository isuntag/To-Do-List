from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, List, Task, Company
from datetime import datetime
import bcrypt
from django.utils import timezone

def index(request):
    if 'id' not in request.session:
        return redirect('/login')
    else:
        content = {
            'lists': List.objects.filter(users__id=request.session['id']),
            'user': User.objects.get(id=request.session['id']),
            'all_users': User.objects.all()
        }
        return render(request, 'app/index.html', content)

def company(request):
    if 'id' not in request.session:
        return redirect('/login')
    else:
        content = {
            'all_lists': List.objects.all()
        }
        return render(request, 'app/company.html', content)

def createlist(request, id):
    if request.method == 'POST':
        errors = List.objects.validation(request.POST)
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='list')
        else:
            this_user = User.objects.get(id=request.session['id'])
            this_list = List.objects.create(title=request.POST['title'], description=request.POST['description'], creator=this_user)
            this_list.users.add(this_user)
        if id != '0':
            return redirect('/lists/'+id)
        else:
            return redirect('/')
    else:
        return redirect('/')

def adduserlist(request, id):
    if request.method == 'POST' and 'user' in request.POST:
        this_list = List.objects.get(id=id)
        if this_list.creator == User.objects.get(id=request.session['id']):
            this_list.users.add(User.objects.get(id=request.POST['user']))
    return redirect('/')

def removeuserlist(request, id):
    if request.method == 'POST' and 'user' in request.POST:
        this_list = List.objects.get(id=id)
        if this_list.creator == User.objects.get(id=request.session['id']) and User.objects.get(id=request.POST['user']) != this_list.creator:
            this_list.users.remove(User.objects.get(id=request.POST['user']))
    return redirect('/')

def deletelist(request, id):
    this_list = List.objects.get(id=id)
    if this_list.creator == User.objects.get(id=request.session['id']):
        this_list.delete()
    return redirect('/')

def viewlist(request, id):
    if 'id' not in request.session:
        return redirect('/login')
    elif User.objects.get(id=request.session['id']) not in List.objects.get(id=id).users.all():
        return redirect('/')
    else:
        content = {
            'this_list': List.objects.get(id=id),
            'my_todo_tasks': List.objects.get(id=id).tasks.filter(completed=0, users__id=request.session['id']).order_by('due_date'),
            'other_todo_tasks': List.objects.get(id=id).tasks.filter(completed=0).exclude(users__id=request.session['id']).order_by('due_date'),
            'my_completed_tasks': List.objects.get(id=id).tasks.filter(completed=1, users__id=request.session['id']).order_by('due_date'),
            'other_completed_tasks': List.objects.get(id=id).tasks.filter(completed=1).exclude(users__id=request.session['id']).order_by('due_date'),
            'lists': List.objects.filter(users__id=request.session['id']),
            'user': User.objects.get(id=request.session['id']),
            'all_users': User.objects.all()
        }
        return render(request, 'app/viewlist.html', content)

def createtask(request, listid):
    if request.method == 'POST':
        errors = Task.objects.validation(request.POST)
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='task')
        else:
            this_user = User.objects.get(id=request.session['id'])
            this_list = List.objects.get(id=listid)
            this_task = Task.objects.create(title=request.POST['title'], due_date=request.POST['due_date'], assignedlist=this_list, creator=this_user)
            this_task.users.add(this_user)
        return redirect('/lists/'+listid)
    else:
        return redirect('/')

def addusertask(request, id):
    if request.method == 'POST':
        this_task = Task.objects.get(id=id)
        if this_task.creator == User.objects.get(id=request.session['id']):
            this_task.users.add(User.objects.get(id=request.POST['user']))
    return redirect('/lists/'+str(this_task.assignedlist.id))

def removeusertask(request, id):
    if request.method == 'POST' and 'user' in request.POST:
        this_task = Task.objects.get(id=id)
        if this_task.creator == User.objects.get(id=request.session['id']) and User.objects.get(id=request.POST['user']) != this_task.creator:
            this_task.users.remove(User.objects.get(id=request.POST['user']))
    return redirect('/lists/'+str(this_task.assignedlist.id))

def changetaskstatus(request, taskid, listid):
    this_task = Task.objects.get(id=taskid)
    this_user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        if this_user in this_task.users.all():
            this_task.completed = not this_task.completed
            this_task.save()
    return redirect('/lists/'+listid)

def deletetask(request, id):
    this_task = Task.objects.get(id=id)
    if this_task.creator == User.objects.get(id=request.session['id']):
        this_task.delete()
    return redirect('/')

def admin(request):
    if 'id' not in request.session:
        return redirect('/login')
    elif not User.objects.get(id=request.session['id']).is_admin:
        return redirect('/')
    else:
        content = {
            'users': User.objects.all()
        }
        return render(request, 'app/admin.html', content)

def login(request):
    if 'id' in request.session:
        return redirect('/')
    else:
        return render(request, "app/login.html")

def register(request, id):
    errors = User.objects.validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='register')
        return redirect('/login')
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        admin = 0
        if User.objects.all().count() < 1:
            admin = 1
        newUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwhash, admin=admin)
        request.session['email'] = request.POST['email']
        request.session['first_name'] = request.POST['first_name']
        request.session['id'] = User.objects.get(email=request.POST['email']).id
        if id:
            return redirect('/admins')
        return redirect('/')

def admin_registered(request):
    errors = User.objects.admin_created_user(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='register')
    else:
        pwhash = bcrypt.hashpw('changeme'.encode(), bcrypt.gensalt())
        newUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwhash)
    return redirect('/admins')

def updateuser(request, id):
    errors = User.objects.update_user(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='register')
    else:
        this_user = User.objects.get(id=id)
        this_user.first_name = request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        this_user.save(update_fields=['first_name', 'last_name', 'password'])
    return redirect('/users/'+id)

def signin(request):
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='login')
        return redirect('/login')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['email'] = user.email
        request.session['first_name'] = user.first_name
        request.session['id'] = user.id
        if user.password == bcrypt.hashpw('changeme'.encode(), user.password.encode()):
            return redirect('/users/'+str(request.session['id']))
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/login')

def userpage(request, id):
    if 'id' not in request.session:
        return redirect('/login')
    else:
        content = {
            'user': User.objects.get(id=id)
        }
        return render(request, 'app/userpage.html', content)
