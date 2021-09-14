from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from blog.models import Article
from blog.serializer import ArticleSerializer


class BlogTestCase(TestCase):
    fixtures = ['init_data.json']

    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_category(self):
        url_list_category = reverse('list_category')
        response = self.client.get(url_list_category)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertEqual({'id': 1, 'name': 'ЕГЭ'}, response.data[0])

    def test_get_article_list(self):
        url_list_article = reverse('list_article')
        response = self.client.get(url_list_article)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual([], response.data['results'])

    def test_get_single_article(self):
        url_single_article = reverse('single_article', kwargs={'pk': 1})
        response = self.client.get(url_single_article)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(None, response.data)

    def test_add_like_for_article(self):
        url_add_like_for_article = reverse('add_like', kwargs={'pk': 1})
        response = self.client.post(url_add_like_for_article)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'like': True, 'article': 1}, response.data)

        response_two = self.client.post(url_add_like_for_article)
        self.assertEqual(status.HTTP_200_OK, response_two.status_code)
        self.assertEqual({'like': False, 'article': 1}, response_two.data)

    def test_list_files(self):
        url_list_files = reverse('list_files')
        response = self.client.get(url_list_files)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
