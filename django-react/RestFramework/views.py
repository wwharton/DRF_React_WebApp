from rest_framework.renderers import TemplateHTMLRenderer

from .models import WsbMeta
from .serializers import WSBModelSerializer
from rest_framework import viewsets
from django.template import loader
from django.shortcuts import render


class WSBViewset(viewsets.ModelViewSet):
    queryset = WsbMeta.objects.all()
    serializer_class = WSBModelSerializer





