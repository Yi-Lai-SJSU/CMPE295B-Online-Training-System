from __future__ import absolute_import, unicode_literals
# from __future__ import absolute_import, unicode_literals
# https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
# https://ruddra.com/posts/docker-do-stuff-using-celery-using-redis-as-broker/   * main ref
# https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/
# https://mopitz199.github.io/docs/celery-redis-django-docker.html

import os
from celery import Celery
import logging
from .customized import train
# from models.customized import train
from django.conf import settings
from django.apps import apps
import datetime

# https://ruddra.com/posts/docker-do-stuff-using-celery-using-redis-as-broker/

logger = logging.getLogger("Celery")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlphaProject.settings')

app = Celery('celery_tasks.tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def train_mode(param1, param2):
    # project_folder = getProjectFolder(param2)
    Model = apps.get_model(app_label='models', model_name='model')
    Project = apps.get_model(app_label='projects', model_name='project')
    User = apps.get_model(app_label='auth', model_name='User')
    # user = User.objects.get(id=param2[0])
    # project = Project.objects.get(id=param2[1])
    print("*(((((((((((((((((((((>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(param2)
    print(type(param2))
    model = Model.objects.get(id=param2)
    print(model.id)
    print("&***&*&*&**************************************")
    print(model.project.location)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
    train(settings.MEDIA_ROOT + model.project.location, timestamp)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(param2)
    # https://stackoverflow.com/questions/57666355/cannot-import-models-into-celery-tasks-in-django
    # It works well!
    # print(user.id)
    # print(user.username)
    # print(project.title)
    model.status = "Trained"
    model.save()
    locationOfModel = os.path.abspath(os.path.dirname(__file__))
    print(locationOfModel)

# def getProjectFolder(param2):
#     project_folder = settings.MEDIA_ROOT + str(param2[0]) + "/" + param2[1] + "/"
#     return project_folder





