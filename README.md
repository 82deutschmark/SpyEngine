# Spy Story Game Engine

## Overview
An interactive thriller game engine that generates dynamic narratives with branching storylines, character relationships, and mission-based gameplay in a world of high-stakes espionage.

### Key Features
- Dynamic story generation powered by OpenAI's advanced language models
- Branching storylines with consistent character and mission tracking
- Rich character integration with traits, backstories, and plot lines
- Mission-based gameplay with progress tracking and story integration
- Multi-node story persistence with comprehensive state management
- Context preservation between story segments for narrative coherence

## Architecture

### Core Components
1. **Story Generation System**
   - **Initial Story Creation** (`services/story_maker.py`)
     - `StoryGenerator` class creates new stories via OpenAI
     - `StoryPromptBuilder` constructs comprehensive prompts with character context
     - `CharacterPromptBuilder` formats character information for prompts
   
   - **Story Continuation** (`services/segment_maker.py`)
     - `StoryContinuationHandler` generates new segments based on player choices
     - Maintains narrative coherence with rich context preservation
     - Processes mission updates and character interactions
   
   - **Game Engine** (`services/game_engine.py`)
     - `GameEngine` class coordinates the entire game flow
     - `start_new_story()` method initiates new narratives
     - `make_choice()` method processes player decisions
     - Handles database transactions and state updates

2. **Character System**
   - **Character Model** (`models/character_data.py`)
     - Role-based characters (mission-giver, villain, neutral, undetermined)
     - Comprehensive character profiles with traits, backstory, plot lines
   
   - **Character Manager** (`utils/character_manager.py`)
     - `extract_character_role()` standardizes role field handling
     - `extract_character_traits()` processes various trait formats
     - `get_random_characters()` selects appropriate characters for stories
   
   - **Role Enforcement**
     - System enforces consistent character behaviors based on roles
     - Mission-givers must assign missions, villains must oppose player
     - Character ID tracking maintains consistency across story segments

3. **State Management**
   - **GameState** (`services/state_manager.py`)
     - Tracks current story position and player progress
     - Resolves current node with priority-based approach
     - Provides rich context for story continuation
     - **Note:** When serializing state (e.g., via `GameState.to_dict()`), ensure `Mission` objects are converted using their `to_dict()` method for consistency.
   
   - **StoryNode Model** (`models/stories.py`)
     - Stores narrative text and branch metadata
     - `branch_metadata` field preserves character data, mission state, and choices
     - Forms tree structure of narrative with parent-child relationships
   
   - **UserProgress Model** (`models/user.py`)
     - Tracks player state, choices, and relationships
     - Manages currency, experience, and mission progress

4. **API & Frontend Interface**
   - **Backend API** (`routes/api_routes.py` and `api/game_api.py`)
     - Stateless JSON endpoints for frontend access
     - Comprehensive error handling and validation
     - Authentication and session management
   
   - **CapacitorJS Frontend** 
     - Cross-platform mobile application framework
     - Native device feature access through Capacitor plugins
     - Responsive UI optimized for mobile devices
     - Offline functionality with local storage for game state
     - Seamless integration with backend API

## Data Flow

### Story Generation Process
1. User selects parameters and characters (via frontend app)
2. Frontend makes API request to `GameEngine.start_new_story()`
3. `StoryGenerator.generate_story()` builds prompts and calls OpenAI
4. `OpenAIContextManager.generate_initial_story()` manages API communication
5. Response is processed and stored in database models
6. `GameState` is updated with references to new story
7. API returns structured response to frontend application

### Choice Processing Flow
1. User makes choice via mobile app interface
2. Frontend sends choice to API endpoint
3. `GameEngine.make_choice()` retrieves state and current node
4. `StoryContinuationHandler.generate_continuation()` calls OpenAI with context
5. New `StoryNode` is created with comprehensive metadata
6. State transitions atomically to new node
7. Response is returned to mobile application
8. Frontend updates UI and stores game state locally

## Technical Stack
- **Backend**: Python 3.8+ with Flask web framework
- **Database**: PostgreSQL for robust data persistence
- **AI**: OpenAI API for advanced narrative generation
- **Frontend**: 
  - CapacitorJS for cross-platform mobile app development
  - Modern responsive UI with HTML5/CSS3/JavaScript
  - Native device integrations via Capacitor plugins

## Database Schema

- **StoryGeneration**: Stores story parameters (conflict, setting, style, mood)
- **StoryNode**: Contains narrative text and rich branch_metadata
- **Character**: Stores character details with traits as JSONB
- **UserProgress**: Tracks user state with game_state JSONB field
- **Mission**: Tracks mission objectives, progress, and rewards

## Documentation
- [System Documentation](docs/Updated_System_Documentation.md) - Comprehensive system overview




## Narrative Analysis Migration

This release includes a migration from the deprecated narrative functionality in `segment_maker.py` to a more robust and stateless system. Key changes include:

- **Narrative Analyzer Module**: Introduced `narrative_analyzer.py` to handle:
  - Extraction of character interactions
  - Extraction of previous choices
  - Processing of mission updates
  - Cleaning of story responses

- **Context Manager Enhancements**: The `context_manager.py` has been updated with new methods such as `extract_story_elements` and `process_story_response` to better support narrative continuity.

- **GameState Update**: The `GameState` class now includes a `get_enhanced_context` method, which provides enriched narrative context incorporating detailed character interactions and previous choices.

- **Backward Compatibility**: The deprecated `segment_maker.py` now includes adapter functions with deprecation warnings to forward calls to the new modules.
