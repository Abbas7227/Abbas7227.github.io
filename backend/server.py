from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Football plays dictionary
FOOTBALL_PLAYS = {
    "man_beater": "Man Beater",
    "vertical_drag_short_cross": "Vertical Drag Short Cross",
    "pa_outs": "PA Outs",
    "double_drag_streaks": "Double Drag Streaks",
    "smash_concept": "Smash Concept",
    "four_verticals": "Four Verticals",
    "mesh_shallow": "Mesh Shallow",
    "drive_concept": "Drive Concept",
    "pa_boot_drag": "PA Boot Drag",
    "double_slants": "Double Slants",
    "stick_concept": "Stick Concept",
    "flood_post": "Flood Post",
    "texas_concept": "Texas Concept",
    "levels_concept": "Levels Concept",
    "corner_post": "Corner Post",
    "deep_crossers": "Deep Crossers",
    "dagger_concept": "Dagger Concept",
    "scissors": "Scissors",
    "yankee_concept": "Yankee Concept",
    "slot_cross": "Slot Cross",
    "corner_flood": "Corner Flood",
    "dagger_pivot": "Dagger Pivot",
    "deep_out_wheel": "Deep Out Wheel",
    "bunch_flood": "Bunch Flood",
    "backside_post_cross": "Backside Post Cross",
    "switch_verticals": "Switch Verticals",
    "post_wheel": "Post Wheel",
    "levels_backed_up": "Levels Backed Up",
    "flood_switch": "Flood Switch",
    "pa_deep_cross": "PA Deep Cross",
    "double_post": "Double Post",
    "curl_flat": "Curl Flat",
    "snag_concept": "Snag Concept",
    "slot_fade": "Slot Fade",
    "angle_route": "Angle Route",
    "stick_nod": "Stick Nod",
    "quick_outs": "Quick Outs",
    "china_concept": "China Concept",
    "four_verts_backed_up": "Four Verts Backed Up",
    "out_and_up": "Out and Up"
}

# Define Models
class PlayRecommendationRequest(BaseModel):
    yard_position: int = Field(..., ge=0, le=100, description="Current yard position (0-100)")
    down: str = Field(..., description="Current down (1st, 2nd, 3rd, 4th)")
    yard_gain: str = Field(..., description="Target yard gain (short, medium, long)")

class PlayRecommendationResponse(BaseModel):
    recommended_plays: List[str]
    field_situation: str
    strategy_note: str

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

