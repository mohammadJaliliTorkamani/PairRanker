import os

from fastapi.templating import Jinja2Templates

# Always anchor to project root via environment or fallback
BASE_DIR = os.getenv("APP_DIR", "/app")

TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

print("TEMPLATE DIR LOADED:", TEMPLATE_DIR)
print("EXISTS:", os.path.exists(TEMPLATE_DIR))
