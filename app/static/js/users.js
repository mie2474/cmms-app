async function loadUsers() {
  const data = await apiGet("/users");
  const tbody = document.querySelector("#userTable tbody");
  tbody.innerHTML = "";
  data.forEach(u => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${u.email}</td>
      <td>${u.name || ""}</td>
      <td>${u.role || ""}</td>
    `;
    tbody.appendChild(tr);
  });
}

function initUsers() {
  const form = document.getElementById("userForm");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      email: document.getElementById("user-email").value,
      name: document.getElementById("user-name").value || null,
      role: document.getElementById("user-role").value || null
    };
    await apiPost("/users/", payload);
    form.reset();
    loadUsers();
  });

  loadUsers();
}
