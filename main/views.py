from django.shortcuts import render , HttpResponse, redirect
from django.contrib import messages
from .models import User, Listing
import bcrypt
from PIL import Image
from .forms import ImageForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    pw_hash = bcrypt.hashpw(request.POST['pw'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User.objects.create(
        first = request.POST['first'],
        last= request.POST['last'],
        email= request.POST['email'],
        password= pw_hash
        )
    request.session['user_id'] = new_user.id
    messages.success(request, 'Thats it!')
    return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    list_of_users = User.objects.filter(email=request.POST['email'])
    if len(list_of_users) > 0:
        user = list_of_users[0]
        print(user)
        if bcrypt.checkpw(request.POST['pw'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            errors['incorrect'] = 'Your email or password is incorrect'

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_in_user': logged_in_user,
        'all_listings': Listing.objects.all()
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def listing(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    form= ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        newform = Listing(docfile = request.FILES['docfile'])
        newform.save()
    context= {
        'form': form
            }

    return render(request, 'newlisting.html', context)

def addListing(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    Listing.objects.create(
        title= request.POST['title'],
        desc=request.POST['desc'],
        posted_by= logged_in_user,
        price=request.POST['price'],
        location=request.POST['location'],
        img=request.POST['img']
    )
    return redirect('/dashboard')

def viewListing(request, num):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    item = Listing.objects.get(id=num)
    form= ImageForm(request.POST or None, request.FILES or None)
    context ={
        'form': form,
        'logged_in_user': logged_in_user,
        'item': item
    }
    return render(request, 'viewlisting.html', context)

def updateListing(request, num):
    to_update = Listing.objects.get(id=num)
    form= ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        to_update.title = request.POST['title']
        to_update.desc = request.POST['desc']
        to_update.img = request.FILES['img']
        to_update.price = request.POST['price']
        to_update.condition= request.POST['condition']
        to_update.location = request.POST['location']
        to_update.save()
    return redirect('/dashboard')

def deleteListing(request, num):
    to_delete = Listing.objects.get(id=num)
    to_delete.delete()
    return redirect('/dashboard')