from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    DATABASE_TEST_URL: PostgresDsn


settings = Settings()


# for migrations
TORTOISE_ORM = {
    'connections': {'default': settings.DATABASE_URL},
    'apps': {
        'models': {
            'models': ['app.events.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}
