const state = { mode: "content" };

const movieSelect = document.getElementById("movie-select");
const userSelectCF = document.getElementById("user-select-cf");
const userSelectSVD = document.getElementById("user-select-svd");
const resultsGrid = document.getElementById("results-grid");
const resultsTitle = document.getElementById("results-title");
const resultsMeta = document.getElementById("results-meta");
const userHistory = document.getElementById("user-history");

const MODE_LABELS = {
  content: "Content-Based Recommendations",
  collaborative: "Collaborative Filtering Recommendations",
  svd: "Matrix Factorization (SVD) Recommendations",
};

// ---- Tab switching ----
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".mode-panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    state.mode = tab.dataset.mode;
    document.getElementById(`panel-${state.mode}`).classList.add("active");
    resultsTitle.textContent = "Recommendations";
    resultsMeta.textContent = "";
    userHistory.innerHTML = "";
    resultsGrid.innerHTML = `<p class="placeholder">Hit the button to generate recommendations.</p>`;
  });
});

// ---- Populate dropdowns ----
async function init() {
  const movies = await fetch("/api/movies").then((r) => r.json());
  movies
    .sort((a, b) => a.title.localeCompare(b.title))
    .forEach((m) => {
      const opt = document.createElement("option");
      opt.value = m.title;
      opt.textContent = m.title;
      movieSelect.appendChild(opt);
    });

  const users = await fetch("/api/users").then((r) => r.json());
  [userSelectCF, userSelectSVD].forEach((sel) => {
    users.forEach((u) => {
      const opt = document.createElement("option");
      opt.value = u;
      opt.textContent = `User #${u}`;
      sel.appendChild(opt);
    });
  });
}
init();

// ---- Rendering ----
function renderResults(results) {
  resultsGrid.innerHTML = "";
  if (!Array.isArray(results) || results.length === 0) {
    resultsGrid.innerHTML = `<p class="placeholder">No recommendations found.</p>`;
    return;
  }
  const maxScore = Math.max(...results.map((r) => r.score), 0.0001);
  results.forEach((movie, i) => {
    const pct = Math.max(4, Math.round((Math.max(movie.score, 0) / maxScore) * 100));
    const card = document.createElement("div");
    card.className = "movie-card";
    card.innerHTML = `
      <div class="rank">#${i + 1}</div>
      <h3>${movie.title}</h3>
      <div class="genres">${movie.genres}</div>
      <div class="score-bar"><div class="score-bar-fill" style="width:${pct}%"></div></div>
      <div class="score-label">match score: ${movie.score}</div>
    `;
    resultsGrid.appendChild(card);
  });
}

function renderError(msg) {
  resultsGrid.innerHTML = `<p class="placeholder">${msg}</p>`;
}

async function showUserHistory(userId) {
  const rated = await fetch(`/api/user/${userId}/ratings`).then((r) => r.json());
  if (!rated.length) { userHistory.innerHTML = ""; return; }
  const top = rated.slice(0, 5).map((m) => `${m.title} (${m.rating}★)`).join(", ");
  userHistory.innerHTML = `<strong>User #${userId}</strong> previously rated highly: ${top}`;
}

// ---- Button actions ----
document.getElementById("btn-content").addEventListener("click", async () => {
  const title = movieSelect.value;
  resultsTitle.textContent = MODE_LABELS.content;
  resultsMeta.textContent = `similar to "${title}"`;
  userHistory.innerHTML = "";
  resultsGrid.innerHTML = `<p class="placeholder">Loading…</p>`;
  const data = await fetch(`/api/recommend/content?title=${encodeURIComponent(title)}`).then((r) => r.json());
  if (data.error) return renderError(data.error);
  renderResults(data);
});

document.getElementById("btn-collaborative").addEventListener("click", async () => {
  const userId = userSelectCF.value;
  resultsTitle.textContent = MODE_LABELS.collaborative;
  resultsMeta.textContent = `for User #${userId}`;
  resultsGrid.innerHTML = `<p class="placeholder">Loading…</p>`;
  await showUserHistory(userId);
  const data = await fetch(`/api/recommend/collaborative?user_id=${userId}`).then((r) => r.json());
  if (data.error) return renderError(data.error);
  renderResults(data);
});

document.getElementById("btn-svd").addEventListener("click", async () => {
  const userId = userSelectSVD.value;
  resultsTitle.textContent = MODE_LABELS.svd;
  resultsMeta.textContent = `for User #${userId}`;
  resultsGrid.innerHTML = `<p class="placeholder">Loading…</p>`;
  await showUserHistory(userId);
  const data = await fetch(`/api/recommend/svd?user_id=${userId}`).then((r) => r.json());
  if (data.error) return renderError(data.error);
  renderResults(data);
});
