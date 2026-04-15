from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse

from app.core.templates import templates
from app.services.user_dataset_service import user_dataset_exists

router = APIRouter()


@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, user_id: str = Form(...)):
    if not user_dataset_exists(user_id):
        return HTMLResponse(
            content="<h3>User dataset not found. Please contact admin.</h3>",
            status_code=400
        )

    response = RedirectResponse(url="/survey", status_code=302)
    response.set_cookie(key="user_id", value=user_id)

    return response