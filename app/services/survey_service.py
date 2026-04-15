import random
from app.db import get_db

async def fetch_pairs():
    db = get_db()
    pairs = await db.pairs.find().to_list(1000)

    # Randomize left/right order
    randomized = []
    for p in pairs:
        if random.random() > 0.5:
            left, right = p["left"], p["right"]
        else:
            left, right = p["right"], p["left"]

        randomized.append({
            "id": str(p["_id"]),
            "left": left,
            "right": right
        })

    random.shuffle(randomized)
    return randomized


async def save_response(user_id, pair_id, rating, reason):
    db = get_db()
    await db.responses.insert_one({
        "user_id": user_id,
        "pair_id": pair_id,
        "rating": rating,
        "reason": reason
    })