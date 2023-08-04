from rest_framework import serializers

from core.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ("title", "url",)
    