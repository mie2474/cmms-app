// -------------------------------
// INITIAL LOAD
// -------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadLevel1List();
    loadLevel2List();
    loadLevel3List();
    loadLevel4List();
});

// -------------------------------
// API HELPERS
// -------------------------------
async function apiGet(url) {
    const res = await fetch(url);
    return res.json();
}

async function apiPost(url, data) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return res.json();
}

// -------------------------------
// LEVEL 1 – REGION
// -------------------------------
async function saveLevel1() {
    const payload = {
        region_number: Number(document.getElementById("l1-region-number").value),
        description: document.getElementById("l1-description").value,
        date_opened: document.getElementById("l1-date-opened").value || null
    };

    await apiPost("/api/locations/level1", payload);
    alert("Region saved");
    loadLevel1List();
}

async function loadLevel1List() {
    const regions = await apiGet("/api/locations/level1");

    const select = document.getElementById("l2-region-select");
    if (!select) return;

    select.innerHTML = `<option value="">Select Region</option>`;
    regions.forEach(r => {
        select.innerHTML += `<option value="${r.id}">${r.description}</option>`;
    });
}

// -------------------------------
// LEVEL 2 – BUILDING
// -------------------------------
async function saveLevel2() {
    const payload = {
        level1_id: Number(document.getElementById("l2-region-select").value),
        division_number: Number(document.getElementById("l2-division-number").value),
        building_name: document.getElementById("l2-building-name").value,
        address: document.getElementById("l2-address").value,
        scity: document.getElementById("l2-scity").value,
        state: document.getElementById("l2-state").value,
        postal_code: document.getElementById("l2-postal").value
    };

    await apiPost("/api/locations/level2", payload);
    alert("Building saved");
    loadLevel2List();
}

async function loadLevel2List() {
    const buildings = await apiGet("/api/locations/level2");

    const select = document.getElementById("l3-building-select");
    if (!select) return;

    select.innerHTML = `<option value="">Select Building</option>`;
    buildings.forEach(b => {
        select.innerHTML += `<option value="${b.id}">${b.building_name}</option>`;
    });
}

// -------------------------------
// LEVEL 3 – FLOOR
// -------------------------------
async function saveLevel3() {
    const level2_id = Number(document.getElementById("l3-building-select").value);
    const district_number = document.getElementById("l3-district-number").value;
    const description = document.getElementById("l3-description").value;

    if (!level2_id) return alert("Please select a building.");
    if (!district_number) return alert("District number is required.");
    if (!description) return alert("Floor description is required.");

    const payload = {
        level2_id,
        district_number: Number(district_number),
        description,
        date_opened: document.getElementById("l3-date-opened").value || null,
        date_closed: document.getElementById("l3-date-closed").value || null
    };

    await apiPost("/api/locations/level3", payload);
    alert("Floor saved");

    loadLevel3List();
    loadFloorsForBuilding();
}

async function loadLevel3List() {
    const floors = await apiGet("/api/locations/level3");

    const select = document.getElementById("l4-floor-select");
    if (!select) return;

    select.innerHTML = `<option value="">Select Floor</option>`;
    floors.forEach(f => {
        select.innerHTML += `<option value="${f.id}">${f.description}</option>`;
    });
}

document.getElementById("l3-building-select").addEventListener("change", () => {
    loadFloorsForBuilding();
});

async function loadFloorsForBuilding() {
    const buildingId = Number(document.getElementById("l3-building-select").value);
    if (!buildingId) return;

    const floors = await apiGet(`/api/locations/level3?building_id=${buildingId}`);

    const select = document.getElementById("l4-floor-select");
    select.innerHTML = `<option value="">Select Floor</option>`;

    floors.forEach(f => {
        select.innerHTML += `<option value="${f.id}">${f.description}</option>`;
    });
}

// -------------------------------
// LEVEL 4 – ROOM
// -------------------------------
async function saveLevel4() {
    const payload = {
        level3_id: Number(document.getElementById("l4-floor-select").value),
        customer_site: document.getElementById("l4-customer-site").value,
        customer_site_number: Number(document.getElementById("l4-customer-site-number").value),
        room_desc: document.getElementById("l4-room-desc").value,
        ship_address: document.getElementById("l4-ship-address").value,
        ship_city: document.getElementById("l4-ship-city").value,
        ship_state: document.getElementById("l4-ship-state").value,
        ship_postal: document.getElementById("l4-ship-postal").value,
        ship_country: document.getElementById("l4-ship-country").value
    };

    await apiPost("/api/locations/level4", payload);
    alert("Room saved");
    loadLevel4List();
}

async function loadLevel4List() {
    const rooms = await apiGet("/api/locations/level4");

    const table = document.querySelector("#l4-room-table tbody");
    if (!table) return;

    table.innerHTML = "";
    rooms.forEach(r => {
        table.innerHTML += `
            <tr>
                <td>${r.region_number}</td>
                <td>${r.building_name}</td>
                <td>${r.floor_description}</td>
                <td>${r.room_desc}</td>
                <td>${r.customer_site}</td>
                <td>${r.customer_site_number}</td>
            </tr>
        `;
    });
}

document.getElementById("l4-floor-select").addEventListener("change", () => {
    loadRoomsForFloor();
});

