from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Sum, Case, When, IntegerField
from .models import List
from ..users_app.models import User

# Create your views here.
def createviewlist(request, id):
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
            return redirect(reverse('lists:add', kwargs={'id': id }))
        else:
            return redirect(reverse('users:index'))
    if request.method == 'GET':
        if 'id' not in request.session:
            return redirect(reverse('users:loginpage'))
        elif User.objects.get(id=request.session['id']) not in List.objects.get(id=id).users.all():
            return redirect(reverse('users:index'))
        else:
            content = {
                'this_list': List.objects.get(id=id),
                'all_tasks': List.objects.get(id=id).tasks.all(),
                'my_todo_tasks': List.objects.get(id=id).tasks.filter(completed=0, users__id=request.session['id']).order_by('due_date'),
                'other_todo_tasks': List.objects.get(id=id).tasks.filter(completed=0).exclude(users__id=request.session['id']).order_by('due_date'),
                'completed_tasks': List.objects.get(id=id).tasks.filter(completed=1).order_by('due_date'),
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
            lists = List.objects.filter(users__id=request.session['id'])
            for listy in lists:
                num_tasks = listy.tasks.filter(completed=0).count()
            return render(request, 'lists_app/viewlist.html', content, lists)

def adduserlist(request, id):
    if request.method == 'POST' and 'user' in request.POST:
        this_list = List.objects.get(id=id)
        if this_list.creator == User.objects.get(id=request.session['id']):
            this_list.users.add(User.objects.get(id=request.POST['user']))
    return redirect(reverse('users:index'))

def removeuserlist(request, id):
    if request.method == 'POST' and 'user' in request.POST:
        this_list = List.objects.get(id=id)
        if this_list.creator == User.objects.get(id=request.session['id']) and User.objects.get(id=request.POST['user']) != this_list.creator:
            this_list.users.remove(User.objects.get(id=request.POST['user']))
    return redirect(reverse('users:index'))

def deletelist(request, id):
    this_list = List.objects.get(id=id)
    if this_list.creator == User.objects.get(id=request.session['id']):
        this_list.delete()
    return redirect(reverse('users:index'))
