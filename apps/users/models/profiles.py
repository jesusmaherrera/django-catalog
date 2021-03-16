""" Profile model. """

# Django
from django.db import models

# Utilities
from apps.utils.models import FinanzenBaseModel


class Profile(FinanzenBaseModel):
    """Profile model.

    A profile holds a user's public data like biography, picture,
    and statics.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True,
    )
    biography = models.TextField(max_length=500, blank=True)

    # Stats

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
