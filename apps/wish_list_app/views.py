from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def main(request):
    return redirect('/main')

def index(request):
    return render(request, 'wish_list_app/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        # query for username
        q = User.objects.filter(username=request.POST['username'])
        if q.count() > 0:
            # check for existing user
            messages.error(request, "A user account with that username already \
            exists", extra_tags="username")
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            q = User.objects.create(name = request.POST['name'], username = request.POST['username'], password=hashed_pw)
            request.session['user_id'] = q.id
            request.session['username'] = q.username
            return redirect('/success')
    return redirect('/')

def log_in(request):
    # check user for that username
    # then check password
    found_users = User.objects.filter(username=request.POST['username'])
    if found_users.count() > 0:
        # check password
        found_user = found_users.first()
        if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) is True:
            # log in user
            request.session['user_id'] = found_user.id  # user_id from username query
            request.session['username'] = found_user.username
            return redirect('/success')
        else:
            messages.error(request, "Login Failed", extra_tags="username")
            return redirect('/')
    else:
        messages.error(request, "Invalid login", extra_tags="username")
        return redirect('/')

def success(request):
    ''' Redirects user to /dashboard if user passes login() or register() '''
    return redirect('/dashboard')

def dashboard(request):
    context = {
        "my_items": Item.objects.filter(poster__id = request.session['user_id']),
        "other_items_added": Item.objects.filter(users__id = request.session['user_id']),
        "all_items": Item.objects.exclude(users__id = request.session['user_id']).exclude(poster__id = request.session['user_id']),
        "poster_username": User.objects.get(id = request.session['user_id']).username
    }
    return render(request, 'wish_list_app/dashboard.html', context)

def post_item(request):
    if request.method == "POST":
        errors = Item.objects.basic_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/post_item')
        else:
            q = Item.objects.create(item = request.POST['item'],poster = User.objects.get(id = request.session['user_id']))
            return redirect('/dashboard')
    else:
        return render(request, 'wish_list_app/add.html')

def join(request, id):  
    if request.method == "POST":
        user_query = User.objects.get(id=request.session['user_id'])
        user_query.save()
        item_query = Item.objects.get(id=id)  # here, second id = trip_id
        item_query.save()
        
        item_query.users.add(user_query)
       
        print "Added user #", request.session['user_id'], "to item #", item_query
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def wish_items(request, id):  
    context = {
        "joiners": User.objects.filter(items__id = id),  
        "item_info": Item.objects.get(id = id)
    }
    print context
    return render(request, 'wish_list_app/wish_items.html', context)

def remove(request):
    Item.objects.get(id = request.POST['item_item']).delete()
    return redirect('/dashboard')




