// =========================
// Matrix Problem Codes JS
// =========================

const MATRIX_API_BASE = "/api/matrixproblemcodes";
const LEVEL4_API_BASE = "/api/locations/level4";      // adjust to your actual endpoint
const PROBLEM_API_BASE = "/api/problemcodes";


document.addEventListener("DOMContentLoaded", async () => {

  requireAuth()
    .then(user => {
      const userBox = document.getElementById("userBox");
      if (userBox) {
        userBox.innerHTML = `Signed in as: <strong>${user.email}</strong>`;
      }
    })
    .catch(() => {
      console.warn("Auth failed, loading page anyway");
    })
    .finally(async () => {
      await loadLevel4Locations();
      await loadProblemCodes();
      await loadMatrixForSelectedLocation();
    });
    

});
function getField(id) {
  return document.getElementById(id);
}
// -------- LOAD DROPDOWNS --------
async function loadLevel4Locations() {
  try {
    const res = await fetch(LEVEL4_API_BASE + "/");
    if (!res.ok) return;
    const data = await res.json();

    const select = getField("level4_id");
    select.innerHTML = `<option value="">-- Select Location --</option>`;

    data.forEach(loc => {
      const opt = document.createElement("option");
      opt.value = loc.id;
      opt.textContent = `${loc.customer_site} - ${loc.room_desc}`;
      select.appendChild(opt);
    });

    select.addEventListener("change", loadMatrixForSelectedLocation);
  } catch (err) {
    console.error("Error loading level4 locations", err);
  }
}

async function loadProblemCodes() {
  try {
    const res = await fetch(PROBLEM_API_BASE + "/");
    if (!res.ok) return;
    const data = await res.json();

    const select = getField("problem_code_id");
    select.innerHTML = `<option value="">-- Select Problem Code --</option>`;

    data.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = `${p.problem_code_num} - ${p.problem_code_description}`;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error("Error loading problem codes", err);
  }
}

// -------- LOAD MATRIX TABLE --------
async function loadMatrixForSelectedLocation() {
  const level4Id = getField("level4_id").value;
  const tbody = document.querySelector("#matrix-problem-code-table tbody");
  tbody.innerHTML = "";

  if (!level4Id) return;

  try {
    console.log("LEVEL4 ID =", level4Id);
    console.log("FETCH URL =", `${MATRIX_API_BASE}/by-location/${level4Id}`);

    const res = await fetch(`${MATRIX_API_BASE}/by-location/${level4Id}`);
    if (!res.ok) return;
    const data = await res.json();

    data.forEach(row => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${row.level4_id}</td>
        <td>${row.problem_code_id}</td>
        <td></td>
        <td>${row.date_open ?? ""}</td>
        <td>${row.date_close ?? ""}</td>
        <td class="actions">
          <button class="delete-btn" data-id="${row.id}">🗑️</button>
        </td>
      `;

      tbody.appendChild(tr);
    });

    wireDeleteButtons();
  } catch (err) {
    console.error("Error loading matrix problem codes", err);
  }
}

// -------- ADD MATRIX ROW --------
async function addMatrixProblemCode(event) {
  event.preventDefault();

  const level4Id = parseInt(getField("level4_id").value, 10);
  const problemCodeId = parseInt(getField("problem_code_id").value, 10);

  if (isNaN(level4Id) || isNaN(problemCodeId)) {
    alert("Select both Level 4 Location and Problem Code.");
    return;
  }

  const payload = {
    level4_id: level4Id,
    problem_code_id: problemCodeId,
    date_open: getField("date_open").value || null,
    date_close: getField("date_close").value || null,
  };

  console.log("SENDING PAYLOAD →", payload);

  const res = await fetch(MATRIX_API_BASE + "/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    console.error("Failed to create matrix problem code", await res.text());
    return;
  }

  getField("problem_code_id").value = "";
  getField("date_open").value = "";
  getField("date_close").value = "";

  await loadMatrixForSelectedLocation();
}


// -------- DELETE --------
function wireDeleteButtons() {
  document.querySelectorAll("#matrix-problem-table .delete-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      const id = e.target.dataset.id;
      if (!confirm("Delete this matrix problem code?")) return;

      const res = await fetch(`${MATRIX_API_BASE}/${id}`, {
        method: "DELETE"
      });

      if (!res.ok) {
        console.error("Failed to delete", await res.text());
        return;
      }

      loadMatrixForSelectedLocation();
    });
  });
}

// -------- BUTTON WIRING --------
const addBtn = document.getElementById("matrix-add-btn");
if (addBtn) {
  addBtn.addEventListener("click", addMatrixProblemCode);
}

const templateBtn = document.getElementById("matrix-template-btn");
if (templateBtn) {
  templateBtn.addEventListener("click", () => {
    window.location.href = MATRIX_API_BASE + "/template";
  });
}

const dataBtn = document.getElementById("matrix-data-btn");
if (dataBtn) {
  dataBtn.addEventListener("click", () => {
    window.location.href = MATRIX_API_BASE + "/data";
  });
}
