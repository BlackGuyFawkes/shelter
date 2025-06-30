from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import csv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("index.html")

@app.get("/styles.css")
async def serve_styles():
    return FileResponse("styles.css")

@app.get("/script.js")
async def serve_script():
    return FileResponse("script.js")

def load_shelter_data():
    shelters = []
    with open("shelters.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Occupancy'] = int(row['Occupancy']) if row['Occupancy'].isdigit() else 0
            row['Capacity'] = int(row['Capacity']) if row['Capacity'].isdigit() else 0
            row['Available'] = row['Capacity'] - row['Occupancy']
            shelters.append(row)
    return shelters

@app.get("/shelters")
def get_shelters(sector: str = None, city: str = None):
    shelters = load_shelter_data()
    results = []
    for s in shelters:
        if sector and sector.lower() not in s['Sector'].lower():
            continue
        if city and city.lower() not in s['City'].lower():
            continue
        results.append(s)
    return {"count": len(results), "data": results}
