const BASE_URL = "http://localhost:8000/api/v1"; // Adjust if backend runs elsewhere

// --- Mock fallback state ---
const mockState = {
  current_story_id: 123,
  current_node_id: 456,
  currency_balances: {
    "💎": 490,
    "💶": 5020,
    "💴": 150000,
    "💵": 4800,
    "💷": 5000
  },
  story_text: "Your mission, should you choose to accept it, begins in the heart of Berlin...",
  choice_history: ["Investigate the ambassador", "Trust the informant"]
};

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

function fetchInitialState() {
  fetch(`${BASE_URL}/state`)
    .then(r => r.json())
    .then(data => {
      renderStory(data.story_text || "(No story text)");
      renderBalances(data.currency_balances || {});
    })
    .catch(() => {
      // Fallback to mock
      renderStory(mockState.story_text);
      renderBalances(mockState.currency_balances);
    });
}

function postChoice(choice) {
  fetch(`${BASE_URL}/choice`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ choice })
  })
    .then(r => r.json())
    .then(data => {
      renderStory(data.story_text || "(No story text)");
      renderBalances(data.currency_balances || {});
    })
    .catch(() => {
      // Fallback to mock
      renderStory(mockState.story_text + "\n(Mocked response: " + choice + ")");
      renderBalances(mockState.currency_balances);
    });
}

document.getElementById('send-choice').addEventListener('click', () => {
  const input = document.getElementById('choice-input');
  const choice = input.value.trim();
  if (!choice) return;
  postChoice(choice);
  input.value = '';
});

window.onload = fetchInitialState;
