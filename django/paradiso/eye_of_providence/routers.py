from rest_framework import routers
from .viewsets import GuestViewSet, EventViewSet

router = routers.DefaultRouter()

router.register(r'guest', GuestViewSet)
router.register(r'event', EventViewSet)
