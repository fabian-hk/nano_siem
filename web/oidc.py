import os
from urllib.parse import urlencode
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth import logout
from django.urls import reverse


def user_logout(request):
    if os.getenv("OIDC_ENABLED") == "True":
        query = {
            "post_logout_redirect_uri": request.build_absolute_uri(
                reverse("oidc_authentication_init")
            ),
            "id_token_hint": request.session.get("oidc_id_token"),
            "client_id": os.getenv("OIDC_CLIENT_ID"),
        }
        query_string = urlencode(query)
        return f"{os.getenv('OIDC_LOGOUT_ENDPOINT')}?{query_string}"
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
