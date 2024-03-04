import os


@staticmethod
def is_dev():
    return os.getenv("ENVIRONMENT", "").lower() == "dev"
