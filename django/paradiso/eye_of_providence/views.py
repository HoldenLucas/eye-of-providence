from rest_framework import generics
from .serializers import GuestSerializer, EventSerializer
from django.shortcuts import render


from .models import Guest, Event

def index(request):
    guests = Guest.objects.all()
    events = Event.objects.all()

    return render(request, "eye_of_providence/index.html", context={"guests": guests, "events": events})

class GuestListCreate(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class GuestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class EventListCreate(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
