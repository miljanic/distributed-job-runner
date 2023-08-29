from os import getenv

if not getenv("ENV"):
    from dotenv import load_dotenv

    load_dotenv()

from djb_api.application import create_app  # noqa: E402
from djb_api.config import config  # noqa: E402, F401

app = create_app()
