import os

class Config(object):
    DEBUG = True
    TESTING = False
    EMAIL_PASS = 'amkx fedi ilnm qahn'
    CLIENT_ID = '92320207172-8cnk4c9unfaa7llua906p6kjvhnvkbqd.apps.googleusercontent.com'
    CLIENT_SECRET = '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'
    SECRET_KEY = os.getenv('SECRET_KEY', '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')
    GOOGLE_CLIENT_ID = os.getenv(
        'GOOGLE_CLIENT_ID',
        '92320207172-8cnk4c9unfaa7llua906p6kjvhnvkbqd.apps.googleusercontent.com'
    )
    GOOGLE_CLIENT_SECRET = os.getenv(
        'GOOGLE_CLIENT_SECRET',
        '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'
    )
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_REDIRECT_URI = "http://127.0.0.1:5000/login"
    MONGO_URI = "mongodb+srv://devangsaraogi:0TiCCbFRYLXVg2GU@cluster-1.enu2q.mongodb.net/slashdb"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
