from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import ceil
import operator
from functools import reduce
from django.db.models import Q

from rest_framework import status

    
class CustomPagination:
    def custom_pagination(self, request, search_keys, serializer, queryset):
        length = request.data.get("length")
        page = request.data.get("start")
        search = request.data.get("search")
        if search:
            filters = Q()
            for key in search_keys:
                filters |= Q(**{key:search})
            queryset = queryset.filter(filters)    
        # print(queryset)    
        paginator = Paginator(queryset, length)
        try:
            paginated_data = paginator.page(page)
        except EmptyPage:
            return {"response_object": "", "total_records": 0,"start":page,"length":length}
        except Exception as error:
            # print(error, type(error), '----')
            return {"error": f"{error}", "total_records": 0,"start":page,"length":length}
        serializer = serializer(paginated_data, many=True)
        return {"response_object": serializer.data, "total_records": paginated_data.paginator.count,"start":page,"length":length}
