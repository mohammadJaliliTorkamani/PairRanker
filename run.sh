#!/bin/bash

docker-compose up --build -d

sleep 5

echo "Opening CASEY in browser..."
python3 -m webbrowser http://localhost:8000