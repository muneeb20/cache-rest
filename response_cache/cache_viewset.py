from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .cache_helper import CacheHelpers


class ResponseCacheRetrieveModeViewSet(GenericViewSet, RetrieveModelMixin, CacheHelpers):
    """ Set or Get the retrieve object cache. Inherit from this class if your object views need to be cached.
    """

    def retrieve(self, request, *args, **kwargs):
        cache_response, cache_key = self._get_cache_response_for_for_view(request, **kwargs)
        return cache_response or self._build_cache_for_single_obj(request, *args, **kwargs)

    def _build_cache_for_single_obj(self, request, *args, **kwargs):
        cache_key = self.cache_key
        response = super(GenericViewSet, self).retrieve(request, *args, **kwargs)
        self._build_cache_from_data(cache_key, response.data)
        return response


class ResponseCacheListModeViewSet(GenericViewSet, ListModelMixin, CacheHelpers):
    """ Set or Get the list cache. Inherit from this class if your list views need to be cached.
    """

    def list(self, request, *args, **kwargs):
        kwargs['is_list_data'] = True
        cached_response, cache_key = self._get_cache_response_for_for_view(request, **kwargs)
        return cached_response or self._build_cache_for_list(request, *args, **kwargs)

    def _build_cache_for_list(self, request, *args, **kwargs):
        cache_key = self.cache_key
        response = super(GenericViewSet, self).list(request, *args, **kwargs)
        self._build_cache_from_data(cache_key, response.data)
        return response


class ResponseCacheViewSet(ResponseCacheRetrieveModeViewSet, ResponseCacheListModeViewSet):
    """ Set or Get the list or object cache. Inherit from this class if your list views or object
    need to be cached.
    """
    pass
