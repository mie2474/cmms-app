
async function requireAuth() {
  try {
    const resp = await fetch("http://127.0.0.1:8000/me", {
      credentials: "include"
    });

    if (!resp.ok) {
      window.location.href = "http://127.0.0.1:8000/login";
      return;
    }

    const user = await resp.json()
    window.currentUser = user;
    return user;

  } catch (err) {
    window.location.href = "http://127.0.0.1:8000/login";
  }
}

// function attachLayout() {
//   const displayName =
//     window.currentUser?.name ||
//     window.currentUser?.preferred_username ||
//     window.currentUser?.email ||
//     "User";

//   document.getElementById("header").innerHTML = `
//     <div class="header">
//       <h1>CMMS</h1>
//       <div class="user-info">${displayName}</div>
//     </div>
//   `;

  // document.getElementById("sidebar").innerHTML = `
  //   <ul>
  //     <li><a href="http://127.0.0.1:8000/">Dashboard</a></li>
  //     <li><a href="http://127.0.0.1:8000/static/pages/create-work-order.html">Work Orders</a></li>
  //     <li><a href="http://127.0.0.1:8000/static/pages/assets.html">Assets</a></li>
  //     <li><a href="http://127.0.0.1:8000/static/pages/inventory.html">Inventory</a></li>
  //     <li><a href="http://127.0.0.1:8000/static/pages/vendors.html">Vendors</a></li>
  //   </ul>
  // `;

//   document.getElementById("footer").innerHTML = `<p>© 2026 CMMS</p>`;
// }
