import os


class Config:
    ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    BASE_URL = os.environ.get('BASE_URL', 'https://smartconference.network/')
    COLOR = os.environ.get('COLOR', '#121565')
    IMG_URL = os.environ.get('IMG_URL', None)
    SECRET = os.environ.get('SECRET', 'secret')

