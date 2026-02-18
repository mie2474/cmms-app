// =========================================================
// COUNTRY MASTER MODULE
// =========================================================

// -------------------------------
// Load countries on page load
// -------------------------------
document.addEventListener("DOMContentLoaded", () => {
  loadCountries();
  setupFilters();
  setupCreate();
  setupBulkload();
  setupModalControls();
});

// =========================================================
// 1. LOAD COUNTRY LIST
// =========================================================
async function loadCountries() {
  try {
    const resp = await fetch("http://127.0.0.1:8000/api/country/list", {
      credentials: "include"
    });

    const data = await resp.json();
    renderCountryTable(data);

  } catch (err) {
    console.error("Error loading countries:", err);
  }
}

// =========================================================
// 2. RENDER TABLE
// =========================================================
function renderCountryTable(rows) {
  const tbody = document.querySelector("#country-table tbody");
  tbody.innerHTML = "";

  rows.forEach(row => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td><input type="checkbox" class="row-check" data-abbr="${row.Abbreviation}"></td>

      <td>
        <a href="#" class="edit-link" data-abbr="${row.Abbreviation}">
          ${row.Abbreviation}
        </a>
      </td>

      <td>${row.Name}</td>
      <td>${row.CurrencyCode}</td>
      <td>${row.Status == 1 ? "Active" : "Inactive"}</td>
    `;

    tbody.appendChild(tr);
  });

  // Attach click handlers for edit links
  document.querySelectorAll(".edit-link").forEach(link => {
    link.addEventListener("click", openEditModal);
  });
}

// =========================================================
// 3. FILTERS
// =========================================================
function setupFilters() {
  const abbr = document.getElementById("filter-abbr");
  const name = document.getElementById("filter-name");
  const currency = document.getElementById("filter-currency");
  const status = document.getElementById("filter-status");

  [abbr, name, currency, status].forEach(el => {
    el.addEventListener("input", applyFilters);
  });
}

async function applyFilters() {
  const abbr = document.getElementById("filter-abbr").value.trim();
  const name = document.getElementById("filter-name").value.trim();
  const currency = document.getElementById("filter-currency").value.trim();
  const status = document.getElementById("filter-status").value;

  const resp = await fetch("http://127.0.0.1:8000/api/country/list", {
    credentials: "include"
  });

  const data = await resp.json();

  const filtered = data.filter(row => {
    return (
      row.Abbreviation.toLowerCase().includes(abbr.toLowerCase()) &&
      row.Name.toLowerCase().includes(name.toLowerCase()) &&
      row.CurrencyCode.toLowerCase().includes(currency.toLowerCase()) &&
      (status === "" || String(row.Status) === status)
    );
  });

  renderCountryTable(filtered);
}

// =========================================================
// 4. CREATE COUNTRY
// =========================================================
function setupCreate() {
  document.getElementById("country-add-btn").addEventListener("click", async () => {
    const payload = {
      Abbreviation: document.getElementById("country_abbr").value.trim(),
      Name: document.getElementById("country_name").value.trim(),
      CurrencyCode: document.getElementById("currency_code").value.trim(),
      Status: document.getElementById("country_status").checked ? 1 : 0
    };

    if (!payload.Abbreviation || !payload.Name || !payload.CurrencyCode) {
      alert("Abbreviation, Name, and Currency Code are required.");
      return;
    }

    try {
      const resp = await fetch("http://127.0.0.1:8000/api/country/create", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (resp.ok) {
        loadCountries();
        clearCreateForm();
      } else {
        alert("Error creating country.");
      }

    } catch (err) {
      console.error("Create error:", err);
    }
  });
}

function clearCreateForm() {
  document.getElementById("country_abbr").value = "";
  document.getElementById("country_name").value = "";
  document.getElementById("currency_code").value = "";
  document.getElementById("country_status").checked = false;
}

// =========================================================
// 5. EDIT MODAL
// =========================================================
function openEditModal(e) {
  e.preventDefault();

  const abbr = e.target.dataset.abbr;

  fetch(`http://127.0.0.1:8000/api/country/get/${abbr}`, {
    credentials: "include"
  })
    .then(resp => resp.json())
    .then(row => {
      document.getElementById("edit_abbr").value = row.Abbreviation;
      document.getElementById("edit_name").value = row.Name;
      document.getElementById("edit_currency").value = row.CurrencyCode;
      document.getElementById("edit_status").checked = row.Status == 1;

      document.getElementById("editModal").style.display = "block";
    });
}

function setupModalControls() {
  document.getElementById("edit-close-btn").addEventListener("click", () => {
    document.getElementById("editModal").style.display = "none";
  });

  document.getElementById("edit-save-btn").addEventListener("click", saveEdit);
  document.getElementById("edit-delete-btn").addEventListener("click", deleteCountry);
}

async function saveEdit() {
  const payload = {
    Abbreviation: document.getElementById("edit_abbr").value,
    Name: document.getElementById("edit_name").value,
    CurrencyCode: document.getElementById("edit_currency").value,
    Status: document.getElementById("edit_status").checked ? 1 : 0
  };

  const resp = await fetch("http://127.0.0.1:8000/api/country/update", {
    method: "PUT",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (resp.ok) {
    document.getElementById("editModal").style.display = "none";
    loadCountries();
  } else {
    alert("Error updating country.");
  }
}

async function deleteCountry() {
  const abbr = document.getElementById("edit_abbr").value;

  if (!confirm(`Delete country ${abbr}?`)) return;

  const resp = await fetch(`http://127.0.0.1:8000/api/country/delete/${abbr}`, {
    method: "DELETE",
    credentials: "include"
  });

  if (resp.ok) {
    document.getElementById("editModal").style.display = "none";
    loadCountries();
  } else {
    alert("Error deleting country.");
  }
}

// =========================================================
// 6. BULKLOAD
// =========================================================
function setupBulkload() {
  document.querySelectorAll("[data-action]").forEach(btn => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.action;
      const fileInput = document.getElementById("bulk-file");

      if (!fileInput.files.length) {
        alert("Please select a file first.");
        return;
      }

      const formData = new FormData();
      formData.append("file", fileInput.files[0]);
      formData.append("action", action);

      fetch("http://127.0.0.1:8000/api/country/bulkload", {
        method: "POST",
        credentials: "include",
        body: formData
      })
        .then(resp => resp.json())
        .then(result => {
          alert(result.message || "Bulkload complete.");
          loadCountries();
        })
        .catch(err => console.error("Bulkload error:", err));
    });
  });

  document.getElementById("country-upload-btn").addEventListener("click", () => {
  const fileInput = document.getElementById("bulk-file");

  if (!fileInput.files.length) {
    alert("Please select a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("http://127.0.0.1:8000/api/country/bulkload", {
    method: "POST",
    credentials: "include",
    body: formData
  })
    .then(resp => resp.json())
    .then(result => {
      alert(result.message || "Bulkload complete.");
      loadCountries();
    });
});
}