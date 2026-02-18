// =========================
// Priority Codes JS Module
// =========================

requireAuth()
  .then(user => {
    const userBox = document.getElementById("userBox");
    if (userBox) {
      userBox.innerHTML = `Signed in as: <strong>${user.email}</strong>`;
    }
  })
  .catch(err => {
    console.warn("Auth failed, loading page anyway");
  })
  .finally(() => {
    loadPriorityCodes();   // ALWAYS load data
  });

const API_BASE = "/api/prioritycodes";

function getField(id) {
  return document.getElementById(id);
}

// =========================
// LOAD TABLE
// =========================
async function loadPriorityCodes() {
  try {
    const res = await fetch(API_BASE + "/");
    if (!res.ok) return;
    const data = await res.json();

    const tbody = document.querySelector("#priority-table tbody");
    tbody.innerHTML = "";

    data.forEach(row => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${row.priority_code}</td>
        <td>${row.priority_description}</td>
        <td>${row.target_response_time ?? ""}</td>
        <td>${row.target_completed ?? ""}</td>
        <td>${row.date_open ?? ""}</td>
        <td>${row.date_close ?? ""}</td>
        <td class="actions">
          <button class="edit-btn" data-id="${row.id}">✏️</button>
          <button class="delete-btn" data-id="${row.id}">🗑️</button>
        </td>
      `;

      tbody.appendChild(tr);
    });

    // After rows are rendered, wire up buttons
    wireDeleteButtons();
    wireEditButtons();

  } catch (err) {
    console.error("Error loading priority codes", err);
  }
}

// =========================
// SAVE NEW PRIORITY
// =========================
async function savePriority(event) {
  event.preventDefault(); // prevent page reload

  const payload = {
    priority_code: getField("priority_code").value.trim(),
    priority_description: getField("priority_description").value.trim(),
    target_response_time: getField("target_response_time").value
      ? parseInt(getField("target_response_time").value, 10)
      : null,
    target_completed: getField("target_completed").value
      ? parseInt(getField("target_completed").value, 10)
      : null,
    date_open: getField("date_open").value || null,
    date_close: getField("date_close").value || null,
  };

  const res = await fetch(API_BASE + "/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    console.error("Failed to save priority", await res.text());
    return;
  }

  // Clear fields
  getField("priority_code").value = "";
  getField("priority_description").value = "";
  getField("target_response_time").value = "";
  getField("target_completed").value = "";
  getField("date_open").value = "";
  getField("date_close").value = "";

  await loadPriorityCodes();
}

// =========================
// DELETE BUTTON HANDLER
// =========================
function wireDeleteButtons() {
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;

      if (!confirm("Delete this priority code?")) return;

      const res = await fetch(`${API_BASE}/${id}`, {
        method: "DELETE"
      });

      if (!res.ok) {
        console.error("Failed to delete", await res.text());
        return;
      }

      loadPriorityCodes();
    });
  });
}

// =========================
// EDIT BUTTON HANDLER
// =========================
function wireEditButtons() {
  document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const id = e.target.dataset.id;
      const tr = e.target.closest("tr");
      const cells = tr.querySelectorAll("td");

      const priority_code = cells[0].innerText;
      const priority_description = cells[1].innerText;
      const target_response_time = cells[2].innerText;
      const target_completed = cells[3].innerText;
      const date_open = cells[4].innerText;
      const date_close = cells[5].innerText;

      tr.innerHTML = `
        <td><input value="${priority_code}" id="edit_code_${id}"></td>
        <td><input value="${priority_description}" id="edit_desc_${id}"></td>
        <td><input value="${target_response_time}" id="edit_resp_${id}" type="number"></td>
        <td><input value="${target_completed}" id="edit_comp_${id}" type="number"></td>
        <td><input value="${date_open}" id="edit_open_${id}" type="date"></td>
        <td><input value="${date_close}" id="edit_close_${id}" type="date"></td>
        <td>
          <button class="save-edit-btn" data-id="${id}">💾</button>
          <button class="cancel-edit-btn">✖</button>
        </td>
      `;

      wireEditSave(id);
      wireCancelEdit();
    });
  });
}

// =========================
// SAVE EDITED ROW
// =========================
function wireEditSave(id) {
  document.querySelector(`.save-edit-btn[data-id="${id}"]`)
    .addEventListener("click", async () => {

      const payload = {
        priority_code: document.getElementById(`edit_code_${id}`).value.trim(),
        priority_description: document.getElementById(`edit_desc_${id}`).value.trim(),
        target_response_time: parseInt(document.getElementById(`edit_resp_${id}`).value) || null,
        target_completed: parseInt(document.getElementById(`edit_comp_${id}`).value) || null,
        date_open: document.getElementById(`edit_open_${id}`).value || null,
        date_close: document.getElementById(`edit_close_${id}`).value || null,
      };

      const res = await fetch(`${API_BASE}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        console.error("Failed to update", await res.text());
        return;
      }

      loadPriorityCodes();
    });
}

// =========================
// CANCEL EDIT
// =========================
function wireCancelEdit() {
  document.querySelector(".cancel-edit-btn")
    ?.addEventListener("click", () => loadPriorityCodes());
}

// =========================
// BUTTON WIRING
// =========================
const saveBtn = document.getElementById("priority-save-btn");
if (saveBtn) {
  saveBtn.addEventListener("click", savePriority);
}

const templateBtn = document.getElementById("priority-template-btn");
if (templateBtn) {
  templateBtn.addEventListener("click", () => {
    window.location.href = API_BASE + "/template";
  });
}

const dataBtn = document.getElementById("priority-data-btn");
if (dataBtn) {
  dataBtn.addEventListener("click", () => {
    window.location.href = API_BASE + "/data";
  });
}
