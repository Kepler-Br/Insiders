from django.apps import AppConfig


class UserauthappConfig(AppConfig):
    name = 'UserAuthApp'

    def ready(self):
        import UserAuthApp.signals