import os
from urllib.parse import urlencode
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth import logout
from django.urls import reverse

from nano_siem.settings import OIDC_CONFIGURATION, USE_OIDC


def user_logout(request):
    if USE_OIDC:
        query = {
            "post_logout_redirect_uri": request.build_absolute_uri(
                reverse("oidc_authentication_init")
            ),
            "id_token_hint": request.session.get("oidc_id_token"),
            "client_id": os.getenv("OIDC_CLIENT_ID"),
        }
        query_string = urlencode(query)
        return f"{OIDC_CONFIGURATION['end_session_endpoint']}?{query_string}"
    else:
        logout(request)
        return reverse("login")


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
