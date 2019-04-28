from rest_framework import viewsets

from rest_framework.response import Response

from rest_framework.decorators import action

from eye_of_providence.models import Guest, Event
from .serializers import GuestSerializer, EventSerializer


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['get'])
    def analyse(self, request, pk=None):
        event = self.get_object()
        event.analyse()
        return Response({'status': 'analysing'})

