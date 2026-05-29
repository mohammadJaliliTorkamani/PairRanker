import random

from app.db import fetch_all_pairs, insert_response


async def fetch_pairs():
    pairs = fetch_all_pairs(limit=1000)

    # Randomize left/right order
    randomized = []
    for p in pairs:
        if random.random() > 0.5:
            left, right = p["left_text"], p["right_text"]
        else:
            left, right = p["right_text"], p["left_text"]

        randomized.append({
            "id": str(p["id"]),
            "left": left,
            "right": right
        })

    random.shuffle(randomized)
    return randomized


async def save_response(user_id, pair_id, rating, reason):
    insert_response({
        "user_id": user_id,
        "pair_id": pair_id,
        "rating": rating,
        "reason": reason
    })
