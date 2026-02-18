// =========================
// Problem Codes JS Module
// =========================

const PROBLEM_API_BASE = "/api/problemcodes";
const PRIORITY_API_BASE = "/api/prioritycodes";

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
  .finally(async () => {
    await loadPrioritiesDropdown();
    await loadProblemCodes();
  });

function getField(id) {
  return document.getElementById(id);
}

// =========================
// LOAD PRIORITIES DROPDOWN
// =========================
async function loadPrioritiesDropdown() {
  try {
    const res = await fetch(PRIORITY_API_BASE + "/");
    if (!res.ok) return;
    const data = await res.json();

    const select = getField("priority_id");
    if (!select) return;

    select.innerHTML = `<option value="">-- Select Priority --</option>`;

    data.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;              // FK is priority_id (int)
      opt.textContent = p.priority_code;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error("Error loading priorities", err);
  }
}

// =========================
// LOAD PROBLEM CODES TABLE
// =========================
async function loadProblemCodes() {
  try {
    const res = await fetch(PROBLEM_API_BASE + "/");
    if (!res.ok) return;
    const data = await res.json();

    const tbody = document.querySelector("#problem-table tbody");
    tbody.innerHTML = "";

    data.forEach(row => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${row.problem_code_num}</td>
        <td>${row.problem_code_description}</td>
        <td>${row.priority_id ?? ""}</td>
        <td>${row.date_open ?? ""}</td>
        <td>${row.date_closed ?? ""}</td>
        <td class="actions">
          <button class="edit-btn" data-id="${row.id}">✏️</button>
          <button class="delete-btn" data-id="${row.id}">🗑️</button>
        </td>
      `;

      tbody.appendChild(tr);
    });

    wireProblemDeleteButtons();
    wireProblemEditButtons();

  } catch (err) {
    console.error("Error loading problem codes", err);
  }
}

// =========================
// SAVE NEW PROBLEM CODE
// =========================
async function saveProblem(event) {
  event.preventDefault();

  const payload = {
    problem_code_num: getField("problem_code_num").value.trim(),
    problem_code_description: getField("problem_code_description").value.trim(),
    priority_id: getField("priority_id").value
      ? parseInt(getField("priority_id").value, 10)
      : null,
    date_open: getField("date_open").value || null,
    date_closed: getField("date_closed").value || null,
  };

  const res = await fetch(PROBLEM_API_BASE + "/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    console.error("Failed to save problem code", await res.text());
    return;
  }

  getField("problem_code_num").value = "";
  getField("problem_code_description").value = "";
  getField("priority_id").value = "";
  getField("date_open").value = "";
  getField("date_closed").value = "";

  await loadProblemCodes();
}

// =========================
// DELETE BUTTON HANDLER
// =========================
function wireProblemDeleteButtons() {
  document.querySelectorAll("#problem-table .delete-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;

      if (!confirm("Delete this problem code?")) return;

      const res = await fetch(`${PROBLEM_API_BASE}/${id}`, {
        method: "DELETE"
      });

      if (!res.ok) {
        console.error("Failed to delete", await res.text());
        return;
      }

      loadProblemCodes();
    });
  });
}

// =========================
// EDIT BUTTON HANDLER
// =========================
function wireProblemEditButtons() {
  document.querySelectorAll("#problem-table .edit-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const id = e.target.dataset.id;
      const tr = e.target.closest("tr");
      const cells = tr.querySelectorAll("td");

      const problem_code_num = cells[0].innerText;
      const problem_code_description = cells[1].innerText;
      const priority_id = cells[2].innerText;
      const date_open = cells[3].innerText;
      const date_closed = cells[4].innerText;

      tr.innerHTML = `
        <td><input value="${problem_code_num}" id="edit_num_${id}"></td>
        <td><input value="${problem_code_description}" id="edit_desc_${id}"></td>
        <td>
          <select id="edit_priority_${id}">
            ${buildPriorityOptions(priority_id)}
          </select>
        </td>
        <td><input value="${date_open}" id="edit_open_${id}" type="date"></td>
        <td><input value="${date_closed}" id="edit_close_${id}" type="date"></td>
        <td>
          <button class="save-edit-btn" data-id="${id}">💾</button>
          <button class="cancel-edit-btn">✖</button>
        </td>
      `;

      wireProblemEditSave(id);
      wireProblemCancelEdit();
    });
  });
}

// Build options for edit dropdown using the main priority select as source
function buildPriorityOptions(selectedId) {
  const mainSelect = getField("priority_id");
  if (!mainSelect) return "";

  let html = "";
  Array.from(mainSelect.options).forEach(opt => {
    if (!opt.value) return;
    const selected = opt.value === selectedId ? "selected" : "";
    html += `<option value="${opt.value}" ${selected}>${opt.textContent}</option>`;
  });
  return html;
}

// =========================
// SAVE EDITED ROW
// =========================
function wireProblemEditSave(id) {
  document.querySelector(`.save-edit-btn[data-id="${id}"]`)
    .addEventListener("click", async () => {

      const payload = {
        problem_code_num: document.getElementById(`edit_num_${id}`).value.trim(),
        problem_code_description: document.getElementById(`edit_desc_${id}`).value.trim(),
        priority_id: parseInt(document.getElementById(`edit_priority_${id}`).value) || null,
        date_open: document.getElementById(`edit_open_${id}`).value || null,
        date_closed: document.getElementById(`edit_close_${id}`).value || null,
      };

      const res = await fetch(`${PROBLEM_API_BASE}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        console.error("Failed to update problem code", await res.text());
        return;
      }

      loadProblemCodes();
    });
}

// =========================
// CANCEL EDIT
// =========================
function wireProblemCancelEdit() {
  document.querySelector(".cancel-edit-btn")
    ?.addEventListener("click", () => loadProblemCodes());
}

// =========================
// BUTTON WIRING
// =========================
const problemSaveBtn = document.getElementById("problem-save-btn");
if (problemSaveBtn) {
  problemSaveBtn.addEventListener("click", saveProblem);
}
