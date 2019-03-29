from django.urls import path

from . import views

app_name = "eye_of_providence"

urlpatterns = [
    path("test", views.test, name="test"),
    path("", views.index, name="index"),
    path("manage_guests", views.ManageGuests.as_view(), name="guest-manage"),
    path("manage_events", views.ManageEvents.as_view(), name="event-manage"),
    path("view_guest/<str:pk>", views.GuestDetailView.as_view(), name="detail-guest"),
    path("view_event/<str:pk>", views.EventDetailView.as_view(), name="detail-event"),
    path("delete_guest/<str:pk>", views.GuestDelete.as_view(), name="delete-guest"),
    path("delete_event/<str:pk>", views.EventDelete.as_view(), name="delete-event"),
    path("api/guest/", views.GuestListCreate.as_view()),
]
