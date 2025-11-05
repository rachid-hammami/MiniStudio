// === MiniStudio Control Panel ===

const base = window.location.origin;

async function callAPI(endpoint, method = "GET") {
  const res = await fetch(base + endpoint, { method });
  return await res.json();
}

document.getElementById("startServer").onclick = async () => {
  alert("Le serveur FastAPI doit déjà tourner pour être contrôlé.");
};

document.getElementById("stopServer").onclick = async () => {
  const data = await callAPI("/control/stop", "POST");
  alert(data.message);
};

document.getElementById("restartServer").onclick = async () => {
  const data = await callAPI("/control/restart", "POST");
  alert(data.message);
};

document.getElementById("startNgrok").onclick = async () => {
  const data = await callAPI("/control/ngrok/start", "POST");
  alert(data.message);
};

document.getElementById("stopNgrok").onclick = async () => {
  const data = await callAPI("/control/ngrok/stop", "POST");
  alert(data.message);
};

(async () => {
  const data = await callAPI("/control/api-key");
  document.getElementById("apiKey").textContent = "🔑 " + data.key;
})();
