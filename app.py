"""
SpyEngine API Server

A minimal FastAPI server that exposes the SpyEngine backend functionality to the frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import Dict, List, Optional, Any, Tuple
import json
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="SpyEngine API", description="API for SpyEngine frontend integration")

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Define story options directly (copied from story_maker.py) ---
STORY_OPTIONS = {
    "conflicts": [
        ("💼", "Corporate espionage"),
        ("🤵", "Double agent exposed"),
        ("🧪", "Bioweapon heist"),
        ("💰", "Trillion-dollar ransom"),
        ("🔍", "Hidden conspiracy"),
        ("🕵️", "Government overthrow"),
        ("🌌", "Space station takeover"),
        ("🧠", "Mind control experiment"),
    ],
    "settings": [
        ("🗼", "Modern Europe"),
        ("🏙️", "Neo-noir Cyber Metropolis"),
        ("🌌", "Space Station"),
        ("🏝️", "Chain of Private Islands"),
        ("🏙️", "New York City"),
        ("🚢", "Luxury Cruise Liner"),
        ("❄️", "Arctic Research Base"),
        ("🏰", "Moscow Underworld"),
        ("🏜️", "1920s Europe"),
        ("🌋", "Volcanic Lair"),
    ],
    "narrative_styles": [
        ("🤪", "Modern irreverence (e.g., Christopher Moore)"),
        ("🤪", "Metafictional absurdity (e.g., Jasper Fforde)"),
        ("🤪", "Contemporary satire (e.g., Gary Shteyngart)"),
        ("🤪", "Historical playfulness (e.g., Tom Holt)"),
        ("🤪", "Darkly absurd (e.g., David Wong)"),
        ("🤪", "Quirky offbeat humor (e.g., Simon Rich)"),
        ("🤪", "Absurdist Comedy (e.g., Douglas Adams, Terry Pratchett)"),
        ("😎", "Spy Thriller (e.g., John le Carré, Ian Fleming)"),
        ("🔥", "Steamy Romance (e.g., Nora Roberts, E.L. James)"),
        ("🎭", "Surreal Narrative (e.g., Haruki Murakami, Franz Kafka)"),
        ("🎬", "Action Adventure (e.g., Tom Clancy, Robert Ludlum)"),
        ("🕵️", "Noir Detective (e.g., Dennis Lehane, Michael Connelly)"),
        ("🏙️", "Urban Grit (e.g., S. A. Cosby, Colson Whitehead)"),
        ("👽", "Dystopian Sci-Fi (e.g., George Orwell, Aldous Huxley)"),
        ("⚔️", "Epic Fantasy (e.g., J.R.R. Tolkien, George R.R. Martin)"),
        ("🎻", "Literary Drama (e.g., Fyodor Dostoevsky, Virginia Woolf)"),
        ("🧙", "Magical Adventure (e.g., J.K. Rowling, C.S. Lewis)"),
        ("🪐", "Cosmic Horror (e.g., H.P. Lovecraft, Clive Barker)"),
        ("🗺️", "Mythic Quest (e.g., Robert Jordan, Guy Gavriel Kay)"),
    ],
    "moods": [
        ("😜", "Witty and irreverent with offbeat humor"),
        ("🤯", "Mind-bending and playful with layered meta humor"),
        ("😏", "Sharp, satirical, and cutting with modern wit"),
        ("🏰", "Lighthearted and whimsical with a nod to history"),
        ("😈", "Gritty, dark, and absurdly humorous"),
        ("🤡", "Eccentric, quirky, and delightfully offbeat"),
        ("🤣", "Wildly imaginative and hilariously absurd"),
        ("🕶️", "Tense, secretive, and cool"),
        ("💋", "Passionate, sensual, and emotionally charged"),
        ("🌌", "Dreamlike, enigmatic, and surreal"),
        ("💥", "High-octane, thrilling, and adventurous"),
        ("🕵️", "Mysterious, brooding, and gritty"),
        ("🏙️", "Raw, edgy, and distinctly urban"),
        ("🤖", "Bleak, dystopic, and thought-provoking"),
        ("🐉", "Grand, epic, and full of adventure"),
        ("📖", "Deep, introspective, and emotionally profound"),
        ("✨", "Enchanting, whimsical, and full of wonder"),
        ("👻", "Eerily unsettling and cosmic in scale"),
        ("🗺️", "Legendary, epic, and mythic")
    ],
}

# --- Define currency constants directly (copied from constants.py) ---
DEFAULT_CURRENCY_BALANCES = {
    "💎": 500,   # Diamonds
    "💷": 5000,  # Pounds
    "💶": 5000,  # Euros
    "💴": 5000,  # Yen
    "💵": 5000,  # Dollars
}

CURRENCY_TYPES = {
    "💎": "Diamond",
    "💷": "Pound",
    "💶": "Euro",
    "💴": "Yen",
    "💵": "Dollar"
}

# --- Pydantic models ---
class StoryOptions(BaseModel):
    conflicts: List[Tuple[str, str]]
    settings: List[Tuple[str, str]]
    narrative_styles: List[Tuple[str, str]]
    moods: List[Tuple[str, str]]

class StoryRequest(BaseModel):
    protagonist_name: str
    protagonist_gender: str
    conflict: str
    setting: str
    narrative_style: str
    mood: str
    custom_conflict: Optional[str] = None
    custom_setting: Optional[str] = None
    custom_narrative: Optional[str] = None
    custom_mood: Optional[str] = None
    
class ChoiceRequest(BaseModel):
    choice_id: str
    custom_choice_text: Optional[str] = None

class Character(BaseModel):
    name: str
    role: str
    traits: List[str]
    backstory: str
    plot_lines: List[str]

# --- Mock data for characters (this would come from a database in production) ---
MOCK_CHARACTERS = [
    {
        "name": "Viktor Dragunov",
        "role": "villain",
        "traits": ["ruthless", "paranoid", "mastermind"],
        "backstory": "Former KGB, now controls a global tech cartel.",
        "plot_lines": ["Sabotage the protagonist's mission", "Seize control of AI weapons"]
    },
    {
        "name": "Evelyn Fox",
        "role": "mission-giver",
        "traits": ["calculating", "exasperated", "well-connected"],
        "backstory": "Disgraced MI6 handler, desperate for redemption.",
        "plot_lines": ["Recruit protagonist for impossible jobs", "Keep her own secrets hidden"]
    },
    {
        "name": "Maximilian Zhou",
        "role": "neutral",
        "traits": ["suave", "resourceful", "charming"],
        "backstory": "Nightclub owner with ties to every side.",
        "plot_lines": ["Broker deals", "Play all sides"]
    },
    {
        "name": "Svetlana Petrova",
        "role": "undetermined",
        "traits": ["enigmatic", "loyal", "skilled hacker"],
        "backstory": "Escaped from a secret lab, now on the run.",
        "plot_lines": ["Help protagonist", "Hide from villain"]
    }
]

# --- Mock story generation (since actual generation requires OpenAI and complex dependencies) ---
def mock_generate_story(
    conflict,
    setting,
    narrative_style,
    mood,
    protagonist_name,
    protagonist_gender,
    character_info=None,
    additional_characters=None,
    **kwargs
):
    """A mock implementation of story generation for development purposes"""
    
    # Create a reasonable narrative that includes the parameters provided
    narrative = f"""You are {protagonist_name}, a skilled operative drawn into a web of {conflict.lower()} in {setting}. 
    
