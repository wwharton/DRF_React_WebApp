from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request, settings.BASE_DIR / "django-react/templates/index.html")