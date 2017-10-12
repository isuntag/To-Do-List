from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Sum, Case, When, IntegerField
import bcrypt
from .models import User, Company
from ..lists_app.models import List

# Create your views here.
def index(request):
    if 'id' not in request.session:
        return redirect(reverse('users:loginpage'))
    else:
        content = {
            'lists': List.objects.filter(users__id=request.session['id']).annotate(num_tasks=Sum(
                Case(
                    When(tasks__completed=0, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )),
            'user': User.objects.get(id=request.session['id']),
            'all_users': User.objects.all()
        }
        return render(request, 'users_app/index.html', content)

def company(request):
    if 'id' not in request.session:
        return redirect(reverse('users:loginpage'))
    else:
        content = {
            'all_lists': List.objects.filter(users__id=request.session['id']).annotate(num_tasks=Sum(
                Case(
                    When(tasks__completed=0, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )),
            'user': User.objects.get(id=request.session['id']),
            'all_users': User.objects.all()
        }
        return render(request, 'users_app/company.html', content)

def loginpage(request):
    if request.method=='GET':
        if 'id' in request.session:
            return redirect(reverse('users:index'))
        else:
            return render(request, "users_app/login.html")
    if request.method=='POST':
        errors = User.objects.validation(request.POST)
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='register')
            return redirect(reverse('users:loginpage'))
        else:
            pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            admin = 0
            if User.objects.all().count() < 1:
                admin = 1
            newUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwhash, admin=admin)
            request.session['email'] = request.POST['email']
            request.session['first_name'] = request.POST['first_name']
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            return redirect(reverse('users:index'))

def admin(request):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['id'])
        if current_user.is_admin and current_user != User.objects.get(id=request.POST['id']):
            user = User.objects.get(id=request.POST['id'])
            user.admin = not user.admin
            user.save()
        return redirect(reverse('users:admin'))
    if request.method == 'GET':
        if 'id' not in request.session:
            return redirect(reverse('users:loginpage'))
        elif not User.objects.get(id=request.session['id']).is_admin:
            return redirect(reverse('users:index'))
        else:
            content = {
                'user': User.objects.get(id=request.session['id']),
                'users': User.objects.all().annotate(num_tasks=Sum(
                    Case(
                        When(tasks__completed=0, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )),
            }
            return render(request, 'users_app/admin.html', content)

def admin_registered(request):
    errors = User.objects.admin_created_user(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='register')
    else:
        pwhash = bcrypt.hashpw('changeme'.encode(), bcrypt.gensalt())
        newUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwhash)
    return redirect(reverse('users:admin'))

def user(request, id):
    if request.method == 'POST':
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
        return redirect(reverse('users', kwargs={'id': id }))
    if request.method == 'GET':
        if 'id' not in request.session:
            return redirect(reverse('users:loginpage'))
        else:
            content = {
                'user': User.objects.get(id=id)
            }
            return render(request, 'users_app/userpage.html', content)

def signin(request):
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags='login')
        return redirect(reverse('users:loginpage'))
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['email'] = user.email
        request.session['first_name'] = user.first_name
        request.session['id'] = user.id
        if user.password == bcrypt.hashpw('changeme'.encode(), user.password.encode()):
            return redirect(reverse('users:users', kwargs={'id': request.session['id'] }))
        return redirect(reverse('users:index'))

def logout(request):
    request.session.clear()
    return redirect(reverse('users:loginpage'))