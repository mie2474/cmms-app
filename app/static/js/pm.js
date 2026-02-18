async function loadPM() {
  const data = await apiGet("/pm");
  const tbody = document.querySelector("#pmTable tbody");
  tbody.innerHTML = "";
  data.forEach(pm => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${pm.name}</td>
      <td>${pm.asset_id || ""}</td>
      <td>${pm.frequency_days || ""}</td>
      <td>${pm.priority || ""}</td>
    `;
    tbody.appendChild(tr);
  });
}

function initPM() {
  const form = document.getElementById("pmForm");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById("pm-name").value,
      description: document.getElementById("pm-description").value || null,
      asset_id: document.getElementById("pm-asset").value || null,
      frequency_days: document.getElementById("pm-frequency").value
        ? parseInt(document.getElementById("pm-frequency").value, 10)
        : null,
      priority: document.getElementById("pm-priority").value || null
    };
    await apiPost("/pm/", payload);
    form.reset();
    loadPM();
  });

  loadPM();
}
