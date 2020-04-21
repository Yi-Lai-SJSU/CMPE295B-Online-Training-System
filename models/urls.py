from django.urls import path
from . import views
from models.views.ModelsAllView import ModelsAllView
from models.views.ModelView import ModelView

urlpatterns = [
    path('all', ModelsAllView.as_view(), name="modelList"),
    path('<int:model_id>', ModelView.as_view(), name="model")
    # path('user/(?P<variable_a>(\d+))/(?P<variable_b>(\d+))/$', views.ProjectListView.as_view(), name="projectList"),
    # path('predict', views.predict),
]