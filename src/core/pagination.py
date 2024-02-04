"""
This module defines a custom pagination class for the app Sistemas Inteligentes.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPaginationClass(PageNumberPagination):
    """
    This class defines a custom pagination class for the Django app.

    Attributes:
        page_size (int): The number of items to include on each page. Default is 10.
        page_size_query_param (str): The query parameter to use for specifying the page size. Default is 'limit'.
    """

    page_size = 10
    page_size_query_param = 'limit'

    def get_paginated_response(self, data: list[dict]) -> Response:
        """
        Returns a paginated response containing the provided data.

        Parameters:
            data (list[dict]): The data to include in the response.

        Returns:
            Response: The paginated response containing the data.
        """

        return Response(
            {
                'total': self.page.paginator.count,
                "next": self.get_next_link(),
                "next_page": self.page.number + 1 if self.page.has_next() else None,
                "previous": self.get_previous_link(),
                "previous_page": self.page.number - 1 if self.page.has_previous() else None,
                "page": self.page.number,
                "limit": self.page.paginator.per_page,
                "pages": self.page.paginator.num_pages,
                'results': data,
            }
        )
