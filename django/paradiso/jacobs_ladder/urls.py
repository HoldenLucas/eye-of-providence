from django.urls import path
from . import views

app_name = "jacobs_ladder"

urlpatterns = [path("", views.index, name="index")]
