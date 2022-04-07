import os


class Config:
    ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    BASE_URL = os.environ.get('BASE_URL', 'https://54.194.204.59/')
    COLOR = os.environ.get('COLOR', '#000000')
    IMG_URL = os.environ.get('IMG_URL', None)
    SECRET = os.environ.get('SECRET', 'secret')

