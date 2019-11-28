from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^demo', Demo.as_view()),
]
