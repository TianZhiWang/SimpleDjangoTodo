from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from todo.models import TodoItem

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','username','password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create (self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        try:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return e

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'completed', 'description')

    def create(self, validated_data):
        owner = self.context['request'].user
        todo = TodoItem.objects.create(
            owner=owner, 
            **validated_data
        )
        return todo