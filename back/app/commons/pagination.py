from rest_framework.pagination import PageNumberPagination
import math
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        total_pages = math.ceil(total_items / self.page_size)

        return Response(
            {
                "count": total_items,
                "total_pages": total_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class GenreResponsePagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        total_pages = math.ceil(total_items / self.page_size)

        return Response(
            {
                "count": total_items,
                "total_pages": total_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
