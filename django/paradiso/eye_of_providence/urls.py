from django.urls import path
from . import views

app_name = "eye_of_providence"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/guest/", views.GuestListCreate.as_view()),
    path("api/guest/<str:pk>", views.GuestDetail.as_view()),
    path("api/event/", views.EventListCreate.as_view()),
    path("api/event/<str:pk>", views.EventDetail.as_view()),
]