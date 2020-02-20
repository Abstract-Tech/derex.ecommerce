from whitenoise import WhiteNoise

application = __import__("ecommerce.wsgi").wsgi.application

application = WhiteNoise(application, root="/openedx/staticfiles", prefix="/static")
