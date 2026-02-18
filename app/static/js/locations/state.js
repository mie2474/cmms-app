document.addEventListener("DOMContentLoaded", async () => {
  await requireAuth();
  attachLayout();

  document.getElementById("state-save-btn").addEventListener("click", saveState);
});

async function saveState() {
  const payload = {
    name: document.getElementById("state-name").value,
    code: document.getElementById("state-code").value,
    status: Number(document.getElementById("state-status").value)
  };

  const res = await fetch("/api/locations/state", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    alert("Failed to save state");
    return;
  }

  alert("State saved successfully");
}
