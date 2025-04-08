from .models import Program, DailyStudy
from rest_framework import serializers


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'title', 'created_at']

    def create(self, validated_data):
        return Program.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  
        return instance


class DailyStudySerializer(serializers.ModelSerializer):
    program = serializers.SlugRelatedField(slug_field="title", queryset=Program.objects.all())
    class Meta:
        model = DailyStudy
        fields = ['id', 'program', 'date', 'title', 'content', 'created_at']
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }
    
    def create(self, validated_data):
        return DailyStudy.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  
        return instance