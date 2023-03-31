import os
import logging
from urllib.parse import urlencode
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
import urllib.parse
import requests

logger = logging.getLogger(__name__)


def user_logout(request):
    if _use_oidc():
        query = {
            "post_logout_redirect_uri": request.build_absolute_uri(reverse("index")),
            "id_token_hint": request.session.get("oidc_id_token"),
            "client_id": os.getenv("OIDC_CLIENT_ID", ""),
        }
        query_string = urlencode(query)
        return f"{os.getenv('OIDC_END_SESSION_ENDPOINT', '')}?{query_string}"
    else:
        logout(request)
        return reverse("login")


def login_proxy(request):
    if _use_oidc():
        return redirect(
            reverse("oidc_authentication_init")
            + "?"
            + urllib.parse.urlencode(request.GET)
        )
    else:
        return redirect(reverse("login") + "?" + urllib.parse.urlencode(request.GET))


def _use_oidc() -> bool:
    if not os.getenv("OIDC_JWKS_ENDPOINT"):
        return False
    try:
        response = requests.get(os.getenv("OIDC_JWKS_ENDPOINT", ""))
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


class CustomAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(CustomAuthenticationBackend, self).create_user(claims)

        user.username = claims.get("preferred_username", "")
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()

        return user

    def update_user(self, user, claims):
        user.username = claims.get("preferred_username", "")
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()

        return user
