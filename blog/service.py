from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


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

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'count_page': round(self.page.paginator.count/self.page_size),
            'results': data
        })