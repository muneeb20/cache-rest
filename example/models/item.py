from django.db import models


class Item(models.Model):
    """
    Example model to demonstrate the cache response rest framework. It contains only name field
    """
    name = models.CharField(max_length=30, help_text="Specify the Item Name")

    def __unicode__(self):
        return self.name
