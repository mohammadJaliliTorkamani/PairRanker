import json
import os

from app.db import initialize_database, replace_user_pairs


def seed_user_data(user_id: str):
    """
    Load JSONL for a specific user and overwrite their dataset.
    """

    path = f"data/users/{user_id}.jsonl"

    if not os.path.exists(path):
        raise FileNotFoundError(f"No dataset found for user {user_id}")

    pairs = []

    with open(path, "r") as f:
        for line in f:
            obj = json.loads(line)

            pairs.append({
                "user_id": user_id,
                "left": obj["ground_truth_description"],
                "right": obj["prediction"]
            })

    initialize_database()
    replace_user_pairs(user_id, pairs)

    print(f"[SEED] Loaded {len(pairs)} pairs for {user_id}")
