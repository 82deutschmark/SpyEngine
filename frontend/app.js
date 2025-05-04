// --- API Configuration ---
const BASE_URL = "http://localhost:8000/api/v1";

// --- STORY_OPTIONS will be fetched from API ---
let STORY_OPTIONS = {
  conflicts: [],
  settings: [],
  narrative_styles: [],
  moods: []
};

// --- Character data from API ---
let characters = [];

// --- UI Helper Functions ---
function showSection(id, show=true) {
  const el = document.getElementById(id);
  if (el) el.style.display = show ? '' : 'none';
}

function renderStory(text) {
  document.getElementById('story-container').textContent = text;
}

function renderBalances(balances) {
  const ul = document.getElementById('currency-list');
  ul.innerHTML = '';
  Object.entries(balances).forEach(([symbol, amount]) => {
    const li = document.createElement('li');
    li.textContent = `${symbol} ${amount}`;
    ul.appendChild(li);
  });
}

function renderCharacters(characters) {
  const container = document.getElementById('character-list');
  container.innerHTML = '';
  characters.forEach(char => {
    const div = document.createElement('div');
    div.className = 'character-card';
    div.innerHTML = `<strong>${char.name}</strong> <em>(${char.role})</em><br>
      <b>Traits:</b> ${char.traits.join(', ')}<br>
      <b>Backstory:</b> ${char.backstory}<br>
      <b>Plot Lines:</b> ${char.plot_lines.join(', ')}`;
    container.appendChild(div);
  });
}

function renderChoices(choices) {
  const list = document.getElementById('choices-list');
  list.innerHTML = '';
  choices.forEach(choice => {
    const div = document.createElement('div');
    div.innerHTML = `<input type="radio" name="story-choice" value="${choice.choice_id}" id="choice-${choice.choice_id}">
      <label for="choice-${choice.choice_id}">${choice.text}</label>`;
    list.appendChild(div);
  });
}

// --- API Functions ---
async function fetchStoryOptions() {
  try {
    const response = await fetch(`${BASE_URL}/story_options`);
    if (!response.ok) throw new Error('Failed to fetch story options');
    
    STORY_OPTIONS = await response.json();
    populateOptions();
  } catch (error) {
    console.error('Error fetching story options:', error);
    // Fall back to empty options, will be populated in populateOptions() if needed
  }
}

async function fetchInitialState() {
  try {
    const response = await fetch(`${BASE_URL}/state`);
    if (!response.ok) throw new Error('Failed to fetch initial state');
    
    const data = await response.json();
    if (data.currency_balances) {
      renderBalances(data.currency_balances);
    }
    
    return data;
  } catch (error) {
    console.error('Error fetching initial state:', error);
    return { currency_balances: {} };
  }
}

async function fetchRandomCharacters() {
  try {
    const response = await fetch(`${BASE_URL}/characters?count=3`);
    if (!response.ok) throw new Error('Failed to fetch characters');
    
    characters = await response.json();
    renderCharacters(characters);
    return characters;
  } catch (error) {
    console.error('Error fetching characters:', error);
    return [];
  }
}

async function generateStory(storyData) {
  try {
    const response = await fetch(`${BASE_URL}/generate_story`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(storyData)
    });
    
    if (!response.ok) throw new Error('Failed to generate story');
    
    const data = await response.json();
    
    // Render story components
    if (data.story_data && data.story_data.narrative_text) {
      renderStory(data.story_data.narrative_text);
    }
    
    if (data.story_data && data.story_data.choices) {
      renderChoices(data.story_data.choices);
    }
    
    if (data.currency_balances) {
      renderBalances(data.currency_balances);
    }
    
    if (data.characters) {
      characters = data.characters;
      renderCharacters(characters);
    }
    
    return data;
  } catch (error) {
    console.error('Error generating story:', error);
    // Show error message in story container
    renderStory(`Error: Could not generate story. Please try again.`);
    return null;
  }
}

async function submitChoice(choiceId, customText = null) {
  try {
    const response = await fetch(`${BASE_URL}/choice`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        choice_id: choiceId,
        custom_choice_text: customText
      })
    });
    
    if (!response.ok) throw new Error('Failed to submit choice');
    
    const data = await response.json();
    
    // Update UI with response
    if (data.narrative_text) {
      renderStory(data.narrative_text);
    }
    
    if (data.choices) {
      renderChoices(data.choices);
    }
    
    if (data.currency_balances) {
      renderBalances(data.currency_balances);
    }
    
    return data;
  } catch (error) {
    console.error('Error submitting choice:', error);
    // Show error in story
    renderStory(document.getElementById('story-container').textContent + 
      `\n\nError: Could not process your choice. Please try again.`);
    return null;
  }
}

// --- UI Initialization ---
function populateOptions() {
  function fill(selectId, options) {
    const sel = document.getElementById(selectId);
    sel.innerHTML = '';
    
    // If API fetch failed and STORY_OPTIONS is empty, use defaults
    if (!options || options.length === 0) {
      // Don't show empty dropdowns
      return;
    }
    
    options.forEach(([icon, label]) => {
      const opt = document.createElement('option');
      opt.value = label;
      opt.textContent = `${icon} ${label}`;
      sel.appendChild(opt);
    });
  }
  
  fill('conflict-select', STORY_OPTIONS.conflicts);
  fill('setting-select', STORY_OPTIONS.settings);
  fill('narrative-style-select', STORY_OPTIONS.narrative_styles);
  fill('mood-select', STORY_OPTIONS.moods);
}

// --- Event Handlers ---
document.getElementById('initial-input-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  // Collect form data
  const storyData = {
    protagonist_name: document.getElementById('protagonist-name').value.trim(),
    protagonist_gender: document.getElementById('protagonist-gender').value,
    conflict: document.getElementById('conflict-select').value,
    setting: document.getElementById('setting-select').value,
    narrative_style: document.getElementById('narrative-style-select').value,
    mood: document.getElementById('mood-select').value
  };
  
  // Save to localStorage
  Object.entries(storyData).forEach(([key, value]) => {
    localStorage.setItem(key, value);
  });
  
  // Show loading state
  renderStory('Generating your adventure...');
  showSection('story-section', true);
  
  // Fetch characters and show character section
  await fetchRandomCharacters();
  showSection('character-section', true);
  
  // Hide input form, show other sections
  showSection('initial-input-section', false);
  showSection('currency-section', true);
  showSection('choice-section', true);
  
  // Generate story with selected options
  await generateStory(storyData);
});

document.getElementById('choice-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const selected = document.querySelector('input[name="story-choice"]:checked');
  if (!selected) return;
  
  // Get the choice text to include in story
  const choiceText = selected.nextElementSibling.textContent;
  
  // Update story to acknowledge selection
  const currentStory = document.getElementById('story-container').textContent;
  renderStory(`${currentStory}\n\nYou chose: ${choiceText}\n\nProcessing...`);
  
  // Send choice to backend
  await submitChoice(selected.value, choiceText);
});

// --- Initialize App ---
async function initializeApp() {
  // Fetch story options from API
  await fetchStoryOptions();
  
  // Fetch initial state
  await fetchInitialState();
  
  // Restore from localStorage if available
  const fields = ['protagonist-name', 'protagonist-gender', 'conflict-select', 
                 'setting-select', 'narrative-style-select', 'mood-select'];
  
  fields.forEach(id => {
    const storageKey = id.replace('-', '_');
    const value = localStorage.getItem(storageKey);
    if (value) {
      const el = document.getElementById(id);
      if (el) el.value = value;
    }
  });
}

// Initialize on page load
window.onload = initializeApp;
