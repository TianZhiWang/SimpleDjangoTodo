from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from todo.models import TodoItem

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