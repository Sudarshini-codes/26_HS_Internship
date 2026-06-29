from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import pathlib

from RuleBasedDetector import detect_anomaly

class SensorReading(BaseModel):
    timestamp: datetime = Field(default="2025-07-30T09:20:00")
    temperature_c: float = Field(default=24.3, ge=-50.0, le=100.0)
    vibration_mm_s: float = Field(default=2.41, ge=0.0)
    pressure_kpa: float = Field(default=101.28, gt=0.0)
    current_a: float = Field(default=5.92, ge=0.0)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = pathlib.Path(__file__).resolve().parent
UI_FILE = BASE_DIR / "ui.html"
INDEX_UI_FILE = BASE_DIR / "index.html"
LIVE_CHART_FILE = BASE_DIR / "live_chart.html"
COMPACT_UI_FILE = BASE_DIR / "compact.html"
SIMULATOR_UI_FILE = BASE_DIR / "simulator.html"

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(UI_FILE.read_text(encoding="utf-8"))

@app.post("/predict")
def predict_anomaly(reading: SensorReading):
    reading_dict = reading.model_dump()
    reading_dict["timestamp"] = reading.timestamp.isoformat()
    return detect_anomaly(reading_dict)

@app.get("/index", response_class=HTMLResponse)
async def root():
    return HTMLResponse(INDEX_UI_FILE.read_text(encoding="utf-8"))

@app.get("/dark_mode", response_class=HTMLResponse)
async def root():
    return HTMLResponse(COMPACT_UI_FILE.read_text(encoding="utf-8"))

@app.get("/live_chart", response_class=HTMLResponse)
async def root():
    return HTMLResponse(LIVE_CHART_FILE.read_text(encoding="utf-8"))

@app.get("/simulator", response_class=HTMLResponse)
async def root():
    return HTMLResponse(SIMULATOR_UI_FILE.read_text(encoding="utf-8"))