import os

# App config
APP_TITLE_NAME = "Magani"
SUB_TITLE_NAME = "API Testing tool"

# Web Config
MAGANI_HOST = os.environ["MAGANI_HOST"] if "MAGANI_HOST" in os.environ else "localhost"
MAGANI_PORT = os.environ["MAGANI_PORT"] if "MAGANI_PORT" in os.environ else 8000
