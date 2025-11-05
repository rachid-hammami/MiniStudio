// === MiniStudio Dashboard ===
// Contrôle visuel complet du tableau de bord IA
// Version restaurée étape 7

const API_BASE = window.location.origin.replace(/\/$/, "");
const suggestionsContainer = document.getElementById("suggestions");
const reportsContainer = document.getElementById("reports");
const filesContainer = document.getElementById("files");
const themeToggle = document.getElementById("themeToggle");
const controls = document.getElementById("controls");

const statusElements = {
  suggestions: document.getElementById("suggestions-status"),
  reports: document.getElementById("reports-status"),
  files: document.getElementById("files-status"),
};

// === Thème sombre/clair ===
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
});
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark");
}

// === Création dynamique des boutons d'action ===
const actionBar = document.createElement("div");
actionBar.style.textAlign = "center";
actionBar.style.margin = "1em";

const btnAnalyze = createButton("Analyser 🔍", analyzeFiles);
const btnClear = createButton("Nettoyer 🧹", clearSuggestions);
const btnRefresh = createButton("Rafraîchir 🔄", refreshAll);

actionBar.append(btnAnalyze, btnClear, btnRefresh);
document.body.insertBefore(actionBar, document.querySelector("main"));

function createButton(label, onClick) {
  const btn = document.createElement("button");
  btn.textContent = label;
  btn.style.margin = "0.3em";
  btn.style.padding = "0.6em 1.2em";
  btn.style.cursor = "pointer";
  btn.addEventListener("click", onClick);
  return btn;
}

// === Chargement initial des données ===
refreshAll();

// === Rafraîchir toutes les sections ===
async function refreshAll() {
  await Promise.all([loadSuggestions(), loadReports(), loadFiles()]);
}

// === Charger les suggestions ===
async function loadSuggestions(lang = "all") {
  statusElements.suggestions.textContent = "⏳";
  suggestionsContainer.innerHTML = "";
  try {
    const res = await fetch(`${API_BASE}/api/suggestions`);
    const data = await res.json();
    if (data.status === "ok") {
      const filtered = lang === "all"
        ? data.suggestions
        : data.suggestions.filter(s => s.language === lang);
      suggestionsContainer.innerHTML = filtered
        .map(
          s => `
          <div class="suggestion">
            <b>${s.file}</b> — <i>${s.language}</i><br>
            <span class="msg">${s.message}</span><br>
            <small>💡 ${s.suggestion}</small>
          </div>
        `
        )
        .join("");
      statusElements.suggestions.textContent = `(${filtered.length})`;
    }
  } catch (err) {
    console.error("Erreur chargement suggestions:", err);
    statusElements.suggestions.textContent = "⚠️";
  }
}

// === Charger les rapports ===
async function loadReports() {
  statusElements.reports.textContent = "⏳";
  reportsContainer.innerHTML = "";
  try {
    const res = await fetch(`${API_BASE}/api/reports`);
    const data = await res.json();
    if (data.status === "ok") {
      reportsContainer.innerHTML = data.reports
        .map(
          r => `
          <div class="report">
            <b>${r.file}</b> — <i>${r.language}</i><br>
            <span>${r.type}: ${r.message}</span>
          </div>
        `
        )
        .join("");
      statusElements.reports.textContent = `(${data.reports.length})`;
    }
  } catch (err) {
    console.error("Erreur chargement rapports:", err);
    statusElements.reports.textContent = "⚠️";
  }
}

// === Charger la liste des fichiers ===
async function loadFiles() {
  statusElements.files.textContent = "⏳";
  filesContainer.innerHTML = "";
  try {
    const res = await fetch(`${API_BASE}/api/files`);
    const data = await res.json();
    if (data.status === "ok") {
      filesContainer.innerHTML = data.files.map(f => `<li>${f}</li>`).join("");
      statusElements.files.textContent = `(${data.files.length})`;
    }
  } catch (err) {
    console.error("Erreur chargement fichiers:", err);
    statusElements.files.textContent = "⚠️";
  }
}

// === Boutons d’analyse et de nettoyage ===
async function analyzeFiles() {
  btnAnalyze.disabled = true;
  btnAnalyze.textContent = "Analyse en cours...";
  try {
    const res = await fetch(`${API_BASE}/ai/suggest`);
    const data = await res.json();
    alert(`✅ Analyse terminée : ${data.count} suggestions trouvées`);
    await refreshAll();
  } catch (err) {
    alert("❌ Erreur lors de l'analyse");
  } finally {
    btnAnalyze.disabled = false;
    btnAnalyze.textContent = "Analyser 🔍";
  }
}

async function clearSuggestions() {
  if (!confirm("Voulez-vous vraiment nettoyer toutes les suggestions ?")) return;
  btnClear.disabled = true;
  btnClear.textContent = "Nettoyage...";
  try {
    await fetch(`${API_BASE}/ai/clear`, { method: "DELETE" });
    alert("🧹 Base de suggestions nettoyée !");
    await refreshAll();
  } catch (err) {
    alert("❌ Erreur pendant le nettoyage");
  } finally {
    btnClear.disabled = false;
    btnClear.textContent = "Nettoyer 🧹";
  }
}

// === Filtres de langue ===
controls.querySelectorAll("button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const lang = btn.dataset.lang;
    controls.querySelectorAll("button").forEach(b => b.disabled = false);
    btn.disabled = true;
    loadSuggestions(lang);
  });
});
