from constants import SECRET_PATH
from dotenv import load_dotenv
from os import getenv

class SecretLoader:
    isLoaded = False

    @classmethod
    def load(cls):
        if not load_dotenv(SECRET_PATH):
            raise ValueError("Secret couldn't be loaded!")

    @classmethod
    def get(cls, name):
        if not cls.isLoaded:
            cls.load()
            cls.isLoaded = True

        return getenv(name)