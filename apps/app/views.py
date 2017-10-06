from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, List, Task, Company
from datetime import datetime
import bcrypt

def index(request):
    if 'email' not in request.session:
        return redirect('/login')
    else:
        content = {
            'lists': List.objects.all()
        }
        return render(request, 'app/index.html', content)

def company(request):
    if 'email' not in request.session:
        return redirect('/login')
    else:
        return render(request, 'app/company.html')

def createlist(request):
    if request.method == 'POST':
        errors = List.objects.validation(request.POST)
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='list')
        else:
            this_user = User.objects.get(id=request.session['id'])
            this_list = List.objects.create(title=request.POST['title'], description=request.POST['description'])
            this_list.users.add(this_user)
    return redirect('/')

def viewlist(request, id):
    content = {
        'this_list': List.objects.get(id=id),
        'this_list_tasks': List.objects.get(id=id).tasks.all(),
        'lists': List.objects.all()
    }
    return render(request, 'app/viewlist.html', content)

def admin(request):
    if 'email' not in request.session:
        return redirect('/login')
    else:
        return render(request, 'app/admin.html')

def login(request):
    if 'email' in request.session:
        return redirect('/')
    else:
        return render(request, "app/login.html")

def register(request):
    errors = User.objects.validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='register')
        return redirect('/login')
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwhash)
        request.session['email'] = request.POST['email']
        request.session['first_name'] = request.POST['first_name']
        request.session['id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/')
def signin(request):
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='login')
        return redirect('/login')
    else:
        request.session['email'] = User.objects.get(email=request.POST['email']).email
        request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
        request.session['id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/login')
