from derex_ecommerce_django.settings.default import *


EDX_DRF_EXTENSIONS["OAUTH2_USER_INFO_URL"] = "{}/user_info".format(
    SOCIAL_AUTH_EDX_OAUTH2_ISSUER
)

LMS_JWT_ISSUER = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
CMS_JWT_ISSUER = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
ECOMMERCE_JWT_ISSUER = SOCIAL_AUTH_EDX_OAUTH2_ISSUER

EDX_API_KEY = "lms-secret"

# JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
#     {
#         "kty": "RSA",
#         "kid": "L9IHZW6G",
#         "e": "AQAB",
#         "n": "uId8gxb1JqiwS2jYDo6jKAolZzniNr2lviBga-pDyZuBOsVkqL1kreDKKo4C4MFF11XAeFfjEkRlYayrGfHh3GWIyeVA3zr5c1PL0RlxwgmPCRo8XRD5r2hofcRYUzQkjKAVYcs-etLB3_e0Lj0HH0z1RDEKA7dZ6wvJc1UtsUJwLp3IuKRv3I9WXbM3C6RTQgGpfII7tAPsnqnn6TYLvXcvScXpA56IZC6THO5__SuW9JtKMvhX8nuM-U5sBgQi-JFhR1aHoOzmrgMCkw4VvPZC2yPDapqwxl74nUSDN5TokxSheGGtrh6LRUtBWeb4sDE8Xpp_2F7cV-DwYORiKw",
#         "d": "TUhVIfPh_Wxl1VdWMZaUh4bkTlzEPKflvACEUX3-IPgTQgF83Fzhxx7fnL34P5hCf2KHJv-r9rEVgrhVupp-vRb7GI9-wV9KLP5Z3Lua1Ki7MpU91b5vzAJezNmIImSysAC1o80C4F7XWs07tafSjU3mZMZjCtZl_tZjav2wEs3n79rzM8ihmOpLiSOoecvVu6j3ihWdd-k2VNQjSdW9-Mq8ZKgO-BpHNmor9ce2MUTTMKe4U27hTaaPPCyx_uL1ezA82RC2PCuGQt3WJ-BVmtFqdn4JZ96YcTDPWMe_vvVs6Zuwj6wsAgbtRaklhPivuiLGlRdaBGYaXJfxfUTvSQ",
#         "p": "u3cpGjFFD5nNqx1vAE0maz8_pgfYfUTLmznuiXtmVU4d2NPQueEPlD-TCQN7NfAzWk6uFeDSh8PONHJulkFd74xzJltS4nGRjsjoMyX-ptN5_lP1howBFZwe_x2s8nax18v6z2L1RvjruFTmMh5AXvmOFZOMgUbmjosva35FKzk",
#         "q": "-_2GcItzMS7NePv95IOSJ5s0Qb2BMwoAuQPSMgKGF7M_MVYIQHVMtz3BBB52QpgPwBoDv2bzDdU0mwQgOyMDt94Ya06aiHH8WXtFgjKD9FAwN9zsO3ZIiKhmA5WomcxyMVB2N0lVs9gTut_09TW57bfAeSfUdd7ztwh7DJqFZIM",
#     }
# )

JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "e": "AQAB",
                "kid": "L9IHZW6G",
                "kty": "RSA",
                "n": "uId8gxb1JqiwS2jYDo6jKAolZzniNr2lviBga-pDyZuBOsVkqL1kreDKKo4C4MFF11XAeFfjEkRlYayrGfHh3GWIyeVA3zr5c1PL0RlxwgmPCRo8XRD5r2hofcRYUzQkjKAVYcs-etLB3_e0Lj0HH0z1RDEKA7dZ6wvJc1UtsUJwLp3IuKRv3I9WXbM3C6RTQgGpfII7tAPsnqnn6TYLvXcvScXpA56IZC6THO5__SuW9JtKMvhX8nuM-U5sBgQi-JFhR1aHoOzmrgMCkw4VvPZC2yPDapqwxl74nUSDN5TokxSheGGtrh6LRUtBWeb4sDE8Xpp_2F7cV-DwYORiKw",
            }
        ]
    }
)
JWT_PUBLIC_SIGNING_JWK_SET = json.dumps(
    {
        "keys": [
            {
                "e": "AQAB",
                "kid": "L9IHZW6G",
                "kty": "RSA",
                "n": "uId8gxb1JqiwS2jYDo6jKAolZzniNr2lviBga-pDyZuBOsVkqL1kreDKKo4C4MFF11XAeFfjEkRlYayrGfHh3GWIyeVA3zr5c1PL0RlxwgmPCRo8XRD5r2hofcRYUzQkjKAVYcs-etLB3_e0Lj0HH0z1RDEKA7dZ6wvJc1UtsUJwLp3IuKRv3I9WXbM3C6RTQgGpfII7tAPsnqnn6TYLvXcvScXpA56IZC6THO5__SuW9JtKMvhX8nuM-U5sBgQi-JFhR1aHoOzmrgMCkw4VvPZC2yPDapqwxl74nUSDN5TokxSheGGtrh6LRUtBWeb4sDE8Xpp_2F7cV-DwYORiKw",
            }
        ]
    }
)

JWT_AUTH.update(
    {
        "JWT_AUDIENCE": "lms-key",  # Warning: Without this the LMS will reply with a 401 "Invalid token"
        "JWT_SECRET_KEY": "lms-secret",
        # These settings are NOT part of DRF-JWT's defaults.
        "JWT_ISSUERS": [
            {
                "AUDIENCE": "lms-key",
                "ISSUER": SOCIAL_AUTH_EDX_OAUTH2_ISSUER,
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

PAYMENT_PROCESSOR_CONFIG = {
    "edx": {
        "paypal": {
            "cancel_checkout_path": "/checkout/cancel-checkout/",
            "client_id": "client_id",
            "client_secret": "client_secret",
            "error_path": "/checkout/error/",
            "mode": "sandbox",
            "receipt_path": "/checkout/receipt/",
        },
        "stripe": {
            "apple_pay_merchant_id_domain_association": "",
            "country": "DE",
            "publishable_key": "publishable_key",
            "secret_key": "publishable_secret",
        },
    },
}

ENTERPRISE_API_URL = "{}/enterprise/api/v1".format(SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT)
BACKEND_SERVICE_EDX_OAUTH2_KEY = "lms-key"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "lms-secret"
