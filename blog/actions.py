from rest_framework.request import Request

from blog.models import Like, Article
from blog.service import get_client_ip
from django_project.exceptions import BadRequestException


class LikeArticle:
    def __init__(self, request: Request, pk_article: int):
        self._request = request
        self._pk_article = pk_article

    def add_like(self):
        like, created = Like.objects.get_or_create(ip=get_client_ip(self._request), article=self._get_article())
        if created:
            like.is_like = True
        else:
            like.is_like = not like.is_like
        like.save()

        return self._generate_response_data(like)

    def _get_article(self):
        try:
            return Article.objects.get(pk=self._pk_article)
        except Article.DoesNotExist:
            raise BadRequestException(
                message='An article with this id={} was not found'.format(self._pk_article),
                code='not_found'
            )

    @staticmethod
    def _generate_response_data(like: Like):
        return {
            'like': like.is_like,
            'article': like.article.id
        }
