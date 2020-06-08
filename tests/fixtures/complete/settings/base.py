from .derex import *  # type: ignore # noqa

FEATURES["ENABLE_OAUTH2_PROVIDER"] = True  # type: ignore # noqa
OAUTH_OIDC_ISSUER = "http://complete.localhost/oauth2"

JWT_AUTH["JWT_ISSUER"] = JWT_ISSUER
JWT_AUTH["JWT_AUDIENCE"] = JWT_AUDIENCE
JWT_AUTH["JWT_SECRET_KEY"] = JWT_SECRET_KEY