def get_play_recommendations(yard: int, down: str, yard_gain: str) -> List[str]:
    """Convert the Lua logic to Python for play recommendations"""
    recommendations = []
    
    # Original pan plays
    if (yard > 40) and (down in ["1st", "2nd"]) and (yard_gain in ["medium", "long"]):
        recommendations.append("vertical_drag_short_cross")
    
    if (yard < 30 or yard > 70) and (down == "2nd") and (yard_gain == "long"):
        recommendations.append("double_drag_streaks")
    
    if (yard > 10) and (down in ["2nd", "3rd", "4th"]) and (yard_gain in ["short", "medium"]):
        recommendations.append("pa_outs")
    
    # New plays from the Lua script
    if (0 <= yard <= 40) and (down in ["1st", "2nd"]) and yard_gain == "short":
        recommendations.append("smash_concept")
    
    if (20 <= yard <= 80) and (down in ["2nd", "3rd"]) and yard_gain == "long":
        recommendations.append("four_verticals")
    
    if (20 <= yard <= 60) and (down in ["2nd", "3rd"]) and yard_gain == "short":
        recommendations.append("mesh_shallow")
    
    if (15 <= yard <= 70) and (down in ["1st", "2nd"]) and yard_gain == "medium":
        recommendations.append("drive_concept")
    
    if (10 <= yard <= 50) and down == "1st" and yard_gain == "medium":
        recommendations.append("pa_boot_drag")
    
    if (0 <= yard <= 30) and (down in ["3rd", "4th"]) and yard_gain == "short":
        recommendations.append("double_slants")
    
    if (0 <= yard <= 30) and down == "3rd" and yard_gain == "short":
        recommendations.append("stick_concept")
    
    if (30 <= yard <= 80) and down == "2nd" and yard_gain == "long":
        recommendations.append("flood_post")
    
    if (10 <= yard <= 40) and (down in ["2nd", "3rd"]) and yard_gain == "short":
        recommendations.append("texas_concept")
    
    if (20 <= yard <= 60) and (down in ["2nd", "3rd"]) and yard_gain == "short":
        recommendations.append("levels_concept")
    
    if (30 <= yard <= 70) and (down in ["3rd", "4th"]) and yard_gain == "medium":
        recommendations.append("corner_post")
    
    if (40 <= yard <= 80) and (down in ["3rd", "4th"]) and yard_gain == "long":
        recommendations.append("deep_crossers")
    
    if (25 <= yard <= 60) and (down in ["3rd", "4th"]) and yard_gain == "medium":
        recommendations.append("dagger_concept")
    
    if (30 <= yard <= 60) and down == "3rd" and yard_gain == "medium":
        recommendations.append("scissors")
    
    if (50 <= yard <= 80) and (down in ["3rd", "4th"]) and yard_gain == "long":
        recommendations.append("yankee_concept")
    
    if (20 <= yard <= 50) and down == "3rd" and yard_gain == "medium":
        recommendations.append("slot_cross")
    
    if (40 <= yard <= 70) and down == "3rd" and yard_gain == "long":
        recommendations.append("corner_flood")
    
    if (25 <= yard <= 50) and down == "3rd" and yard_gain == "medium":
        recommendations.append("dagger_pivot")
    
    if (30 <= yard <= 70) and down == "4th" and yard_gain == "long":
        recommendations.append("deep_out_wheel")
    
    if (30 <= yard <= 60) and down == "3rd" and yard_gain == "medium":
        recommendations.append("bunch_flood")
    
    if (40 <= yard <= 80) and down == "4th" and yard_gain == "long":
        recommendations.append("backside_post_cross")
    
    if (yard == 100) and (down == "3rd") and (yard_gain == "medium"):
        recommendations.append("switch_verticals")
    
    if (yard <= 10) and (down == "1st") and (yard_gain == "long"):
        recommendations.append("post_wheel")
    
    if (yard <= 10) and (down == "4th") and (yard_gain == "medium"):
        recommendations.append("levels_backed_up")
    
    if (20 <= yard <= 30) and (down == "4th") and (yard_gain == "long"):
        recommendations.append("flood_switch")
    
    if (15 <= yard <= 30) and (down == "1st") and (yard_gain == "long"):
        recommendations.append("pa_deep_cross")
    
    if (10 <= yard <= 25) and (down == "4th") and (yard_gain == "long"):
        recommendations.append("double_post")
    
    if (5 <= yard <= 15) and (down == "2nd") and (yard_gain == "medium"):
        recommendations.append("curl_flat")
    
    if (yard <= 10) and (down == "3rd") and (yard_gain == "medium"):
        recommendations.append("snag_concept")
    
    if (yard >= 85) and (down == "4th") and (yard_gain == "medium"):
        recommendations.append("slot_fade")
    
    if (yard <= 10) and (down == "2nd") and (yard_gain == "medium"):
        recommendations.append("angle_route")
    
    if (yard >= 90) and (down == "3rd") and (yard_gain == "medium"):
        recommendations.append("stick_nod")
    
    if (70 <= yard <= 80) and (down == "1st") and (yard_gain == "short"):
        recommendations.append("quick_outs")
    
    if (yard <= 5) and (down == "2nd") and (yard_gain == "medium"):
        recommendations.append("china_concept")
    
    if (yard <= 5) and (down == "1st") and (yard_gain == "long"):
        recommendations.append("four_verts_backed_up")
    
    if (yard <= 10) and (down == "4th") and (yard_gain == "medium"):
        recommendations.append("out_and_up")
    
    return recommendations

def get_field_situation(yard: int) -> str:
    """Determine field situation based on yard position"""
    if yard <= 20:
        return "Own Territory - Conservative"
    elif yard <= 50:
        return "Midfield - Balanced"
    elif yard <= 80:
        return "Red Zone Approach - Aggressive"
    else:
        return "Red Zone - Score Now"

def get_strategy_note(down: str, yard_gain: str) -> str:
    """Get strategy note based on down and yard gain"""
    if down == "1st":
        return "Establish rhythm and set up future downs"
    elif down == "2nd":
        if yard_gain == "short":
            return "High percentage play to ensure manageable 3rd down"
        elif yard_gain == "medium":
            return "Keep the chains moving"
        else:
            return "Take a shot downfield"
    elif down == "3rd":
        return "Must convert to keep the drive alive"
    else:  # 4th down
        return "All or nothing - go for it!"

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Football Play Recommendation System API"}

@api_router.post("/recommend-play", response_model=PlayRecommendationResponse)
async def recommend_play(request: PlayRecommendationRequest):
    """Get play recommendations based on field position, down, and yard gain target"""
    recommendations = get_play_recommendations(
        request.yard_position, 
        request.down, 
        request.yard_gain
    )
    
    # Convert internal play names to display names
    display_plays = [FOOTBALL_PLAYS.get(play, play) for play in recommendations]
    
    # Remove duplicates while preserving order
    unique_plays = []
    seen = set()
    for play in display_plays:
        if play not in seen:
            unique_plays.append(play)
            seen.add(play)
    
    # If no specific recommendations, provide general advice
    if not unique_plays:
        if request.yard_gain == "short":
            unique_plays = ["Quick Slant", "Checkdown Pass", "Draw Play"]
        elif request.yard_gain == "medium":
            unique_plays = ["Out Route", "Curl Route", "Screen Pass"]
        else:
            unique_plays = ["Go Route", "Post Route", "Deep Cross"]
    
    return PlayRecommendationResponse(
        recommended_plays=unique_plays,
        field_situation=get_field_situation(request.yard_position),
        strategy_note=get_strategy_note(request.down, request.yard_gain)
    )

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()