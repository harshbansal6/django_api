from django.apps import AppConfig
from django.db import models
import uuid


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        from django.contrib.auth.models import User
        # Add the auth_token field if it doesn't exist
        if not hasattr(User, 'auth_token'):
            User.add_to_class('auth_token', models.UUIDField(default=uuid.uuid4, null=True, blank=True))
