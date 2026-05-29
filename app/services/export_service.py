import json
import os
from datetime import datetime

from app.db import fetch_user_responses


def export_user_results(user_id: str):
    responses = fetch_user_responses(user_id, limit=10000)

    output = []
    output.append({
        "timestamp": datetime.utcnow().isoformat()
    })

    for r in responses:
        output.append({
            "user_id": r["user_id"],
            "pair_id": r["pair_id"],
            "rating": r["rating"],
            "reason": r["reason"],
            "ground_truth": r.get("ground_truth"),
            "prediction": r.get("prediction")
        })

    base_dir = os.path.abspath("/app/data/results")
    os.makedirs(base_dir, exist_ok=True)

    file_path = os.path.join(base_dir, f"results_{user_id}.json")

    with open(file_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[EXPORT] Saved results at: {file_path}")
    return file_path
