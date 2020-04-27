from django.urls import path
from images.views.ImageView import ImageView
from images.views.ImagesByTagsView import ImagesByTagsView
from images.views.ImagesAllView import ImagesAllView
from images.views.ImagePredictView import ImagePredict
from images.views.ImageTypeView import ImageTypeView
from images.views.ImagesByVideoView import ImagesByVideoView

urlpatterns = [
    path('all', ImagesAllView.as_view(), name="imageList"),
    path('type', ImageTypeView.as_view(), name='imageType'),
    path('predict', ImagePredict.as_view(), name="imagePredict"),
    path('byVideo/<int:video_id>', ImagesByVideoView.as_view(), name='imageByVideo'),
    path('<int:image_id>', ImageView.as_view(), name="image"),
    path('<str:image_tag>', ImagesByTagsView.as_view(), name="imageByTags"),
]