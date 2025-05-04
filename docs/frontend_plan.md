# Front-end Checklist (CapacitorJS Static Prototype)

> Use this file as a running checklist. Tick items off as completed.

## 1. Directory
- [ ] Create `frontend/` root inside repository.

## 2. Entry Document
- [ ] `frontend/index.html` with:
  - Initial input form for:
    - Protagonist name (text)
    - Protagonist gender (dropdown)
    - Conflict (dropdown, from STORY_OPTIONS)
    - Setting (dropdown, from STORY_OPTIONS)
    - Narrative style (dropdown, from STORY_OPTIONS)
    - Mood (dropdown, from STORY_OPTIONS)
  - `<div id="story-container">` to render narrative paragraphs.
  - `<ul id="currency-list">` with balances.
  - Choice form (`<input id="choice-input">` – `<button id="send-choice">`).
  - Section to display featured/random NPC character(s) (with traits, backstory, etc).

## 3. Styling
- [ ] `frontend/styles.css` – flex column layout, dark spy-themed palette.

## 4. Behaviour Script
- [ ] `frontend/app.js`
  - `const BASE_URL = "http://localhost:8000/api/v1"; // adjustable`.
  - `fetchInitialState()` – GET `/state` (or build initial state from user input).
  - `fetchStory()` – POST `/generate_story` with all user-selected options and protagonist info.
  - `postChoice(choice)` – POST `/choice`.
  - Fetch and display random featured/secondary NPC character(s) (mocked for now).
  - DOM update helpers `renderStory(node)`, `renderBalances(balances)`, `renderCharacters(characters)`.
  - Use `localStorage` to preserve state and user selections between reloads.
  - Modular, clearly commented code.

## 5. Local Preview
- [ ] Run: `python -m http.server 8000 -d frontend`.
- [ ] Visit: `http://localhost:8000`.

## 6. Future (post-refactor)
- [ ] Migrate to full Capacitor+React project (`frontend/capacitor-app/`).
- [ ] Integrate real authentication and error handling.
