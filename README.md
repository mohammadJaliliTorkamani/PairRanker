# PairRank — Human Evaluation Platform for Text Similarity

PairRank is a lightweight, Dockerized web application built with FastAPI for conducting human evaluation studies on text similarity. It enables users to compare pairs of descriptions and rate their similarity while providing reasoning.

This project is designed for both research experiments and backend engineering portfolios, emphasizing clean architecture, reproducibility, and modular design.

---

## 🚀 Features

- 🔐 User-specific datasets (JSONL-based)
- 🎲 Randomized pair order and left/right swapping
- 🧠 Human similarity annotation (3-level rating)
- ✍️ Free-text reasoning collection
- 💾 MongoDB storage for responses
- 📤 Automatic export to JSON files
- 🐳 Fully Dockerized (one-command startup)
- 🎯 Minimal and clean UI for user studies

---

## 🧱 Tech Stack

- Backend: FastAPI
- Database: MongoDB (Motor async client)
- Frontend: Jinja2 templates + HTML/CSS
- Containerization: Docker + Docker Compose

---

## 📥 Dataset Format

Each user must have a corresponding JSONL file:

data/datasets/{user_id}.jsonl

Each line:

{
  "ground_truth_description": "Description A...",
  "prediction": "Description B..."
}

---

## ▶️ Running the Project

1. Make the ru file executable:

        sudo chmod +x run.sh

2. Run:

        ./run.sh

---

## 🧪 Survey Workflow

1. User logs in with ID
2. Dataset loads dynamically
3. Pairs are randomized and swapped
4. User selects similarity level
5. User provides reasoning
6. All responses submitted together

---

## 💾 Output

Results are:

- Stored in MongoDB
- Exported as JSON:

data/results/results_{user_id}.json

Example:

[
  {
    "user_id": "user123",
    "pair_id": "3",
    "rating": "highly",
    "reason": "...",
    "ground_truth": "...",
    "prediction": "..."
  }
]

---

## 🔁 Data Handling

- Dataset loaded from JSONL files
- Responses overwrite previous submissions per user
- Export file is regenerated on each submission

---

## 📈 Future Improvements

- Resume incomplete surveys
- Response time tracking
- Analytics dashboard
- Inter-annotator agreement metrics

---

## 📜 License

MIT License
