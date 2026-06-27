from django.apps import AppConfig


class {{ cookiecutter.app_name|capitalize }}Config(AppConfig):
    name = "{{ cookiecutter.app_name }}"
    # Distinct label so a service named after a Django builtin (e.g. "auth")
    # doesn't collide with django.contrib.* app labels.
    label = "{{ cookiecutter.app_name }}_app"
