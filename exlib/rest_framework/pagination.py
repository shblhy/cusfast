# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageCodePagination(PageNumberPagination):
    """
        自定义返回数据结构
    """
    page_size = 10
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 0),
            ('msg', ''),
            ('total', self.page.paginator.count),
            ('page', self.page.number),
            ('page_size', self.page.paginator.per_page),
            ('data', data)
        ]))


class LargePageCodePagination(PageCodePagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 200
