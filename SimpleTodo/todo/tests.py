import base64
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from todo.models import TodoItem

class TodoTests(APITestCase):

    URL = 'http://testserver/todos/'

    def setUp(self):
        self.user = User.objects.create_user("user", "password123")
        self.user.save()
        self.user1 = User.objects.create_user("user1", "password123")
        self.user1.save()

    def test_get_unauth_todos(self):
        """ GET the todos without any auth will result in a 403 """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_todos_success(self):
        """ GET with auth should return a 2XX """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.URL)
        self.assertTrue(status.is_success(response.status_code))

    def test_get_correct_todos(self):
        """ GET should return todos """
        todo = TodoItem.objects.create(
            owner=self.user, description="Todo Description", completed=False)
        todos_expected = [{
            'url': self.URL+str(todo.id)+'/',
            'completed': todo.completed,
            'description': todo.description
        }]
        self.client.force_authenticate(self.user)
        response = self.client.get(self.URL)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEquals(json.loads(response.content), todos_expected)

    def test_todo_get_only_users_todos(self):
        """ GET should only return todos that user owns"""
        todo = TodoItem.objects.create(
            owner=self.user, description="Todo Description", completed=False)
        other_users_todo = TodoItem.objects.create(
            owner=self.user1, description="Todo Description", completed=False)

        todos_expected = [{
            'url': self.URL + str(todo.id) + '/',
            'completed': todo.completed,
            'description': todo.description
        }]
        self.client.force_authenticate(self.user)
        response = self.client.get(self.URL)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEquals(json.loads(response.content), todos_expected)

    def test_get_todo(self):
        """ GET single todo item with id """
        todo = TodoItem.objects.create(
            owner=self.user, description="Todo Description", completed=False
        )
        todoExpected = {'url': self.URL + str(todo.id) + '/',
                        'completed': todo.completed,
                        'description': todo.description
                        }
        self.client.force_authenticate(self.user)
        response = self.client.get(self.URL + str(todo.id) + '/')
        self.assertTrue(status.is_success(response.status_code))
        self.assertEquals(json.loads(response.content), todoExpected)

    def test_get_unauth_todo(self):
        """ GET single todo item with id should 403 if not owned by user """
        todo = TodoItem.objects.create(
            owner=self.user1, description="Todo Description", completed=False
        )
        self.client.force_authenticate(self.user)
        response = self.client.get(self.URL + str(todo.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_todo(self):
        """ POST todo should add item to database """
        todo = {'completed': False,
                'description': "Todo Description"
                }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.URL, todo)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(TodoItem.objects.count() == 1)
        id = json.loads(response.content)['url'].split('/')[-2]
        inserted_todo = TodoItem.objects.get(pk=id)
        self.assertEqual(todo['completed'], inserted_todo.completed)
        self.assertEqual(todo['description'], inserted_todo.description)

    def test_update_todo(self):
        """ PUT single todo with id should edit item in database """
        todo = TodoItem.objects.create(
            owner=self.user, description="Todo Description", completed=False
        )
        updated_todo = {'completed': True,
                    'description': "Todo Description 2"
                }
        self.client.force_authenticate(self.user)
        response = self.client.put(self.URL + str(todo.id) + '/', updated_todo)
        self.assertTrue(status.is_success(response.status_code))
        inserted_todo = TodoItem.objects.get(pk=todo.id)
        self.assertEqual(updated_todo['completed'], inserted_todo.completed)
        self.assertEqual(updated_todo['description'], inserted_todo.description)

    def test_update_unauth_todo(self):
        """ PUT single todo with id should 403 if not owned by user """
        todo = TodoItem.objects.create(
            owner=self.user1, description="Todo Description", completed=False
        )
        updated_todo = {'completed': True,
                    'description': "Todo Description 2"
                }
        self.client.force_authenticate(self.user)
        response = self.client.put(self.URL + str(todo.id) + '/', updated_todo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        inserted_todo = TodoItem.objects.get(pk=todo.id)
        self.assertEqual(todo.completed, inserted_todo.completed)
        self.assertEqual(todo.description, inserted_todo.description)

    def test_delete_todo(self):
        """ DELETE single todo with id should delete item in database """
        todo = TodoItem.objects.create(
            owner=self.user, description="Todo Description", completed=False
        )
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.URL + str(todo.id) + '/')
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(TodoItem.objects.count() == 0)

    def test_delete_unauth_todo(self):
        """ DELETE single todo with id should 403 if not owned by user """
        todo = TodoItem.objects.create(
            owner=self.user1, description="Todo Description", completed=False
        )
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.URL + str(todo.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(TodoItem.objects.count() == 1)

