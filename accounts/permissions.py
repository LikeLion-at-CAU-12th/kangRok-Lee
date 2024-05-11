from rest_framework import permissions
import os, json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    # secret 변수를 가져오거나 그렇지 못 하면 예외를 반환
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

class KeyHeaderPermission(permissions.BasePermission):
    """
    Custom permission to only allow ppl w/ super secret key
    """

    def has_permission(self, request, view):
        key = request.META.get('HTTP_X_SUPER_SECRET_KEY')
        if key == get_secret("ORANGE_CATS"):
            return True
        return False