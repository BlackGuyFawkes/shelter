from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return FileResponse("frontend/index.html")

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