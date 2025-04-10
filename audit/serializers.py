from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'


    def perform_create(self, serializer):
        instance = serializer.save()
        instance._user = self.request.user
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance._user = self.request.user
        instance.save()

    def perform_destroy(self, instance):
        instance._user = self.request.user
        instance.delete()

