from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("api/project", views.ProjectHandler.as_view(), name="project"),
    path(
        "api/project/<int:project_id>",
        views.ProjectDetailsHandler.as_view(),
        name="single_project",
    ),
    path("api/projects", views.ProjectListHandler.as_view(), name="projects"),
]
