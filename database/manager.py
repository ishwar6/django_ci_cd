from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.db import connection, connections
from django.db.models.signals import pre_migrate, post_migrate
from django.dispatch import receiver

class QueryOptimizationMiddleware(MiddlewareMixin):
    """
    Middleware that optimizes query performance for dynamically generated models.
    """

    def process_request(self, request):
        """
        Process incoming requests to apply query optimizations.
        
        :param request: Django HTTP request object
        """
        pass

    def process_response(self, request, response):
        """
        Process the response to include query performance metrics and manage cache.
        
        :param request: Django HTTP request object
        :param response: Django HTTP response object
        :return: Modified response object
        """
        if connection.queries:
            total_time = sum(float(query['time']) for query in connection.queries)
            response['X-Query-Time'] = f"{total_time:.2f}s"
        
        return response

    def cache_query(self, key, query_function, *args, **kwargs):
        """
        Cache the result of a database query to reduce load on repeated access.
        
        :param key: Cache key
        :param query_function: Function that executes the query
        :return: Cached or freshly queried data
        """
        result = cache.get(key)
        if not result:
            result = query_function(*args, **kwargs)
            cache.set(key, result, timeout=300)  # Cache for 5 minutes
        return result

    def apply_lazy_loading(self, queryset):
        """
        Apply lazy loading to the queryset to defer the loading of related data until absolutely necessary.
        
        :param queryset: Django QuerySet object 
        
        :return: Lazy-loaded QuerySet
        """
        return queryset.select_related(None).defer(*[f.name for f in queryset.model._meta.get_fields()])
