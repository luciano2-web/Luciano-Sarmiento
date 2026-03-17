const state = {
  hunger: 80,
  energy: 70,
  happiness: 75,
  day: 1,
};

const moodText = {
  happy: "Mochi ronronea feliz.",
  sleepy: "Mochi busca una siesta.",
  hungry: "Mochi te mira con ojitos de hambre.",
  playful: "Mochi mueve la colita esperando jugar.",
};

const elements = {
  hungerFill: document.getElementById("hungerFill"),
  energyFill: document.getElementById("energyFill"),
  happinessFill: document.getElementById("happinessFill"),
  hungerValue: document.getElementById("hungerValue"),
  energyValue: document.getElementById("energyValue"),
  happinessValue: document.getElementById("happinessValue"),
  day: document.getElementById("day"),
  catMood: document.getElementById("catMood"),
  logList: document.getElementById("logList"),
};

const clamp = (value) => Math.max(0, Math.min(100, value));

const updateBars = () => {
  elements.hungerFill.style.width = `${state.hunger}%`;
  elements.energyFill.style.width = `${state.energy}%`;
  elements.happinessFill.style.width = `${state.happiness}%`;

  elements.hungerValue.textContent = state.hunger;
  elements.energyValue.textContent = state.energy;
  elements.happinessValue.textContent = state.happiness;
  elements.day.textContent = state.day;
};

const addLog = (text) => {
  const item = document.createElement("li");
  item.textContent = text;
  elements.logList.prepend(item);
};

const updateMood = () => {
  if (state.hunger < 35) {
    elements.catMood.textContent = moodText.hungry;
    return;
  }

  if (state.energy < 35) {
    elements.catMood.textContent = moodText.sleepy;
    return;
  }

  if (state.happiness > 70) {
    elements.catMood.textContent = moodText.happy;
    return;
  }

  elements.catMood.textContent = moodText.playful;
};

const advanceDay = () => {
  state.day += 1;
  state.hunger = clamp(state.hunger - 6);
  state.energy = clamp(state.energy - 5);
  state.happiness = clamp(state.happiness - 4);
};

const actions = {
  feed() {
    state.hunger = clamp(state.hunger + 20);
    state.happiness = clamp(state.happiness + 4);
    state.energy = clamp(state.energy - 3);
    addLog("Le diste comida a Mochi. Está satisfecho.");
  },
  play() {
    state.happiness = clamp(state.happiness + 18);
    state.energy = clamp(state.energy - 12);
    state.hunger = clamp(state.hunger - 6);
    addLog("Jugaste con Mochi y persiguió una bolita.");
  },
  rest() {
    state.energy = clamp(state.energy + 22);
    state.hunger = clamp(state.hunger - 4);
    addLog("Mochi tomó una siesta cómoda.");
  },
  clean() {
    state.happiness = clamp(state.happiness + 10);
    addLog("Acariciaste a Mochi. Se siente querido.");
  },
};

const handleAction = (event) => {
  const action = event.target.dataset.action;
  if (!action || !actions[action]) return;
  actions[action]();
  advanceDay();
  updateBars();
  updateMood();
};

const start = () => {
  updateBars();
  updateMood();
  addLog("Mochi llegó a casa. ¡Cuídalo bien!");
  setInterval(() => {
    advanceDay();
    updateBars();
    updateMood();
    addLog("Otro día pasó en casa de Mochi.");
  }, 15000);
};

document.addEventListener("DOMContentLoaded", () => {
  start();
  document.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", handleAction);
  });
});
