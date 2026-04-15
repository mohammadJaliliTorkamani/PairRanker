import json
import os
import random

DATASET_DIR = "/app/data/datasets"


def user_dataset_exists(user_id: str) -> bool:
    file_path = os.path.join(DATASET_DIR, f"{user_id}.jsonl")
    return os.path.exists(file_path)


def load_user_dataset(user_id: str):
    file_path = f"/app/data/datasets/{user_id}.jsonl"

    if not os.path.exists(file_path):
        return None

    pairs = []

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            obj = json.loads(line.strip())

            ground_truth = obj["ground_truth_description"]
            prediction = obj["prediction"]

            is_swapped = random.random() < 0.5

            if is_swapped:
                left = prediction
                right = ground_truth
                left_label = "prediction"
                right_label = "ground_truth"
            else:
                left = ground_truth
                right = prediction
                left_label = "ground_truth"
                right_label = "prediction"

            pairs.append({
                "id": str(i),
                "left": left,
                "right": right,
                "left_source": left_label,
                "right_source": right_label
            })

    random.shuffle(pairs)

    return pairs
