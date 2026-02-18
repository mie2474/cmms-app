async function loadLayout() {
  const body = document.body;

  // Insert sidebar + topbar shell
  body.insertAdjacentHTML("afterbegin", `
    <aside class="sidebar">
      <h1>CMMS</h1>
      <a href="/static/pages/index.html" class="nav-link">Dashboard</a>
      <a href="/static/pages/create-work-order.html" class="nav-link">Work Orders</a>
      <a href="/static/pages/assets.html" class="nav-link">Assets</a>
      <a href="/static/pages/locations.html" class="nav-link">Locations</a>
      <a href="/static/pages/matrix-assignment.html" class="nav-link">Matrix Assignment</a>
      <a href="/static/pages/matrix-problemcode.html" class="nav-link">Problem Codes</a>
      <a href="/static/pages/pm-library.html" class="nav-link">PM Library</a>
      <a href="/static/pages/pm-job.html" class="nav-link">PM Jobs</a>
      <a href="/static/pages/security-group.html" class="nav-link">Security Groups</a>
      <a href="/static/pages/users.html" class="nav-link">Users</a>
    </aside>

    <div class="main">
      <header class="topbar">
        <div id="pageTitle">CMMS</div>
        <div id="userBox">Loading user...</div>
      </header>

      <main class="content" id="pageContent"></main>
    </div>
  `);
}
