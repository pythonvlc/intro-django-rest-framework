from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from todo.models import Todo


class TestApi(APITestCase):

    def test_list_todos_returns_forbidden_if_user_is_not_authenticated(self):
        response = self.client.get(reverse("todo-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_todos_returns_only_authenticated_user_todos(self):
        tomas = User.objects.create_user(username="tomas", email="tomas@a.com", password="12345")
        quique = User.objects.create_user(username="quique", email="quique@a.com", password="12345")

        Todo.objects.create(owner=tomas, text="Todo 1")
        Todo.objects.create(owner=quique, text="Todo 2")

        self.client.force_authenticate(user=tomas)
        response = self.client.get(reverse("todo-list"))

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['text'], "Todo 1")

    def test_list_todos_returns_only_undone_todos(self):
        tomas = User.objects.create_user(username="tomas", email="tomas@a.com", password="12345")

        Todo.objects.create(owner=tomas, text="Todo 1", done=False)
        Todo.objects.create(owner=tomas, text="Todo 2", done=True)

        self.client.force_authenticate(user=tomas)
        response = self.client.get(reverse("todo-list"))

        self.assertEqual(response.data['count'], 1)

    def test_access_to_detail_fails_if_user_is_not_the_owner(self):
        tomas = User.objects.create_user(username="tomas", email="tomas@a.com", password="12345")
        quique = User.objects.create_user(username="quique", email="quique@a.com", password="12345")

        todo = Todo.objects.create(owner=tomas, text="Todo 1")

        self.client.force_authenticate(user=quique)
        response = self.client.get(reverse("todo-detail", kwargs={'pk': todo.pk}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_access_to_detail(self):
        tomas = User.objects.create_user(username="tomas", email="tomas@a.com", password="12345")

        todo = Todo.objects.create(owner=tomas, text="Todo 1")

        self.client.force_authenticate(user=tomas)
        response = self.client.get(reverse("todo-detail", kwargs={'pk': todo.pk}))

        self.assertEqual(response.data['text'], "Todo 1")