async function loadRoomsForFloor() {
    const floorId = Number(document.getElementById("l4-floor-select").value);
    if (!floorId) return;

    const rooms = await apiGet(`/api/locations/level4?floor_id=${floorId}`);

    const table = document.querySelector("#l4-room-table tbody");
    table.innerHTML = "";

    rooms.forEach(r => {
        table.innerHTML += `
            <tr>
                <td>${r.region_number}</td>
                <td>${r.building_name}</td>
                <td>${r.floor_description}</td>
                <td>${r.room_desc}</td>
                <td>${r.customer_site}</td>
                <td>${r.customer_site_number}</td>
            </tr>
        `;
    });
}

// -------------------------------
// BULK UPLOAD HELPERS
// -------------------------------
async function uploadExcelToEndpoint(file, url) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(url, {
        method: "POST",
        body: formData
    });

    if (!res.ok) {
        const text = await res.text();
        alert("Bulk load failed: " + text);
        return null;
    }

    return await res.json();
}

// -------------------------------
// LEVEL 1 BULK
// -------------------------------
document.getElementById("bulk-l1-upload-btn").addEventListener("click", () => {
    document.getElementById("bulk-l1-file").click();
});

document.getElementById("bulk-l1-file").addEventListener("change", async () => {
    const file = document.getElementById("bulk-l1-file").files[0];
    if (!file) return;

    const result = await uploadExcelToEndpoint(file, "/api/locations/bulk/level1");
    if (result) {
        alert("Level 1 bulk load complete: " + result.rows_processed + " rows");
        document.getElementById("bulk-l1-file").value = "";
        loadLevel1List();
    }
});

// -------------------------------
// LEVEL 2 BULK
// -------------------------------
document.getElementById("bulk-l2-upload-btn").addEventListener("click", () => {
    document.getElementById("bulk-l2-file").click();
});

document.getElementById("bulk-l2-file").addEventListener("change", async () => {
    const file = document.getElementById("bulk-l2-file").files[0];
    if (!file) return;

    const result = await uploadExcelToEndpoint(file, "/api/locations/bulk/level2");
    if (result) {
        alert("Level 2 bulk load complete: " + result.rows_processed + " rows");
        document.getElementById("bulk-l2-file").value = "";
        loadLevel2List();
    }
});

// -------------------------------
// LEVEL 3 BULK
// -------------------------------
document.getElementById("bulk-l3-upload-btn").addEventListener("click", () => {
    document.getElementById("bulk-l3-file").click();
});

document.getElementById("bulk-l3-file").addEventListener("change", async () => {
    const file = document.getElementById("bulk-l3-file").files[0];
    if (!file) return;

    const result = await uploadExcelToEndpoint(file, "/api/locations/bulk/level3");
    if (result) {
        alert("Level 3 bulk load complete: " + result.rows_processed + " rows");
        document.getElementById("bulk-l3-file").value = "";
        loadLevel3List();
    }
});

// -------------------------------
// LEVEL 4 BULK
// -------------------------------
document.getElementById("bulk-l4-upload-btn").addEventListener("click", () => {
    document.getElementById("bulk-l4-file").click();
});

document.getElementById("bulk-l4-file").addEventListener("change", async () => {
    const file = document.getElementById("bulk-l4-file").files[0];
    if (!file) return;

    const result = await uploadExcelToEndpoint(file, "/api/locations/bulk/level4");
    if (result) {
        alert("Level 4 bulk load complete: " + result.rows_processed + " rows");
        document.getElementById("bulk-l4-file").value = "";
        loadLevel4List();
    }
});

// ---------- TEMPLATE DOWNLOADS ----------
const l1TemplateBtn = document.getElementById("l1-template-btn");
if (l1TemplateBtn) {
  l1TemplateBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/template/l1";
  });
}

const l2TemplateBtn = document.getElementById("l2-template-btn");
if (l2TemplateBtn) {
  l2TemplateBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/template/l2";
  });
}

const l3TemplateBtn = document.getElementById("l3-template-btn");
if (l3TemplateBtn) {
  l3TemplateBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/template/l3";
  });
}

const l4TemplateBtn = document.getElementById("l4-template-btn");
if (l4TemplateBtn) {
  l4TemplateBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/template/l4";
  });
}


// ---------- DATA DOWNLOADS ----------
const l1DataBtn = document.getElementById("l1-data-btn");
if (l1DataBtn) {
  l1DataBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/data/l1";
  });
}

const l2DataBtn = document.getElementById("l2-data-btn");
if (l2DataBtn) {
  l2DataBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/data/l2";
  });
}

const l3DataBtn = document.getElementById("l3-data-btn");
if (l3DataBtn) {
  l3DataBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/data/l3";
  });
}

const l4DataBtn = document.getElementById("l4-data-btn");
if (l4DataBtn) {
  l4DataBtn.addEventListener("click", () => {
    window.location.href = "/api/locations/data/l4";
  });
}


// -------------------------------
// SAVE BUTTON LISTENERS
// -------------------------------
document.getElementById("l1-save-btn").addEventListener("click", saveLevel1);
document.getElementById("l2-save-btn").addEventListener("click", saveLevel2);
document.getElementById("l3-save-btn").addEventListener("click", saveLevel3);
document.getElementById("l4-save-btn").addEventListener("click", saveLevel4);
