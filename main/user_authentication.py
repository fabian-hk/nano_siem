import os
import logging
from urllib.parse import urlencode
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
import urllib.parse
import requests
import json

from nano_siem import settings

logger = logging.getLogger(__name__)


def user_logout(request):
    if settings.USE_OIDC:
        query = {
            "post_logout_redirect_uri": request.build_absolute_uri(
                reverse("index")
            ),
            "id_token_hint": request.session.get("oidc_id_token"),
            "client_id": os.getenv("OIDC_CLIENT_ID"),
        }
        query_string = urlencode(query)
        return f"{settings.OIDC_CONFIGURATION['end_session_endpoint']}?{query_string}"
    else:
        logout(request)
        return reverse("login")


def login_proxy(request):
    try:
        response = requests.get(os.getenv("OIDC_DISCOVERY_DOCUMENT"))
        if response.status_code == 200:
            settings.OIDC_CONFIGURATION = json.loads(response.text)
            settings.OIDC_OP_AUTHORIZATION_ENDPOINT = settings.OIDC_CONFIGURATION[
                "authorization_endpoint"
            ]
            settings.OIDC_OP_TOKEN_ENDPOINT = settings.OIDC_CONFIGURATION[
                "token_endpoint"
            ]
            settings.OIDC_OP_USER_ENDPOINT = settings.OIDC_CONFIGURATION[
                "userinfo_endpoint"
            ]
            settings.OIDC_OP_JWKS_ENDPOINT = settings.OIDC_CONFIGURATION["jwks_uri"]
            settings.USE_OIDC = True
            logger.info(f"Loaded OIDC configuration from {os.getenv('OIDC_DISCOVERY_DOCUMENT')}")
        else:
            settings.USE_OIDC = False
            logger.warning(
                f"Failed to load OIDC configuration from {os.getenv('OIDC_DISCOVERY_DOCUMENT')}. Status code: {response.status_code}"
            )
    except Exception as e:
        settings.USE_OIDC = False
        logger.warning(
            f"Failed to load OIDC configuration from {os.getenv('OIDC_DISCOVERY_DOCUMENT')}"
        )

    if settings.USE_OIDC:
        return redirect(
            reverse("oidc_authentication_init")
            + "?"
            + urllib.parse.urlencode(request.GET)
        )
    else:
        return redirect(reverse("login") + "?" + urllib.parse.urlencode(request.GET))


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
