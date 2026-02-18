function attachLayout() {
  const displayName =
    window.currentUser?.name ||
    window.currentUser?.preferred_username ||
    window.currentUser?.email ||
    "User";

  /* ---------- HEADER ---------- */
//   document.getElementById("header").innerHTML = `
//     <div class="topbar">
//       <div style="font-weight:600;">CMMS</div>
//       <div>${displayName}</div>
//     </div>
//   `;

  /* ---------- SIDEBAR ---------- */
//   document.getElementById("sidebar").innerHTML = `
//     <h1>CMMS</h1>

//     <a class="nav-link" href="/">Dashboard</a>
//     <a class="nav-link" href="/static/pages/create-work-order.html">Work Orders</a>
//     <a class="nav-link" href="/static/pages/create-work-order.html">Create Work Order</a>
//     <a class="nav-link" href="/static/pages/pm-library.html">PM Library</a>
//     <a class="nav-link" href="/static/pages/assets.html">Assets</a>

//     <div class="location-menu">
//         <button class="nav-link" id="locationsLink" type="button">
//             Locations ▾
//         </button>
//         <div id="locationsBox" class="floating-box">
//             <a href="/static/pages/locations/country.html">Country</a>
//             <a href="/static/pages/locations/state.html">State / Province</a>
//             <a href="/static/pages/location-l1.html">Level 1</a>
//             <a href="/static/pages/location-l2.html">Level 2</a>
//             <a href="/static/pages/location-l3.html">Level 3</a>
//             <a href="/static/pages/location-l4.html">Level 4</a>
//         </div>
//     </div>
//     <a class="nav-link" href="/static/pages/matrix-assignments.html">Matrix Assignments</a>
//     <a class="nav-link" href="/static/pages/users.html">Users</a>
//     <a class="nav-link" href="/static/pages/security-groups.html">Security Groups</a>
//     <a class="nav-link" href="/static/pages/prioritycodes.html">Priority Codes</a>
//     <a class="nav-link" href="/static/pages/problemcodes.html">Problem Codes</a>
//     <a class="nav-link active" href="/static/pages/matrix-problemcodes.html">Matrix Problem Codes</a>
//   `;

  /* ---------- Floating toggle for location---------- */
  const link = document.getElementById("locationsLink");
  const box = document.getElementById("locationsBox");

  if (link && box) {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      box.classList.toggle("open");
    });

    document.addEventListener("click", (e) => {
      if (!box.contains(e.target) && !link.contains(e.target)) {
        box.classList.remove("open");
      }
    });
  }

   /* ---------- Floating toggle for Matrix---------- */
  const mLink = document.getElementById("matrixLink");
  const mBox = document.getElementById("matrixBox");

  if (mLink && mBox) {
    mLink.addEventListener("click", (e) => {
      e.preventDefault();
      mBox.classList.toggle("open");
    });

    document.addEventListener("click", (e) => {
      if (!mBox.contains(e.target) && !mLink.contains(e.target)) {
        mBox.classList.remove("open");
      }
    });
  }
}

