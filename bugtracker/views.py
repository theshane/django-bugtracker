from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import bugtracker.models as models


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


class ProjectHandler(LoginRequiredMixin, View):
    def post(self, request):
        new_project = models.Project(
            title=request.POST["title"],
            description=request.POST["description"],
            project_status=models.Status.objects.get(id=1),
            created_by=request.user,
        )
        new_project.save()
        return JsonResponse(new_project.to_dict())


class ProjectDetailsHandler(LoginRequiredMixin, View):
    def post(self, request, project_id=0):
        project_to_update = models.Project.objects.get(id=project_id)
        project_to_update.project_status = models.Status.objects.get(
            id=request.POST.get("project_status", 1)
        )
        project_to_update.title = request.POST.get("title", "")
        project_to_update.description = request.POST.get("description", "")
        project_to_update.save()
        return JsonResponse(project_to_update.to_dict())


class ProjectListHandler(LoginRequiredMixin, View):
    def get(self, request):
        project_array = []
        projects = models.Project.objects.all()
        for project in projects:
            project_array.append(project.to_dict())
        return JsonResponse(project_array, safe=False)
