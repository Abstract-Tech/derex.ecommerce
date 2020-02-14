from .derex import *

# HTTPS = "off"
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
FEATURES['ENABLE_OAUTH2_PROVIDER'] = True
OAUTH_OIDC_ISSUER = 'http://localhost:4700/oauth2'
