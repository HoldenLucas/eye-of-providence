from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.shortcuts import render

from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView

from .models import Guest, Event

from .serializers import GuestSerializer
from rest_framework import generics


def index(request):
    return render(
        request, "eye_of_providence/index.html", context={"events": Event.objects.all()}
    )


class ManageGuests(CreateView):
    template_name = "eye_of_providence/guest_form.html"
    model = Guest
    fields = ["name", "photo"]
    success_url = reverse_lazy("eye_of_providence:guest-manage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guests"] = Guest.objects.all()
        return context


class GuestDetailView(DetailView):
    template_name = "eye_of_providence/guest.html"
    model = Guest


class GuestDelete(DeleteView):
    template_name = "eye_of_providence/guest_confirm_delete.html"
    model = Guest
    success_url = reverse_lazy("eye_of_providence:guest-manage")


# TODO: remove CBV
# def get_guest(request):
#     if request.method == "POST":
# c         form = GuestForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect("eye_of_providence/index.html")
#     else:
#         form = GuestForm()

#     return render(request, "get_guest.html", {"form": form})


class ManageEvents(CreateView):
    template_name = "eye_of_providence/event_form.html"
    model = Event
    fields = ["date", "video"]
    success_url = reverse_lazy("eye_of_providence:event-manage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all()
        return context


class EventDelete(DeleteView):
    template_name = "eye_of_providence/event_confirm_delete.html"
    model = Event
    success_url = reverse_lazy("eye_of_providence:event-manage")


class EventDetailView(DetailView):
    template_name = "eye_of_providence/event.html"
    model = Event


def test(request):
    # if request.method == "GET":
    #     template_name = "eye_of_providence/test.html"
    #     data = {}
    #     data["message"] = "hi!"
    #     return render(request, template_name, data)
    # else:
    #     pass
    data = {"this is a ": "test"}
    return JsonResponse(data)

class GuestListCreate(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer