from django.urls import path, include
from . import views
from .routers import router
from django.views.generic import TemplateView

app_name = "eye_of_providence"

urlpatterns = [
    path("api/", include(router.urls)),
    path("", TemplateView.as_view(template_name="eye_of_providence/index.html")),
]
