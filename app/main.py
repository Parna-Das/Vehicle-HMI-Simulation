from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
import time

app = FastAPI(
    title="Automotive Mock API",
    description="Backend API for Automotive HMI and Test Automation Suite",
    version="1.0.0"
)

# Enable CORS for frontend HMI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/hmi", StaticFiles(directory="app/static", html=True), name="hmi")

# --- In-Memory State Store ---
vehicle_state = {
    "telemetry": {
        "speed": 65.0,
        "rpm": 2200,
        "gear": "D",
        "fuel_level": 78.5,
        "battery_level": 95.0,
        "tire_pressure": {
            "fl": 32.0,
            "fr": 32.0,
            "rl": 31.5,
            "rr": 31.5
        },
        "headlights": True,
        "doors_locked": True,
        "timestamp": time.time()
    },
    "climate": {
        "driver_temp": 21.5,
        "passenger_temp": 22.0,
        "fan_speed": 3,
        "ac_enabled": True,
        "heater_enabled": False,
        "front_defrost": False,
        "rear_defrost": True,
        "seat_heater_driver": 1,
        "seat_heater_passenger": 0
    },
    "navigation": {
        "destination": "Silicon Valley Tech Hub, CA",
        "eta": "24 mins",
        "distance_remaining": "14.2 miles",
        "current_lat": 37.3861,
        "current_lng": -122.0839,
        "next_instruction": "Merge onto US-101 N in 500 feet",
        "is_active": True
    },
    "media": {
        "track_title": "Electric Sunrise",
        "artist": "Aether Sound",
        "album": "Future Highways",
        "duration": 245,
        "progress": 72,
        "is_playing": True,
        "volume": 45,
        "source": "Spotify"
    }
}

# --- Pydantic Models & Validation ---

class TirePressure(BaseModel):
    fl: float = Field(..., ge=15.0, le=50.0)
    fr: float = Field(..., ge=15.0, le=50.0)
    rl: float = Field(..., ge=15.0, le=50.0)
    rr: float = Field(..., ge=15.0, le=50.0)

class TelemetryData(BaseModel):
    speed: float = Field(..., ge=0.0, le=240.0)
    rpm: int = Field(..., ge=0, le=8000)
    gear: str = Field(...)
    fuel_level: float = Field(..., ge=0.0, le=100.0)
    battery_level: float = Field(..., ge=0.0, le=100.0)
    tire_pressure: TirePressure
    headlights: bool
    doors_locked: bool
    timestamp: float

    @field_validator("gear")
    @classmethod
    def case_validator(cls, v: str) -> str:
        valid_gears = {"P", "R", "N", "D", "S"}
        if v.upper() not in valid_gears:
            raise ValueError(f"Invalid gear. Must be one of {valid_gears}")
        return v.upper()


class ClimateSettings(BaseModel):
    driver_temp: float = Field(..., ge=16.0, le=30.0)
    passenger_temp: float = Field(..., ge=16.0, le=30.0)
    fan_speed: int = Field(..., ge=0, le=7)
    ac_enabled: bool
    heater_enabled: bool
    front_defrost: bool
    rear_defrost: bool
    seat_heater_driver: int = Field(..., ge=0, le=3)
    seat_heater_passenger: int = Field(..., ge=0, le=3)


class NavigationRequest(BaseModel):
    destination: str = Field(..., min_length=1, max_length=200)
    search_query: Optional[str] = None


class NavigationResponse(BaseModel):
    destination: str
    eta: str
    distance_remaining: str
    current_lat: float
    current_lng: float
    next_instruction: str
    is_active: bool


class MediaState(BaseModel):
    track_title: str
    artist: str
    album: str
    duration: int = Field(..., ge=0)
    progress: int = Field(..., ge=0)
    is_playing: bool
    volume: int = Field(..., ge=0, le=100)
    source: str


