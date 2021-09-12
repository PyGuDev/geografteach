from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from chat.models import Chat
from user.models import User


class BaseTestCase(TestCase):
    user: User

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='email@email.ru', password='password')
        cls.user.is_active = True
        cls.user.save()

    def setUp(self) -> None:
        self.client = APIClient()
        token = self.get_auth_token()
        self.client.force_authenticate(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def get_auth_token(self):
        sing_in_url = reverse('sing_in')
        response = self.client.post(sing_in_url, data={'email': 'email@email.ru', 'password': 'password'})
        return response.data['access']


class ChatTestCase(BaseTestCase):

    def test_create_chat(self):
        create_chat_url = reverse('create_chat')
        response = self.client.post(create_chat_url)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user.id, response.data['student'])

        response_two = self.client.post(create_chat_url)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_two.status_code)


class MessageTestCase(BaseTestCase):
    chat: Chat

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.chat = Chat(student=cls.user)
        cls.chat.save()

    def test_create_message(self):
        create_msg_url = reverse('create_message', kwargs={'pk': self.chat.id})
        data = {'text': 'Hello, my friends'}
        response = self.client.post(create_msg_url, data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.chat.id, response.data['chat'])

    def test_get_list_message(self):
        list_message_url = reverse('list_message', kwargs={'pk': self.chat.id})

        response = self.client.get(list_message_url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
