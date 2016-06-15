from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from ..models import Item


@receiver(post_save, sender=Item)
@receiver(post_delete, sender=Item)
def update_cache_on_post_delete_or_updated(sender, instance, **kwargs):
    pass