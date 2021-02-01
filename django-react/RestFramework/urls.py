from django.urls import path
from django.views.generic import TemplateView

from . import views
from rest_framework import routers
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings




router = routers.SimpleRouter()
router.register(r'wsb', views.WSBViewset)
urlpatterns = router.urls