The room is dimly lit as Evelyn Fox slides a manila folder across the weathered oak table. Her expression is stern, tinged with that familiar exasperation you've come to expect.

"Listen carefully, {protagonist_name}," she says, adjusting her glasses. "Viktor Dragunov has obtained schematics for an AI-powered weapons system that could destabilize the entire North Atlantic security framework. The geopolitical implications alone would trigger a paradigm shift in how we approach multilateral defense treaties."

You stifle a yawn as she continues her lecture on international relations. Same old Fox - brilliant but unable to get to the point.

"In plain English, Fox?" you interrupt, with the devil-may-care attitude that's both your signature and your curse.

She glares at you. "Steal back the schematics before Dragunov can implement them. You have 72 hours. And try not to cause an international incident this time."

As you exit her office, you consider your next move. The mission is clear, but the path forward is anything but. You'll need allies, information, and a bit of luck.

According to intelligence reports, Maximilian Zhou might have information about Dragunov's security systems. His nightclub, The Golden Dragon, serves as a neutral meeting ground for various operatives. But can he be trusted? He's known to play both sides.

Alternatively, there are rumors that Svetlana Petrova, a skilled hacker who escaped from one of Dragunov's laboratories, might be willing to help bring down her former captor. Finding her won't be easy though - she's in hiding, constantly moving.

