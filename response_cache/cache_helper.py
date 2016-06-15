from django.core.cache import cache
from rest_framework.response import Response
from .cache_keys import ResponseCacheKey


class CacheHelpers(object):
    """
    Cache Helper Class to check the object or list cache key. Build Cache key and set data based on the view
    setup and request params
    """

    cache_keys = [value for key, value in ResponseCacheKey.__dict__.items() if not key.startswith('__') and
                  not callable(key)]

    def _get_list_cache_key(self):
        assert self.list_cache_key is not None, (
            "'%s'include cache key of list otherwise used different class, "
            "or override the `get_list_cache_key()` method."
            % self.__class__.__name__
            )

        return self.list_cache_key

    def _get_object_cache_key(self):
        assert self.object_cache_key is not None, (
            "'%s'include cache key of object otherwise used different class, "
            "or override the `get_object_cache_key()` method."
            % self.__class__.__name__
            )

        return self.object_cache_key

    def _get_cache_key_based_on_view(self, request, **kwargs):
        """
        return cache key depending upon the list of retrieve view
        :param request coming from the api:
        :param key value arguments attached to the view:
        :return cache_key:
        """
        if kwargs.get('is_list_data'):
            query_params = ''
            if request.query_params:
                for key, value in request.query_params.iteritems():
                    query_params += "%s_%s" % (key, value)
            cache_key = self._get_list_cache_key() % (query_params or 1)
        else:
            cache_key = self._get_object_cache_key() % (kwargs['pk'])

        if self.permission_classes:
            user_id = str(request.user.pk)
            cache_key = cache_key + 'user' + user_id
        self.cache_key = cache_key
        return cache_key

    def _get_cache_data_or_none(self, request, **kwargs):
        """
        get cache data if the response is cached.
        :return cache_data and cache_key
        """
        cache_key = self.cache_key if hasattr(self, 'cache_key') else self._get_cache_key_based_on_view(request,
                                                                                                        **kwargs)
        data = cache.get(cache_key)
        if data:
            return data, cache_key
        return None, cache_key

    def _build_cache_from_data(self, cache_key, data, timeout=None):
        """
        build cache data if the response is not cached
        :param cache_key:
        :param data:
        :param timeout:
        :return:
        """
        cache.set(cache_key, data, timeout)

    def _get_cache_response_for_for_view(self, request, **kwargs):
        """
        get response cache of the view and add a new key to test that if response is cached or not
        """
        cache_data, cache_key = self._get_cache_data_or_none(request, **kwargs)
        if cache_data:
            if isinstance(cache_data, dict):
                cache_data['is_cached_data'] = True
            return Response(cache_data), cache_key
        return None, cache_key

    @classmethod
    def set_key_data_empty_on_update(cls, key):
        """
        method to remove the response cache object if related model signal is added and remove cache.
        """
        if cls.cache_keys in key:
            cache.delete_pattern(key+"*")
            return True
        return False