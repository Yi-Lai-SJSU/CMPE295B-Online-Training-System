from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Video
from django.contrib.auth.models import User
from projects.models import Project
import cv2
from images.views.ImagePredictView import predictLabel
from images.serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from .serializers import VideoSerializer
from django.http import HttpResponse, JsonResponse
from models.models import Model
from images.models import Image as MyImage
import tensorflow as tf
import os
import datetime
from PIL import Image

def objectDetectionLImages(user, project, model, timeF, uploaded_file, timestamp):
    print("inside>>>>>>>>>>>>>>>")
    print("Save Video into Database!")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    locationOfVideos = settings.MEDIA_ROOT + project.location + "videos/"

    fs = FileSystemStorage(location=locationOfVideos)
    fs.save(timestamp + uploaded_file.name, uploaded_file)

    videoFile = locationOfVideos + timestamp + uploaded_file.name
    video = Video(title=timestamp + uploaded_file.name,
                  description="default",
                  location=project.location + "videos/" + timestamp + uploaded_file.name,
                  url=settings.MEDIA_URL_DATADASE + project.location + "videos/" + timestamp + uploaded_file.name,
                  type="Detection",
                  user=user,
                  project=project)
    video.save()
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    model_path = settings.MEDIA_ROOT + model.location
    model = models.load_model(model_path, backbone_name='resnet50')
    labels_to_names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train',
                       7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign',
                       12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep',
                       19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
                       25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis',
                       31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
                       36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass',
                       41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple',
                       48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
                       54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
                       60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote',
                       66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink',
                       72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
                       78: 'hair drier', 79: 'toothbrush'}

    vc = cv2.VideoCapture(videoFile)
    c = 1
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        print('Open Error!')
        rval = False

    count = 0
    while rval:
        count = count + 1
        rval, frame = vc.read()
        if c % timeF == 0:
            image = frame
            draw = image.copy()
            draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
            image = preprocess_image(image)
            image, scale = resize_image(image)
            start = time.time()
            boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
            print("labels:", labels)
            print("processing time: resize_image", time.time() - start)
            boxes /= scale

            captions_boxes = dict()
            # visualize detections
            captions_boxes["caption"] = []
            captions_boxes["box"] = []
            captions_text = ""
            boxes_text = ""
            for box, score, label in zip(boxes[0], scores[0], labels[0]):
                # scores are sorted so we can break
                if score < 0.5:
                    break
                color = label_color(label)
                b = box.astype(int)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print(b)
                print("color:", b)
                # draw_box(draw, b, color=color)
                caption = "{} {:.3f}".format(labels_to_names[label], score)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print("caption:", caption)
                # draw_caption(draw, b, caption)
                captions_text = captions_text + "," + caption
                boxes_text = boxes_text + "," + str(b)

            # Get the folder path to save the Frame, if not exited, create a new folder
            image_folder = settings.MEDIA_ROOT + project.location + "images/" + "detected" + "/"
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)

            # Save the frame to the folder
            image_title = timestamp + str(int(c / timeF)) + '.jpg'
            image_path = image_folder + image_title
            cv2.imwrite(image_path, draw)

            # Save to the Image database
            new_image = MyImage(title=image_title,
                                location=project.location + "images/" + "detected" + "/" + image_title,
                                url=settings.MEDIA_URL_DATADASE + project.location + "images/" + "detected" + "/" + image_title,
                                description="default",
                                type="detected",
                                user=user,
                                captions=captions_text,
                                boxes=boxes_text,
                                project=project,
                                video=video,
                                isTrain=True)
            new_image.save()
        c += 1
        cv2.waitKey(1)
    vc.release()