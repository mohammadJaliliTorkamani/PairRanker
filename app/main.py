from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import get_db
from app.routes import auth, survey

app = FastAPI(title="CASEY")

# static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# routers
app.include_router(auth.router)
app.include_router(survey.router)


# startup cleanup
@app.on_event("startup")
def startup_db_cleanup():
    db = get_db()

    db.pairs.delete_many({})
    db.responses.delete_many({})

    print("[STARTUP] Cleared pairs and responses collections")
