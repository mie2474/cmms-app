// async function loadAssets() {
//   const data = await apiGet("/assets");
//   const tbody = document.querySelector("#assetTable tbody");
//   tbody.innerHTML = "";
//   data.forEach(a => {
//     const tr = document.createElement("tr");
//     tr.innerHTML = `
//       <td>${a.name}</td>
//       <td>${a.code || ""}</td>
//       <td>${a.location_id || ""}</td>
//       <td>${a.category || ""}</td>
//       <td>${a.status || ""}</td>
//     `;
//     tbody.appendChild(tr);
//   });
// }

// function initAssets() {
//   const form = document.getElementById("assetForm");
//   form.addEventListener("submit", async (e) => {
//     e.preventDefault();
//     const payload = {
//       name: document.getElementById("asset-name").value,
//       code: document.getElementById("asset-code").value || null,
//       location_id: document.getElementById("asset-location").value || null,
//       category: document.getElementById("asset-category").value || null,
//       status: document.getElementById("asset-status").value || null
//     };
//     await apiPost("/assets/", payload);
//     form.reset();
//     loadAssets();
//   });

//   loadAssets();
// }
async function loadAssets() {
    const response = await fetch(`${API_BASE}/assets/`, {
        headers: getAuthHeaders()
    });

    const data = await response.json();
    const table = document.getElementById("assetTable");

    table.innerHTML = "";

    data.forEach(asset => {
        table.innerHTML += `
            <tr>
                <td>${asset.id}</td>
                <td>${asset.name}</td>
                <td>${asset.asset_tag}</td>
                <td>${asset.status}</td>
            </tr>
        `;
    });
}
