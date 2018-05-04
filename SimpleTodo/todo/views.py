from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from todo.models import TodoItem
from todo.serializers import TodoSerializer, UserSerializer
from todo.permissions import IsOwnerOrAdmin, UserPermissions

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users to be registered.
    GET /users/:id: Returns User Detail - Must be the User or staff
    GET /users/: Returns list of users - Staff
    POST /users/: Create User - All
    PUT /users/:id: Edit User - Staff
    DELETE /users/:id: Delete User - Staff
    """
    permission_classes = (UserPermissions,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows todos to be viewed or edited.
    GET /todos/:id: Returns Todo Detail - Owner and Staff
    GET /todos/: Returns list of own Todos - Owner and Staff
    POST /todos/: Create Todo - Users
    PUT /todos/:id: Edit Todo - Owner and Staff
    DELETE /todos/:id: Delete Todo - Owner and Staff
    """
    permission_classes = (IsAuthenticated,IsOwnerOrAdmin,)
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
