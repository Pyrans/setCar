from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'byCar'
urlpatterns = [
    # url('admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^addplan/', views.AddPlanAPI.as_view()),
    url(r'^addcar/', views.AddCarAPI.as_view())
]
