from django.urls import path
from . import views
from videos.views.VideosAllView import VideosAllView
from videos.views.VideoView import VideoView
urlpatterns = [
    path('all', VideosAllView.as_view(), name="videoList"),
    path('<int:video_id>', VideoView.as_view(), name="video")
    # path('user/(?P<variable_a>(\d+))/(?P<variable_b>(\d+))/$', views.ProjectListView.as_view(), name="projectList"),
    # path('predict', views.predict),
]