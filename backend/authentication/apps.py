from django.apps import AppConfig


class GraphQLAuthConfig(AppConfig):
    name = "authentication"
    verbose_name = "GraphQL Auth"

    def ready(self):
        import authentication.signals
