# Front-end Checklist (CapacitorJS Static Prototype)

> Use this file as a running checklist. Tick items off as completed.

## 1. Directory
- [ ] Create `frontend/` root inside repository.

## 2. Entry Document
- [ ] `frontend/index.html` with:
  - `<div id="story-container">` to render narrative paragraphs.
  - `<ul id="currency-list">` with balances.
  - Choice form (`<input id="choice-input">` – `<button id="send-choice">`).

## 3. Styling
- [ ] `frontend/styles.css` – flex column layout, dark spy-themed palette.

## 4. Behaviour Script
- [ ] `frontend/app.js`
  - `const BASE_URL = "http://localhost:8000/api/v1"; // adjustable`.
  - `fetchInitialState()` – GET `/state`.
  - `postChoice(choice)` – POST `/choice`.
  - Mock fallback with hard-coded JSON.
  - DOM update helpers `renderStory(node)`, `renderBalances(balances)`.
  - Use `localStorage` to preserve state between reloads.

## 5. Local Preview
- [ ] Run: `python -m http.server 8000 -d frontend`.
- [ ] Visit: `http://localhost:8000`.

## 6. Future (post-refactor)
- [ ] Migrate to full Capacitor+React project (`frontend/capacitor-app/`).
- [ ] Integrate real authentication and error handling.
