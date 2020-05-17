from django.urls import path
from projects.views.ProjectsAllView import ProjectsAllView
from projects.views.ProjectView import ProjectView

urlpatterns = [
    path('all', ProjectsAllView.as_view(), name="projectAll"),
    path('<int:project_id>', ProjectView.as_view(), name="image"),
]