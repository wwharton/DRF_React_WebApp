from rest_framework import serializers
from .models import WsbMeta


class WSBModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WsbMeta
        fields = ('bears', 'bulls')