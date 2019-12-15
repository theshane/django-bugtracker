from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
# Create your views here.
@login_required(login_url='/login')
def index(request):
    request.session['user_id'] = 1
    resp = render(request, 'index.html')
    return resp


def login_page(request):
    if request.method == "GET":
        resp = render(request, 'login.html')
        return resp
    
    if request.method == "POST":
        response = redirect('/')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return response
        else:
            response = redirect('/login')
            return response
