from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import HTMLResponse

from app.core.templates import templates
from app.db import get_db
from app.services.export_service import export_user_results
from app.services.user_dataset_service import load_user_dataset

router = APIRouter()


# ---------------------------
# SURVEY PAGE
# ---------------------------
@router.get("/survey", response_class=HTMLResponse)
async def survey_page(request: Request):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return HTMLResponse("Not logged in", status_code=401)

    pairs = load_user_dataset(user_id)

    if not pairs:
        return HTMLResponse("Dataset not found for user", status_code=404)

    return templates.TemplateResponse("survey.html", {
        "request": request,
        "pairs": pairs,
        "user_id": user_id,
        "question": "How similar are these two vulnerability descriptions?"
    })


# ---------------------------
# SUBMIT ALL RESPONSES
# ---------------------------
@router.post("/submit-all")
async def submit_all(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    user_id = request.cookies.get("user_id")

    if not user_id:
        return HTMLResponse("Not logged in", status_code=401)

    db = get_db()

    responses = []

    # safer loop (avoids key-order bugs)
    pair_keys = [k for k in form.keys() if k.startswith("pair_id_")]

    for key in pair_keys:
        idx = key.split("_")[-1]

        pair_id = form.get(f"pair_id_{idx}")
        rating = form.get(f"rating_{idx}")
        reason = form.get(f"reason_{idx}")

        left = form.get(f"left_{idx}")
        right = form.get(f"right_{idx}")
        left_source = form.get(f"left_source_{idx}")
        right_source = form.get(f"right_source_{idx}")

        # reconstruct correctly
        if left_source == "ground_truth":
            ground_truth = left
            prediction = right
        else:
            ground_truth = right
            prediction = left

        responses.append({
            "user_id": user_id,
            "pair_id": pair_id,
            "rating": rating,
            "reason": reason,
            "ground_truth": ground_truth,
            "prediction": prediction
        })

    await db.responses.delete_many({"user_id": user_id})

    if responses:
        await db.responses.insert_many(responses)

    background_tasks.add_task(export_user_results, user_id)

    return {
        "status": "ok",
        "saved": len(responses)
    }
