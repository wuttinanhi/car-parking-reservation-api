"""
    env module
"""


def load_env():
    import os

    from dotenv import load_dotenv
    if os.getenv("env") == "production":
        load_dotenv(dotenv_path=".env")
    else:
        load_dotenv(dotenv_path="dev.env")
