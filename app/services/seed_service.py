import json
import os
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017")
db = client.pairranker_db


def seed_user_data(user_id: str):
    """
    Load JSONL for a specific user and overwrite their dataset.
    """

    path = f"data/users/{user_id}.jsonl"

    if not os.path.exists(path):
        raise FileNotFoundError(f"No dataset found for user {user_id}")

    # Clear old dataset for user
    db.pairs.delete_many({"user_id": user_id})

    pairs = []

    with open(path, "r") as f:
        for line in f:
            obj = json.loads(line)

            pairs.append({
                "user_id": user_id,
                "left": obj["ground_truth_description"],
                "right": obj["prediction"]
            })

    if pairs:
        db.pairs.insert_many(pairs)

    print(f"[SEED] Loaded {len(pairs)} pairs for {user_id}")