You check your equipment and consider the resources at your disposal. Time is ticking."""

    # Generate three choices that make sense for the story
    choices = [
        {
            "choice_id": "1",
            "text": f"Visit Maximilian Zhou at The Golden Dragon nightclub to gather intelligence on Dragunov's security systems"
        },
        {
            "choice_id": "2",
            "text": f"Track down Svetlana Petrova for her insider knowledge of Dragunov's operations"
        },
        {
            "choice_id": "3",
            "text": f"Conduct your own reconnaissance of Dragunov's known headquarters before making contact with any potential allies"
        }
    ]
    
    return {
        "narrative_text": narrative,
        "choices": choices,
        "conflict": conflict,
        "setting": setting,
        "narrative_style": narrative_style,
        "mood": mood
    }

# --- API Routes ---
@app.get("/")
async def root():
    return {"message": "SpyEngine API is running"}

@app.get("/api/v1/story_options", response_model=Dict[str, List[Tuple[str, str]]])
async def story_options():
    """Get all available story options for UI display."""
    return STORY_OPTIONS

@app.get("/api/v1/characters")
async def get_random_characters(count: int = 3):
    """Get random characters from the database (mocked for now)."""
    # In a real implementation, this would pull from the database
    if count > len(MOCK_CHARACTERS):
        count = len(MOCK_CHARACTERS)
    return random.sample(MOCK_CHARACTERS, count)

@app.get("/api/v1/state")
async def get_initial_state():
    """Get initial game state with default currency balances."""
    return {
        "currency_balances": DEFAULT_CURRENCY_BALANCES,
        "story_text": None,
        "choices": []
    }

@app.post("/api/v1/generate_story")
async def create_story(request: StoryRequest):
    """Generate a new story based on user selections."""
    try:
        # Get random characters (would be from database in production)
        char_pool = MOCK_CHARACTERS
        mission_giver = next((c for c in char_pool if c["role"] == "mission-giver"), None)
        villain = next((c for c in char_pool if c["role"] == "villain"), None)
        others = [c for c in char_pool if c["role"] not in ["mission-giver", "villain"]]
        
        # Ensure we have a mission-giver and villain
        if not mission_giver or not villain:
            raise HTTPException(status_code=500, detail="Required character roles not found")
        
        # Select additional characters
        additional_chars = random.sample(others, min(2, len(others)))
        all_chars = [mission_giver] + [villain] + additional_chars
        
        # Generate story (mocked for now without OpenAI)
        story_data = mock_generate_story(
            conflict=request.conflict,
            setting=request.setting,
            narrative_style=request.narrative_style,
            mood=request.mood,
            protagonist_name=request.protagonist_name,
            protagonist_gender=request.protagonist_gender,
            custom_conflict=request.custom_conflict,
            custom_setting=request.custom_setting,
            custom_narrative=request.custom_narrative,
            custom_mood=request.custom_mood,
            # In production, these would be real DB objects
            character_info=mission_giver,
            additional_characters=[villain] + additional_chars
        )
        
        # Return data with characters and currency balances
        response = {
            "story_data": story_data,
            "currency_balances": DEFAULT_CURRENCY_BALANCES,
            "characters": all_chars
        }
        
        return response
    
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")

@app.post("/api/v1/choice")
async def make_choice(request: ChoiceRequest):
    """Process a user's choice in the story."""
    # This would connect to GameEngine.make_choice() in a full implementation
    try:
        # Generate a continuation based on the choice
        if request.choice_id == "1":
            narrative = "You decide to visit Maximilian Zhou at The Golden Dragon nightclub. The neon-lit establishment pulses with energy as you make your way through the crowd. Zhou spots you from his private booth and waves you over, his expression revealing nothing about his intentions."
            choices = [
                {"choice_id": "4", "text": "Ask directly about Dragunov's security systems"},
                {"choice_id": "5", "text": "Play it cool, order drinks and ease into the conversation"},
                {"choice_id": "6", "text": "Offer Zhou a substantial payment for information"}
            ]
        elif request.choice_id == "2":
            narrative = "You begin the challenging task of tracking down Svetlana Petrova. After calling in several favors and following a trail of digital breadcrumbs, you find yourself at an abandoned warehouse that's been converted into a hacker's paradise. Petrova regards you suspiciously from behind a wall of monitors."
            choices = [
                {"choice_id": "7", "text": "Appeal to her desire for revenge against Dragunov"},
                {"choice_id": "8", "text": "Offer technical equipment and resources in exchange for help"},
                {"choice_id": "9", "text": "Be honest about the mission and the stakes"}
            ]
        else:
            narrative = "You decide to conduct your own reconnaissance before involving potential allies. Under cover of darkness, you approach one of Dragunov's known facilities. The compound is heavily guarded, but you notice a potential vulnerability in the patrol patterns."
            choices = [
                {"choice_id": "10", "text": "Attempt to infiltrate now while you have the element of surprise"},
                {"choice_id": "11", "text": "Document your findings and seek Maximilian Zhou's help"},
                {"choice_id": "12", "text": "Look for Petrova to help you exploit the digital security"}
            ]
        
        # Return the continuation
        return {
            "narrative_text": narrative,
            "choices": choices,
            "currency_balances": DEFAULT_CURRENCY_BALANCES
        }
    except Exception as e:
        logger.error(f"Error processing choice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Choice processing failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
