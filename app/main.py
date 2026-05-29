from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import clear_survey_tables, initialize_database
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
    initialize_database()
    clear_survey_tables()

    print("[STARTUP] Cleared pairs and responses tables")
