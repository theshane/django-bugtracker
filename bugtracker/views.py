from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        resp = render(request, "index.html")
        return resp


class LoginView(View):
    def get(self, request):
        resp = render(request, "login.html")
        return resp

    def post(self, request):
        response = redirect("/")
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return response
        else:
            response = redirect("/login")
            return response


# class ProjectsApiView(LoginRequiredMixin, View):
#     def get(self, request):
