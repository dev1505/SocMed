from rest_framework import serializers

from .models import UserMessages


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:  # type:ignore
        model = UserMessages
        fields = "__all__"
