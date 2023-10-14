from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    coordinates = CoordsSerializer(read_only=True)
    levels = LevelSerializer(read_only=True)
    images = ImagesSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Pereval
        fields = '__all__'
