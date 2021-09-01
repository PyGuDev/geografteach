from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

from blog.models import Article


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PaginationApp(PageNumberPagination):
    """Пагинация"""
    page_size = 7
    max_page_size = 1000

    def get_paginated_response(self, data):

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': math.ceil(self.page.paginator.count / self.page_size),
            'results': data
        })

