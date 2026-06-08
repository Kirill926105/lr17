from django.apps import AppConfig
from django.db.backends.signals import connection_created


def register_lower_utf8(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        connection.connection.create_function(
            "lower_utf8", 1,
            lambda s: s.lower() if isinstance(s, str) else s
        )


class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        connection_created.connect(register_lower_utf8)
