from rest_framework import serializers
from .models import Rubric, Bb


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'name')


class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'rubric', 'content', 'price', 'published')
