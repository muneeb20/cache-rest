from response_cache import ResponseCacheViewSet, ResponseCacheKey
from ..models import Item


class ItemViewSet(ResponseCacheViewSet):
    """ Simple View/Api to demonstrate the concept oh how to use the cache key. It should only provide 2 class based
    variables to setup a response cache on top of django database
    """
    object_cache_key = ResponseCacheKey.SPECIFIC_ITEM_RESPONSE + '%s'
    list_cache_key = ResponseCacheKey.ALL_ITEMS_RESPONSE + '%s'
    queryset = Item.objects.all()
