"""Django model utilities."""

# django
from django.db import models


class FinanzenBaseModel(models.Model):
    """Finanzen base model.

    FinanzenBaseModel acts as an abstract base class from witchnevery
    other model in the project will inherit. This class provides
    every table with de following attribute:
        + created (DateTime): Store the datetime the object was created
        + modified (DateTime): Store the last datetime the object was modified
    """

    created = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text="Date time on with the object was created."
    )
    modified = models.DateTimeField(
        'modified_at',
        auto_now=True,
        help_text="Date time on with the object was last modified."
    )

    class Meta(object):
        """docstring for Meta"""
        abstract = True

        get_latest_by = 'created'
        ordering = ('-created', '-modified')