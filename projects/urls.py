from django.urls import path
from projects.views.ProjectsAllView import ProjectsAllView
from projects.views.ProjectView import ProjectView

urlpatterns = [
    path('all', ProjectsAllView.as_view(), name="projectAll"),
    path('<int:project_id>', ProjectView.as_view(), name="image"),
    # path('user/(?P<variable_a>(\d+))/(?P<variable_b>(\d+))/$', views.ProjectListView.as_view(), name="projectList"),
    # path('predict', views.predict),
]