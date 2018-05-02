from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todo.models import TodoItem
from todo.serializers import TodoSerializer
from todo.permissions import IsOwner

class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows todos to be viewed or edited.
    """
    permission_classes = (IsOwner,)
    queryset = TodoItem.objects.all()
    serializer_class = TodoSerializer

    def list(self, request):
        queryset = TodoItem.objects.filter(owner=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