class MediaControl(BaseModel):
    action: str = Field(..., description="play, pause, next, prev, toggle")
    volume: Optional[int] = Field(None, ge=0, le=100)
    source: Optional[str] = None
    seek_progress: Optional[int] = Field(None, ge=0)

    @field_validator("action")
    @classmethod
    def action_validator(cls, v: str) -> str:
        valid_actions = {"play", "pause", "next", "prev", "toggle", "stop"}
        if v.lower() not in valid_actions:
            raise ValueError(f"Invalid media action. Must be one of {valid_actions}")
        return v.lower()


# --- Endpoints ---

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Automotive Mock API",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/telemetry",
            "/api/v1/climate",
            "/api/v1/navigation",
            "/api/v1/media"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Telemetry Endpoints
@app.get("/api/v1/telemetry", response_model=TelemetryData)
def get_telemetry():
    vehicle_state["telemetry"]["timestamp"] = time.time()
    return vehicle_state["telemetry"]

@app.put("/api/v1/telemetry", response_model=TelemetryData)
def update_telemetry(data: TelemetryData):
    vehicle_state["telemetry"] = data.model_dump()
    return vehicle_state["telemetry"]


# Climate Endpoints
@app.get("/api/v1/climate", response_model=ClimateSettings)
def get_climate():
    return vehicle_state["climate"]

@app.post("/api/v1/climate", response_model=ClimateSettings)
@app.put("/api/v1/climate", response_model=ClimateSettings)
def update_climate(settings: ClimateSettings):
    vehicle_state["climate"] = settings.model_dump()
    return vehicle_state["climate"]


# Navigation Endpoints
@app.get("/api/v1/navigation", response_model=NavigationResponse)
def get_navigation():
    return vehicle_state["navigation"]

@app.post("/api/v1/navigation", response_model=NavigationResponse)
def set_navigation(nav_req: NavigationRequest):
    vehicle_state["navigation"]["destination"] = nav_req.destination
    vehicle_state["navigation"]["eta"] = "18 mins"
    vehicle_state["navigation"]["distance_remaining"] = "9.5 miles"
    vehicle_state["navigation"]["next_instruction"] = f"Proceed to {nav_req.destination}"
    vehicle_state["navigation"]["is_active"] = True
    return vehicle_state["navigation"]

@app.delete("/api/v1/navigation")
def cancel_navigation():
    vehicle_state["navigation"]["is_active"] = False
    vehicle_state["navigation"]["destination"] = "None"
    vehicle_state["navigation"]["eta"] = "0 mins"
    vehicle_state["navigation"]["distance_remaining"] = "0 miles"
    vehicle_state["navigation"]["next_instruction"] = "Navigation ended"
    return {"status": "success", "message": "Navigation cancelled"}


# Media Endpoints
@app.get("/api/v1/media", response_model=MediaState)
def get_media():
    return vehicle_state["media"]

@app.post("/api/v1/media", response_model=MediaState)
def control_media(control: MediaControl):
    media = vehicle_state["media"]

    if control.volume is not None:
        media["volume"] = control.volume

    if control.source is not None:
        media["source"] = control.source

    if control.seek_progress is not None:
        media["seek_progress"] = min(control.seek_progress, media["duration"])
        media["progress"] = media["seek_progress"]

    action = control.action
    if action == "play":
        media["is_playing"] = True
    elif action == "pause":
        media["is_playing"] = False
    elif action == "toggle":
        media["is_playing"] = not media["is_playing"]
    elif action == "next":
        media["track_title"] = "Neon Highway"
        media["artist"] = "Synthwave Allstars"
        media["album"] = "Night Drive Vol. 1"
        media["progress"] = 0
        media["is_playing"] = True
    elif action == "prev":
        media["track_title"] = "Echoes of Tomorrow"
        media["artist"] = "Quantum Pulse"
        media["album"] = "Singularity"
        media["progress"] = 0
        media["is_playing"] = True

    vehicle_state["media"] = media
    return media
