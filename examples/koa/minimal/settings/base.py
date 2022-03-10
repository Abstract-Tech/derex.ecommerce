from derex_django.settings.default import *

import json


FEATURES["ENABLE_OAUTH2_PROVIDER"] = True

OAUTH_OIDC_ISSUER = "http://ecommerce-koa-minimal.localhost/oauth2"

ECOMMERCE_API_SIGNING_KEY = "lms-secret"
ECOMMERCE_API_URL = "http://ecommerce.ecommerce-koa-minimal.localhost/api/v2"
ECOMMERCE_PUBLIC_URL_ROOT = "http://ecommerce.ecommerce-koa-minimal.localhost"

EDX_API_KEY = "lms-secret"

DEFAULT_JWT_ISSUER = {
    "ISSUER": OAUTH_OIDC_ISSUER,
    "AUDIENCE": "lms-key",
    "SECRET_KEY": "lms-secret",
}

JWT_AUTH.update(
    {
        "JWT_SECRET_KEY": "lms-secret",
        "JWT_AUDIENCE": "lms-key",
        "JWT_ISSUER": OAUTH_OIDC_ISSUER,
        # These settings are NOT part of DRF-JWT's defaults.
        "JWT_ISSUERS": [
            {
                "AUDIENCE": "lms-key",
                "ISSUER": OAUTH_OIDC_ISSUER,
                "SECRET_KEY": "lms-secret",
            },
            {
                "AUDIENCE": "lms-key",
                "ISSUER": "ecommerce_worker",
                "SECRET_KEY": "lms-secret",
            },
        ],
    }
)

ENTERPRISE_API_URL = "{}/enterprise/api/v1".format(LMS_ROOT_URL)
JWT_PRIVATE_SIGNING_KEY = json.dumps(
    {
        "kty": "RSA",
        "kid": "L9IHZW6G",
        "e": "AQAB",
        "n": "uId8gxb1JqiwS2jYDo6jKAolZzniNr2lviBga-pDyZuBOsVkqL1kreDKKo4C4MFF11XAeFfjEkRlYayrGfHh3GWIyeVA3zr5c1PL0RlxwgmPCRo8XRD5r2hofcRYUzQkjKAVYcs-etLB3_e0Lj0HH0z1RDEKA7dZ6wvJc1UtsUJwLp3IuKRv3I9WXbM3C6RTQgGpfII7tAPsnqnn6TYLvXcvScXpA56IZC6THO5__SuW9JtKMvhX8nuM-U5sBgQi-JFhR1aHoOzmrgMCkw4VvPZC2yPDapqwxl74nUSDN5TokxSheGGtrh6LRUtBWeb4sDE8Xpp_2F7cV-DwYORiKw",
        "d": "TUhVIfPh_Wxl1VdWMZaUh4bkTlzEPKflvACEUX3-IPgTQgF83Fzhxx7fnL34P5hCf2KHJv-r9rEVgrhVupp-vRb7GI9-wV9KLP5Z3Lua1Ki7MpU91b5vzAJezNmIImSysAC1o80C4F7XWs07tafSjU3mZMZjCtZl_tZjav2wEs3n79rzM8ihmOpLiSOoecvVu6j3ihWdd-k2VNQjSdW9-Mq8ZKgO-BpHNmor9ce2MUTTMKe4U27hTaaPPCyx_uL1ezA82RC2PCuGQt3WJ-BVmtFqdn4JZ96YcTDPWMe_vvVs6Zuwj6wsAgbtRaklhPivuiLGlRdaBGYaXJfxfUTvSQ",
        "p": "u3cpGjFFD5nNqx1vAE0maz8_pgfYfUTLmznuiXtmVU4d2NPQueEPlD-TCQN7NfAzWk6uFeDSh8PONHJulkFd74xzJltS4nGRjsjoMyX-ptN5_lP1howBFZwe_x2s8nax18v6z2L1RvjruFTmMh5AXvmOFZOMgUbmjosva35FKzk",
        "q": "-_2GcItzMS7NePv95IOSJ5s0Qb2BMwoAuQPSMgKGF7M_MVYIQHVMtz3BBB52QpgPwBoDv2bzDdU0mwQgOyMDt94Ya06aiHH8WXtFgjKD9FAwN9zsO3ZIiKhmA5WomcxyMVB2N0lVs9gTut_09TW57bfAeSfUdd7ztwh7DJqFZIM",
    }
)
