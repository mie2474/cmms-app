const API_BASE = "http://localhost:8000";

function getHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("token")
    };
}

function toggleForm() {
    const form = document.getElementById("formContainer");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

// =============================
// LOAD DROPDOWNS
// =============================

async function loadDropdowns() {
    await loadAssets();
    await loadPriorities();
    await loadProblemCodes();
}

async function loadAssets() {
    const response = await fetch(`${API_BASE}/assets/`, {
        headers: getHeaders()
    });

    const select = document.getElementById("woAsset");
    select.innerHTML = "";

    if (!response.ok) return;

    const data = await response.json();

    data.forEach(asset => {
        select.innerHTML += `
            <option value="${asset.id}">
                ${asset.name} (${asset.asset_tag})
            </option>
        `;
    });
}

async function loadPriorities() {
    const response = await fetch(`${API_BASE}/prioritycodes/`, {
        headers: getHeaders()
    });

    const select = document.getElementById("woPriority");
    select.innerHTML = "";

    if (!response.ok) return;

    const data = await response.json();

    data.forEach(priority => {
        select.innerHTML += `
            <option value="${priority.id}">
                ${priority.name}
            </option>
        `;
    });
}

async function loadProblemCodes() {
    const response = await fetch(`${API_BASE}/problemcodes/`, {
        headers: getHeaders()
    });

    const select = document.getElementById("woProblemCode");
    select.innerHTML = "";

    if (!response.ok) return;

    const data = await response.json();

    data.forEach(problem => {
        select.innerHTML += `
            <option value="${problem.id}">
                ${problem.name}
            </option>
        `;
    });
}

// =============================
// LOAD WORK ORDERS
// =============================

async function loadWorkOrders() {
    const response = await fetch(`${API_BASE}/workorders/`, {
        headers: getHeaders()
    });

    if (!response.ok) {
        const error = await response.json();
        alert("Error: " + error.detail);
        return;
    }

    const data = await response.json();
    const table = document.getElementById("woTable");
    table.innerHTML = "";

    data.forEach(wo => {
        table.innerHTML += `
            <tr>
                <td>${wo.id}</td>
                <td>${wo.title}</td>
                <td>${wo.status}</td>
                <td>${wo.asset_id}</td>
                <td>${wo.priority_id}</td>
                <td>${wo.problem_code_id}</td>
                <td>${wo.assigned_to ?? "-"}</td>
                <td>${wo.created_by}</td>
                <td>${new Date(wo.created_at).toLocaleString()}</td>
            </tr>
        `;
    });
}

// =============================
// CREATE WORK ORDER
// =============================

async function createWorkOrder() {

    const payload = {
        title: document.getElementById("woTitle").value,
        description: document.getElementById("woDescription").value,
        asset_id: parseInt(document.getElementById("woAsset").value),
        priority_id: parseInt(document.getElementById("woPriority").value),
        problem_code_id: parseInt(document.getElementById("woProblemCode").value)
    };

    const response = await fetch(`${API_BASE}/workorders/`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const error = await response.json();
        alert("Error: " + error.detail);
        return;
    }

    document.getElementById("formContainer").style.display = "none";
    loadWorkOrders();
}

// =============================
// INIT
// =============================

window.onload = async function() {
    await loadDropdowns();
    await loadWorkOrders();
};
