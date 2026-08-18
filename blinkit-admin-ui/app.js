// ============================================================
// DOM HELPERS
// ============================================================

const $ = (q, s = document) => s.querySelector(q);
const $$ = (q, s = document) => [...s.querySelectorAll(q)];


// ============================================================
// GLOBAL STATE
// ============================================================

const state = {
  base:
    sessionStorage.getItem("blink_base") ||
    "http://127.0.0.1:8000",

  access:
    sessionStorage.getItem("blink_access") ||
    "",

  refresh:
    sessionStorage.getItem("blink_refresh") ||
    "",

  user: JSON.parse(
    sessionStorage.getItem("blink_user") || "null"
  ),

  spec: null,

  page: "overview",

  data: {},

  // Related API data cache
  // e.g. brands, products, branches, managers etc.
  relations: {},

  modal: null,
};


// ============================================================
// ICONS
// ============================================================

const icons = {
  overview: "⌂",
  branches: "⌘",
  managers: "♙",
  brands: "◆",
  categories: "▦",
  products: "◫",
  variants: "≋",
  images: "▧",
  inventory: "▥",
  customers: "♧",
  catalog: "⊞",
  console: "⌁",
  profile: "◎",
};


// ============================================================
// NAVIGATION
// ============================================================

const navGroups = [
  [
    "Workspace",
    [
      ["overview", "Overview"],
      ["branches", "Branches"],
      ["inventory", "Branch Inventory"],
      ["catalog", "Branch Catalog"],
    ],
  ],

  [
    "Catalog",
    [
      ["brands", "Brands"],
      ["categories", "Categories & Subcategories"],
      ["products", "Products"],
      ["variants", "Product Variants"],
      ["images", "Product Images"],
    ],
  ],

  [
    "People",
    [
      ["managers", "Branch Managers"],
      ["customers", "Customers"],
    ],
  ],

  [
    "System",
    [
      ["profile", "Admin Profile"],
      ["console", "API Console"],
    ],
  ],
];


// ============================================================
// CRUD MODULE CONFIG
// ============================================================

const modules = {
  branches: {
    title: "Branches",
    list: "/branches/",
    create: "/branches/create",
    createSchema: "BranchCreate",
    updateSchema: "BranchUpdate",
    id: "unique_id",

    cols: [
      "name",
      "city",
      "pincode",
      "is_active",
      "created_at",
    ],
  },

  managers: {
    title: "Branch Managers",
    list: "/branch-managers/all",
    create: "/branch-managers/create",
    createSchema: "BranchManagerCreate",
    updateSchema: "BranchManagerUpdate",
    base: "/branch-managers",
    id: "unique_id",

    cols: [
      "name",
      "email",
      "role",
      "is_active",
      "created_at",
    ],
  },

  brands: {
    title: "Brands",
    list: "/brands",
    create: "/brands",
    createSchema: "BrandCreate",
    updateSchema: "BrandUpdate",
    base: "/brands",
    id: "unique_id",

    cols: [
      "name",
      "slug",
      "is_active",
      "created_at",
    ],

    activatable: true,
  },

  products: {
    title: "Products",
    list: "/products",
    create: "/products",
    createSchema: "ProductCreate",
    updateSchema: "ProductUpdate",
    base: "/products",
    id: "unique_id",

    cols: [
      "name",
      "slug",
      "is_active",
      "created_at",
    ],

    activatable: true,
  },

  variants: {
    title: "Product Variants",
    list: "/product-variants",
    create: "/product-variants",
    createSchema: "ProductVariantCreate",
    updateSchema: "ProductVariantUpdate",
    base: "/product-variants",
    id: "unique_id",

    cols: [
      "sku",
      "value",
      "unit",
      "mrp",
      "selling_price",
      "is_active",
    ],

    activatable: true,
  },

  images: {
    title: "Product Images",
    list: null,
    create: "/product-images",
    createSchema: "ProductImageCreate",
    updateSchema: "ProductImageUpdate",
    base: "/product-images",
    id: "unique_id",

    cols: [
      "image_url",
      "sort_order",
      "is_primary",
      "created_at",
    ],
  },

  customers: {
    title: "Customers",
    list: "/customers",
    create: null,
    updateSchema: "CustomerUpdate",
    base: "/customers",
    id: "unique_id",

    cols: [
      "name",
      "email",
      "phone",
      "is_active",
      "created_at",
    ],

    activatable: true,
  },
};


// ============================================================
// RELATION CONFIG
//
// IMPORTANT:
// agar form me ye fields aaye,
// raw UUID input ki jagah GET API call karke dropdown banega.
// ============================================================

const relationConfig = {
  brand_unique_id: {
    cache: "brands",
    path: "/brands/active",
    placeholder: "Choose brand",
    label: (x) =>
      x.slug
        ? `${x.name} — ${x.slug}`
        : x.name,
  },

  category_unique_id: {
    cache: "categories",
    path: "/categories/active",
    placeholder: "Choose category",
    label: (x) =>
      x.slug
        ? `${x.name} — ${x.slug}`
        : x.name,
  },

  subcategory_unique_id: {
    cache: "subcategories",
    path: "/subcategories/active",
    placeholder: "Choose subcategory",
    label: (x) =>
      x.slug
        ? `${x.name} — ${x.slug}`
        : x.name,
  },

  product_unique_id: {
    cache: "products",
    path: "/products/active",
    placeholder: "Choose product",
    label: (x) =>
      x.slug
        ? `${x.name} — ${x.slug}`
        : x.name,
  },

  product_variant_unique_id: {
    cache: "variants",
    path: "/product-variants",
    placeholder: "Choose product variant",

    label: (x) => {
      const size = [
        x.value,
        x.unit,
      ]
        .filter(Boolean)
        .join(" ");

      return [
        x.sku,
        size,
        x.selling_price
          ? `₹${x.selling_price}`
          : "",
      ]
        .filter(Boolean)
        .join(" — ");
    },
  },

  branch_unique_id: {
    cache: "branches",
    path: "/branches/",
    placeholder: "Choose branch",

    label: (x) =>
      [
        x.name,
        x.city,
        x.pincode,
      ]
        .filter(Boolean)
        .join(" — "),
  },

  manager_unique_id: {
    cache: "managers",
    path: "/branch-managers/all",
    placeholder: "Choose branch manager",

    label: (x) => {
      const assignedBranch =
        x.branch?.name
          ? ` • ${x.branch.name}`
          : "";

      return `${x.name} — ${x.email}${assignedBranch}`;
    },
  },
};


// ============================================================
// BASIC HELPERS
// ============================================================

function escapeHtml(v) {
  return String(v ?? "").replace(
    /[&<>'"]/g,
    (c) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "'": "&#39;",
        '"': "&quot;",
      })[c]
  );
}


function getRole() {
  return (
    state.user?.role ||
    jwtPayload(state.access)?.role ||
    jwtPayload(state.access)?.user_role ||
    "authenticated"
  ).toLowerCase();
}


function isAdmin() {
  return [
    "admin",
    "super_admin",
    "superadmin",
  ].includes(getRole());
}


function jwtPayload(token) {
  try {
    const payload = token
      .split(".")[1]
      .replace(/-/g, "+")
      .replace(/_/g, "/");

    return JSON.parse(atob(payload));
  } catch {
    return {};
  }
}


function saveSession() {
  sessionStorage.setItem(
    "blink_base",
    state.base
  );

  sessionStorage.setItem(
    "blink_access",
    state.access
  );

  sessionStorage.setItem(
    "blink_refresh",
    state.refresh
  );

  sessionStorage.setItem(
    "blink_user",
    JSON.stringify(state.user || null)
  );
}


function toast(
  title,
  msg = "",
  type = ""
) {
  const e = document.createElement("div");

  e.className = "toast " + type;

  e.innerHTML = `
    <div>
      ${type === "error" ? "!" : "✓"}
    </div>

    <div>
      <b>${escapeHtml(title)}</b>
      <span>${escapeHtml(msg)}</span>
    </div>
  `;

  $("#toast-root").append(e);

  setTimeout(
    () => e.remove(),
    4000
  );
}


// ============================================================
// API HELPER
// ============================================================

async function api(
  path,
  opts = {},
  retry = true
) {
  const headers = {
    "Content-Type": "application/json",
    ...(opts.headers || {}),
  };

  if (state.access) {
    headers.Authorization =
      `Bearer ${state.access}`;
  }

  let response;

  try {
    response = await fetch(
      state.base.replace(/\/$/, "") + path,
      {
        ...opts,
        headers,
      }
    );
  } catch (e) {
    throw Object.assign(
      new Error(
        "Network error. Check API URL / CORS / backend status."
      ),
      {
        status: 0,
      }
    );
  }


  // -----------------------------------------
  // Refresh access token
  // -----------------------------------------

  if (
    response.status === 401 &&
    retry &&
    state.refresh &&
    path !== "/auth/refresh"
  ) {
    try {
      const rr = await fetch(
        state.base.replace(/\/$/, "") +
          "/auth/refresh",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            refresh_token:
              state.refresh,
          }),
        }
      );

      if (rr.ok) {
        const x = await rr.json();

        state.access =
          x.access_token;

        if (x.refresh_token) {
          state.refresh =
            x.refresh_token;
        }

        saveSession();

        return api(
          path,
          opts,
          false
        );
      }
    } catch {}
  }


  let body = null;

  const text =
    await response.text();

  try {
    body = text
      ? JSON.parse(text)
      : null;
  } catch {
    body = text;
  }


  if (!response.ok) {
    const detail =
      typeof body === "object"
        ? (
            body?.detail ||
            body?.message ||
            JSON.stringify(body)
          )
        : body;

    throw Object.assign(
      new Error(
        detail ||
        `HTTP ${response.status}`
      ),
      {
        status:
          response.status,

        body,
      }
    );
  }

  return body;
}


// ============================================================
// OPENAPI
// ============================================================

async function loadSpec() {
  if (state.spec) {
    return state.spec;
  }

  const response =
    await fetch("openapi.json");

  state.spec =
    await response.json();

  return state.spec;
}


// ============================================================
// RELATION LOADER
// ============================================================

async function loadRelation(
  fieldName,
  force = false
) {
  const config =
    relationConfig[fieldName];

  if (!config) {
    return [];
  }

  if (
    !force &&
    Array.isArray(
      state.relations[config.cache]
    )
  ) {
    return state.relations[
      config.cache
    ];
  }

  try {
    const rows =
      await api(config.path);

    state.relations[
      config.cache
    ] = Array.isArray(rows)
      ? rows
      : [];

    return state.relations[
      config.cache
    ];
  } catch (err) {
    console.warn(
      `Could not load relation ${fieldName}`,
      err
    );

    return [];
  }
}


// ============================================================
// LOAD RELATIONS REQUIRED BY A SCHEMA
// ============================================================

async function prepareRelationsForSchema(
  schemaName
) {
  const s =
    schema(schemaName);

  const fields =
    Object.keys(
      s.properties || {}
    );

  const relationFields =
    fields.filter(
      (field) =>
        relationConfig[field]
    );

  await Promise.all(
    relationFields.map(
      (field) =>
        loadRelation(field)
    )
  );
}


// ============================================================
// LOGIN
// ============================================================

async function login(e) {
  e.preventDefault();

  state.base =
    $("#base-url")
      .value
      .trim()
      .replace(/\/$/, "");

  try {
    const result =
      await api(
        "/auth/login",
        {
          method: "POST",

          body: JSON.stringify({
            email:
              $("#login-email")
                .value
                .trim(),

            password:
              $("#login-password")
                .value,
          }),
        },
        false
      );

    state.access =
      result.access_token;

    state.refresh =
      result.refresh_token;

    state.user =
      jwtPayload(
        state.access
      );


    // Try admin profile
    try {
      state.user =
        await api(
          "/admin/get"
        );
    } catch (err) {
      if (
        err.status !== 401 &&
        err.status !== 403
      ) {
        console.warn(err);
      }
    }

    saveSession();

    await showApp();

    toast(
      "Signed in",
      `Session started as ${getRole().replaceAll("_", " ")}`
    );
  } catch (err) {
    toast(
      "Login failed",
      err.message,
      "error"
    );
  }
}


// ============================================================
// SHOW APP
// ============================================================

async function showApp() {
  await loadSpec();

  $("#login-view")
    .classList
    .add("hidden");

  $("#app-view")
    .classList
    .remove("hidden");

  $("#api-host")
    .textContent =
    state.base;

  setUserUI();

  renderNav();

  navigate("overview");
}


// ============================================================
// USER UI
// ============================================================

function setUserUI() {
  const profile =
    state.user ||
    jwtPayload(
      state.access
    );

  const email =
    profile?.email ||
    profile?.sub ||
    "Account";

  const name =
    profile?.name ||
    email.split("@")[0] ||
    "Account";

  $("#user-name")
    .textContent =
    name;

  $("#user-role")
    .textContent =
    getRole()
      .replaceAll(
        "_",
        " "
      );

  $("#avatar")
    .textContent =
    name[0]
      ?.toUpperCase() ||
    "A";
}


// ============================================================
// SIDEBAR
// ============================================================

function renderNav() {
  let html = "";

  for (
    const [label, items]
    of navGroups
  ) {
    html += `
      <div class="nav-label">
        ${label}
      </div>
    `;

    for (
      const [id, name]
      of items
    ) {
      const adminOnly =
        [
          "managers",
          "profile",
        ].includes(id);

      html += `
        <button
          class="nav-item"
          data-nav="${id}"
        >
          <span class="nav-icon">
            ${icons[id]}
          </span>

          ${name}

          ${
            adminOnly &&
            !isAdmin()
              ? `
                <span class="nav-badge">
                  Admin
                </span>
              `
              : ""
          }
        </button>
      `;
    }
  }

  $("#nav")
    .innerHTML =
    html;

  $$("[data-nav]")
    .forEach(
      (button) => {
        button.onclick =
          () =>
            navigate(
              button.dataset.nav
            );
      }
    );
}


// ============================================================
// NAVIGATE
// ============================================================

async function navigate(page) {
  state.page = page;

  $$(".nav-item")
    .forEach(
      (x) =>
        x.classList.toggle(
          "active",
          x.dataset.nav === page
        )
    );


  const names = {
    overview:
      "Operations overview",

    categories:
      "Categories & subcategories",

    inventory:
      "Branch inventory",

    catalog:
      "Branch catalog",

    console:
      "API console",

    profile:
      "Admin profile",
  };


  $("#page-title")
    .textContent =
    names[page] ||
    modules[page]?.title ||
    page;


  $("#crumb")
    .textContent =
    page === "overview"
      ? "Workspace"
      : (
          Object.keys(
            modules
          ).includes(page)
            ? "Management"
            : "Workspace"
        );


  $("#content")
    .innerHTML = `
      <div class="panel">
        <div class="panel-body">
          <div
            class="skeleton"
            style="width:35%"
          ></div>

          <br>

          <div
            class="skeleton"
          ></div>

          <br>

          <div
            class="skeleton"
            style="width:78%"
          ></div>
        </div>
      </div>
    `;


  try {
    if (
      page === "overview"
    ) {
      await renderOverview();
    }

    else if (
      page === "categories"
    ) {
      await renderCategories();
    }

    else if (
      page === "inventory"
    ) {
      await renderInventory();
    }

    else if (
      page === "catalog"
    ) {
      await renderCatalog();
    }

    else if (
      page === "console"
    ) {
      await renderConsole();
    }

    else if (
      page === "profile"
    ) {
      await renderProfile();
    }

    else {
      await renderCrud(page);
    }

  } catch (err) {
    handlePageError(err);
  }
}


// ============================================================
// ERRORS
// ============================================================

function handlePageError(err) {
  if (
    [401, 403]
      .includes(
        err.status
      )
  ) {
    return renderUnauthorized(
      err
    );
  }

  $("#content")
    .innerHTML = `
      <div class="panel">
        <div class="empty">

          <div class="big">
            ⚠
          </div>

          <b>
            Could not load this page
          </b>

          <p>
            ${escapeHtml(
              err.message
            )}
          </p>

          <button
            class="secondary-btn"
            onclick="navigate(state.page)"
          >
            Try again
          </button>

        </div>
      </div>
    `;
}


function renderUnauthorized(err) {
  $("#content")
    .innerHTML = `
      <div class="unauthorized">
        <div>

          <div class="lock">
            ⌾
          </div>

          <h3>
            Unauthorized access
          </h3>

          <p>
            Your
            ${escapeHtml(
              getRole()
                .replaceAll(
                  "_",
                  " "
                )
            )}
            account does not
            have permission for
            this protected
            operation.

            The backend returned
            HTTP ${err.status}.
          </p>

          <button
            class="secondary-btn"
            onclick="navigate('overview')"
          >
            Back to overview
          </button>

        </div>
      </div>
    `;
}


// ============================================================
// OVERVIEW
// ============================================================

async function safeCount(path) {
  try {
    const result =
      await api(path);

    return Array.isArray(
      result
    )
      ? result.length
      : result
        ? 1
        : 0;

  } catch {
    return "—";
  }
}


async function renderOverview() {
  const [
    branches,
    products,
    customers,
    inventory,
  ] = await Promise.all([
    safeCount("/branches/"),
    safeCount("/products"),
    safeCount("/customers"),
    safeCount("/inventory"),
  ]);


  $("#content")
    .innerHTML = `
      <div class="hero-panel">

        <div>

          <span class="eyebrow">
            ${
              isAdmin()
                ? "ADMIN CONTROL CENTER"
                : "BRANCH MANAGER WORKSPACE"
            }
          </span>

          <h3>
            Good to see you,
            ${escapeHtml(
              (
                state.user?.name ||
                "operator"
              )
                .split(" ")[0]
            )}.
          </h3>

          <p>
            Live controls backed by
            your protected Blinkit
            Clone APIs.
          </p>

        </div>

        <div class="hero-actions">

          <button
            class="secondary-btn"
            onclick="navigate('console')"
          >
            Open API console
          </button>

          <button
            class="primary-btn"
            onclick="navigate('branches')"
          >
            Manage branches
          </button>

        </div>

      </div>


      <div class="stat-grid">

        ${stat(
          "⌘",
          "Branches",
          branches,
          "Network locations"
        )}

        ${stat(
          "◫",
          "Products",
          products,
          "Master catalog"
        )}

        ${stat(
          "♧",
          "Customers",
          customers,
          "Registered users"
        )}

        ${stat(
          "▥",
          "Inventory",
          inventory,
          "Branch stock rows"
        )}

      </div>


      <div class="grid-2">

        <div class="panel">

          <div class="panel-head">
            <div>
              <h3>
                Operations map
              </h3>

              <p>
                Core backend areas
                available in this
                console
              </p>
            </div>
          </div>


          <div class="panel-body">

            <div class="quick-grid">

              ${quick(
                "branches",
                "⌘",
                "Branch operations",
                "Create, edit, assign manager"
              )}

              ${quick(
                "categories",
                "▦",
                "Catalog structure",
                "Categories and subcategories"
              )}

              ${quick(
                "products",
                "◫",
                "Product master",
                "Products, variants and images"
              )}

              ${quick(
                "inventory",
                "▥",
                "Stock controls",
                "Branch-level quantity & price"
              )}

            </div>

          </div>

        </div>


        <div class="panel">

          <div class="panel-head">
            <div>

              <h3>
                Role & security
              </h3>

              <p>
                Backend remains
                source of truth
              </p>

            </div>
          </div>


          <div class="panel-body">

            <div class="activity-list">

              <div class="activity-row">

                <span
                  class="activity-dot"
                ></span>

                <div>
                  <b>
                    Bearer token attached
                  </b>

                  <span>
                    Protected calls use
                    Authorization header
                  </span>
                </div>

              </div>


              <div class="activity-row">

                <span
                  class="activity-dot"
                ></span>

                <div>
                  <b>
                    Refresh flow enabled
                  </b>

                  <span>
                    401 attempts token
                    refresh once
                  </span>
                </div>

              </div>


              <div class="activity-row">

                <span
                  class="activity-dot"
                ></span>

                <div>
                  <b>
                    403 handled safely
                  </b>

                  <span>
                    Unauthorized page
                    instead of broken UI
                  </span>
                </div>

              </div>


              <div class="activity-row">

                <span
                  class="activity-dot"
                ></span>

                <div>
                  <b>
                    Current role:
                    ${escapeHtml(
                      getRole()
                    )}
                  </b>

                  <span>
                    JWT / admin profile
                    derived
                  </span>
                </div>

              </div>

            </div>

          </div>

        </div>

      </div>
    `;
}


function stat(
  icon,
  label,
  value,
  sub
) {
  return `
    <div class="stat-card">

      <div class="stat-top">

        <span class="stat-icon">
          ${icon}
        </span>

        <span class="trend">
          LIVE
        </span>

      </div>

      <h4>
        ${escapeHtml(value)}
      </h4>

      <small>
        ${escapeHtml(label)}
      </small>

      <span class="row-sub">
        ${escapeHtml(sub)}
      </span>

    </div>
  `;
}


function quick(
  page,
  icon,
  title,
  subtitle
) {
  return `
    <button
      class="quick-action"
      onclick="navigate('${page}')"
    >

      <span class="stat-icon">
        ${icon}
      </span>

      <b>
        ${title}
      </b>

      <span>
        ${subtitle}
      </span>

    </button>
  `;
}


// ============================================================
// GENERIC CRUD
// ============================================================

async function renderCrud(key) {
  const module =
    modules[key];

  if (!module) {
    return;
  }


  if (
    key === "images"
  ) {
    return renderImages();
  }


  const rows =
    await api(
      module.list
    );


  state.data[key] =
    rows;


  // Keep relation cache fresh
  state.relations[key] =
    rows;


  renderCrudTable(
    key,
    rows
  );
}


function renderCrudTable(
  key,
  rows
) {
  const module =
    modules[key];

  const canCreate =
    !!module.create;


  const html = `
    <div class="toolbar">

      <div class="search">

        <input
          data-search="${key}"
          placeholder="Search ${module.title.toLowerCase()}..."
        >

      </div>


      <div class="toolbar-actions">

        <button
          class="secondary-btn"
          onclick="navigate('${key}')"
        >
          ↻ Refresh
        </button>

        ${
          canCreate
            ? `
              <button
                class="primary-btn"
                onclick="openCreate('${key}')"
              >
                ＋ Add ${module.title.replace(/s$/, "")}
              </button>
            `
            : ""
        }

      </div>

    </div>


    <div class="panel">

      <div class="panel-head">

        <div>

          <h3>
            ${module.title}
          </h3>

          <p>
            ${rows.length}
            record${rows.length === 1 ? "" : "s"}
            returned by the API
          </p>

        </div>

      </div>


      <div
        class="table-wrap"
        id="table-${key}"
      >
        ${tableFor(key, rows)}
      </div>

    </div>
  `;


  $("#content")
    .innerHTML =
    html;


  const search =
    $(
      `[data-search="${key}"]`
    );


  if (search) {
    search.oninput =
      () => {
        const q =
          search.value
            .toLowerCase();


        const filtered =
          rows.filter(
            (row) =>
              JSON.stringify(row)
                .toLowerCase()
                .includes(q)
          );


        $(
          `#table-${key}`
        ).innerHTML =
          tableFor(
            key,
            filtered
          );
      };
  }
}


// ============================================================
// GENERIC TABLE
// ============================================================

function tableFor(
  key,
  rows
) {
  const module =
    modules[key];


  if (!rows.length) {
    return `
      <div class="empty">

        <div class="big">
          ◇
        </div>

        <b>
          No records found
        </b>

        <p>
          Create the first record
          or check the API response.
        </p>

      </div>
    `;
  }


  return `
    <table class="data-table">

      <thead>
        <tr>

          ${
            module.cols
              .map(
                (column) =>
                  `
                    <th>
                      ${column.replaceAll("_", " ")}
                    </th>
                  `
              )
              .join("")
          }

          <th>
            Actions
          </th>

        </tr>
      </thead>


      <tbody>

        ${
          rows
            .map(
              (row) => `
                <tr>

                  ${
                    module.cols
                      .map(
                        (column) =>
                          `
                            <td>
                              ${cell(
                                column,
                                row[column],
                                row
                              )}
                            </td>
                          `
                      )
                      .join("")
                  }


                  <td>

                    <div class="actions">

                      <button
                        class="action-btn"
                        onclick='openEdit(
                          ${JSON.stringify(key)},
                          ${JSON.stringify(row[module.id])}
                        )'
                      >
                        Edit
                      </button>


                      ${
                        key === "branches"
                          ? `
                            <button
                              class="action-btn"
                              onclick='openAssignManager(
                                ${JSON.stringify(row[module.id])}
                              )'
                            >
                              Assign Manager
                            </button>
                          `
                          : ""
                      }


                      ${
                        module.activatable
                          ? `
                            <button
                              class="action-btn"
                              onclick='toggleActive(
                                ${JSON.stringify(key)},
                                ${JSON.stringify(row[module.id])},
                                ${!!row.is_active}
                              )'
                            >
                              ${
                                row.is_active
                                  ? "Disable"
                                  : "Activate"
                              }
                            </button>
                          `
                          : ""
                      }


                      <button
                        class="action-btn danger"
                        onclick='removeRow(
                          ${JSON.stringify(key)},
                          ${JSON.stringify(row[module.id])}
                        )'
                      >
                        Delete
                      </button>

                    </div>

                  </td>

                </tr>
              `
            )
            .join("")
        }

      </tbody>

    </table>
  `;
}


// ============================================================
// TABLE CELL
// ============================================================

function cell(
  key,
  value,
  row
) {
  if (
    key === "is_active" ||
    key === "is_available"
  ) {
    return `
      <span
        class="badge ${
          value ? "on" : "off"
        }"
      >
        ●
        ${
          value
            ? "Active"
            : "Inactive"
        }
      </span>
    `;
  }


  if (
    key === "role"
  ) {
    return `
      <span class="badge role">
        ${escapeHtml(value)}
      </span>
    `;
  }


  if (
    key.includes("created_at") ||
    key.includes("updated_at")
  ) {
    return value
      ? new Date(
          value
        ).toLocaleDateString()
      : "—";
  }


  if (
    key === "image_url" &&
    value
  ) {
    return `
      <a
        href="${escapeHtml(value)}"
        target="_blank"
      >
        Image URL ↗
      </a>
    `;
  }


  if (
    key === "name"
  ) {
    return `
      <span class="row-title">
        ${escapeHtml(value)}
      </span>

      ${
        row.unique_id
          ? `
            <span class="row-sub">
              ${escapeHtml(row.unique_id)}
            </span>
          `
          : ""
      }
    `;
  }


  return escapeHtml(
    value ?? "—"
  );
}


// ============================================================
// OPENAPI SCHEMA HELPERS
// ============================================================

function schema(name) {
  return (
    state.spec
      ?.components
      ?.schemas
      ?.[name] ||
    {
      properties: {},
    }
  );
}


function fieldType(def) {
  const field =
    def.type
      ? def
      : (
          def.anyOf?.find(
            (x) =>
              x.type &&
              x.type !== "null"
          ) || {}
        );


  if (
    field.type === "boolean"
  ) {
    return "boolean";
  }


  if (
    field.type === "integer" ||
    field.type === "number"
  ) {
    return "number";
  }


  if (
    field.format === "email"
  ) {
    return "email";
  }


  if (
    field.format === "date-time"
  ) {
    return "datetime-local";
  }


  return "text";
}


// ============================================================
// RELATION SELECT
// ============================================================

function relationFieldHtml(
  key,
  required,
  selectedValue = ""
) {
  const config =
    relationConfig[key];

  if (!config) {
    return "";
  }


  const rows =
    state.relations[
      config.cache
    ] || [];


  const label =
    key
      .replaceAll(
        "_unique_id",
        ""
      )
      .replaceAll(
        "_",
        " "
      )
      .replace(
        /\b\w/g,
        (m) =>
          m.toUpperCase()
      );


  return `
    <label class="field">

      <span>
        ${label}
        ${required ? " *" : ""}
      </span>


      <select
        name="${key}"
        ${required ? "required" : ""}
      >

        <option value="">
          ${
            required
              ? config.placeholder
              : `No change / ${config.placeholder}`
          }
        </option>


        ${
          rows
            .map(
              (row) => `
                <option
                  value="${escapeHtml(row.unique_id)}"
                  ${
                    String(
                      selectedValue || ""
                    ) ===
                    String(
                      row.unique_id || ""
                    )
                      ? "selected"
                      : ""
                  }
                >
                  ${escapeHtml(
                    config.label(row)
                  )}
                </option>
              `
            )
            .join("")
        }

      </select>

      ${
        !rows.length
          ? `
            <small>
              No records were returned
              by ${escapeHtml(config.path)}.
            </small>
          `
          : ""
      }

    </label>
  `;
}


// ============================================================
// FORM BUILDER
//
// NOW ASYNC because it fetches related records first.
// ============================================================

async function formFields(
  schemaName,
  data = {}
) {
  await prepareRelationsForSchema(
    schemaName
  );


  const s =
    schema(schemaName);


  const required =
    new Set(
      s.required || []
    );


  return Object.entries(
    s.properties || {}
  )
    .map(
      ([key, definition]) => {

        const isRequired =
          required.has(key);


        const value =
          data[key];


        // ---------------------------------
        // RELATIONAL UUID FIELD
        // ---------------------------------

        if (
          relationConfig[key]
        ) {
          return relationFieldHtml(
            key,
            isRequired,
            value
          );
        }


        const type =
          fieldType(
            definition
          );


        const label =
          key
            .replaceAll(
              "_",
              " "
            )
            .replace(
              /\b\w/g,
              (m) =>
                m.toUpperCase()
            );


        // ---------------------------------
        // BOOLEAN
        // ---------------------------------

        if (
          type === "boolean"
        ) {
          return `
            <label class="field">

              <span>
                ${label}
                ${isRequired ? " *" : ""}
              </span>


              <select
                name="${key}"
              >

                <option
                  value="true"
                  ${
                    value === true
                      ? "selected"
                      : ""
                  }
                >
                  Yes
                </option>


                <option
                  value="false"
                  ${
                    value === false
                      ? "selected"
                      : ""
                  }
                >
                  No
                </option>


                ${
                  !isRequired
                    ? `
                      <option
                        value=""
                        ${
                          value === undefined ||
                          value === null
                            ? "selected"
                            : ""
                        }
                      >
                        No change
                      </option>
                    `
                    : ""
                }

              </select>

            </label>
          `;
        }


        // ---------------------------------
        // NORMAL FIELD
        // ---------------------------------

        return `
          <label
            class="field ${
              [
                "description",
                "address",
                "image_url",
              ].includes(key)
                ? "full"
                : ""
            }"
          >

            <span>
              ${label}
              ${isRequired ? " *" : ""}
            </span>


            <input
              name="${key}"
              type="${type}"
              value="${escapeHtml(
                value ?? ""
              )}"
              ${
                isRequired
                  ? "required"
                  : ""
              }
              placeholder="${label}"
            >

          </label>
        `;
      }
    )
    .join("");
}


// ============================================================
// MODAL
// ============================================================

function openModal({
  title,
  kicker = "ACTION",
  body,
  submit =
    "Save changes",
  onSubmit,
}) {
  state.modal = {
    onSubmit,
  };


  $("#modal-title")
    .textContent =
    title;


  $("#modal-kicker")
    .textContent =
    kicker;


  $("#modal-body")
    .innerHTML =
    body;


  $("#modal-submit")
    .textContent =
    submit;


  $("#modal")
    .classList
    .remove("hidden");
}


function closeModal() {
  $("#modal")
    .classList
    .add("hidden");

  state.modal = null;
}


// ============================================================
// FORM -> JS OBJECT
// ============================================================

function formObject(form) {
  const result = {};


  new FormData(form)
    .forEach(
      (value, key) => {

        if (
          value === ""
        ) {
          return;
        }


        const input =
          form.elements[key];


        if (
          input?.tagName ===
            "SELECT" &&
          (
            value === "true" ||
            value === "false"
          )
        ) {
          result[key] =
            value === "true";
        }

        else if (
          input?.type ===
          "number"
        ) {
          result[key] =
            Number(value);
        }

        else {
          result[key] =
            value;
        }
      }
    );


  return result;
}


// ============================================================
// CREATE
// ============================================================

async function openCreate(key) {
  const module =
    modules[key];


  let body =
    await formFields(
      module.createSchema
    );


  // -----------------------------------------
  // CREATE BRANCH:
  // optional manager selection
  // -----------------------------------------

  if (
    key === "branches"
  ) {
    await loadRelation(
      "manager_unique_id",
      true
    );


    body += `
      <div
        class="full"
        style="
          margin-top:8px;
          padding-top:16px;
          border-top:1px solid var(--line);
        "
      >

        <div
          style="
            font-weight:700;
            margin-bottom:10px;
          "
        >
          Manager Assignment
        </div>

        <div class="muted"
          style="
            font-size:12px;
            margin-bottom:12px;
          "
        >
          Optional. The branch will be
          created first and then the
          selected manager will be
          assigned automatically.
        </div>

      </div>

      ${relationFieldHtml(
        "manager_unique_id",
        false
      )}
    `;
  }


  openModal({
    title:
      `Create ${module.title.replace(/s$/, "")}`,

    kicker:
      "NEW RECORD",

    body,

    submit:
      "Create",

    onSubmit:
      async (data) => {

        // -------------------------------------
        // BRANCH + MANAGER
        // -------------------------------------

        if (
          key === "branches"
        ) {
          const managerId =
            data.manager_unique_id;


          delete data.manager_unique_id;


          // First create branch
          const createdBranch =
            await api(
              module.create,
              {
                method:
                  "POST",

                body:
                  JSON.stringify(
                    data
                  ),
              }
            );


          // Then assign manager if selected
          if (
            managerId &&
            createdBranch?.unique_id
          ) {
            await api(
              `/branches/${encodeURIComponent(
                createdBranch.unique_id
              )}/manager`,
              {
                method:
                  "PATCH",

                body:
                  JSON.stringify({
                    manager_unique_id:
                      managerId,
                  }),
              }
            );


            toast(
              "Branch created",
              "Manager assigned successfully"
            );
          } else {
            toast(
              "Branch created successfully"
            );
          }


          // clear relation cache
          delete state.relations.branches;
          delete state.relations.managers;


          closeModal();

          navigate(
            "branches"
          );

          return;
        }


        // -------------------------------------
        // NORMAL CREATE
        // -------------------------------------

        await api(
          module.create,
          {
            method:
              "POST",

            body:
              JSON.stringify(
                data
              ),
          }
        );


        // Relation cache may be stale now
        if (
          state.relations[key]
        ) {
          delete state.relations[key];
        }


        toast(
          "Created successfully"
        );


        closeModal();

        navigate(key);
      },
  });
}


// ============================================================
// EDIT
// ============================================================

async function openEdit(
  key,
  id
) {
  const module =
    modules[key];


  const record =
    (
      state.data[key] ||
      []
    ).find(
      (x) =>
        x[module.id] === id
    ) || {};


  const body =
    await formFields(
      module.updateSchema,
      record
    );


  openModal({
    title:
      `Edit ${module.title.replace(/s$/, "")}`,

    kicker:
      "UPDATE RECORD",

    body,

    onSubmit:
      async (data) => {

        const base =
          module.base ||
          (
            key === "branches"
              ? "/branches"
              : "/" + key
          );


        await api(
          `${base}/${encodeURIComponent(id)}`,
          {
            method:
              "PATCH",

            body:
              JSON.stringify(
                data
              ),
          }
        );


        toast(
          "Changes saved"
        );


        closeModal();

        navigate(key);
      },
  });
}


// ============================================================
// ASSIGN / CHANGE BRANCH MANAGER
// ============================================================

async function openAssignManager(
  branchUniqueId
) {
  const branches =
    state.data.branches ||
    [];


  const branch =
    branches.find(
      (x) =>
        x.unique_id ===
        branchUniqueId
    );


  const managers =
    await loadRelation(
      "manager_unique_id",
      true
    );


  // Find currently assigned manager
  // manager response contains branch field
  const currentManager =
    managers.find(
      (manager) =>
        manager.branch?.unique_id ===
        branchUniqueId
    );


  const managerSelect =
    relationFieldHtml(
      "manager_unique_id",
      true,
      currentManager?.unique_id ||
        ""
    );


  openModal({
    title:
      `Assign Manager${
        branch?.name
          ? ` — ${branch.name}`
          : ""
      }`,

    kicker:
      "BRANCH MANAGER",

    body: `
      <div
        class="full"
        style="
          background:#f6f8f6;
          padding:14px;
          border-radius:12px;
          margin-bottom:8px;
        "
      >

        <b>
          ${
            branch?.name
              ? escapeHtml(branch.name)
              : "Selected branch"
          }
        </b>

        <div
          class="row-sub"
          style="margin-top:4px"
        >
          ${
            branch
              ? escapeHtml(
                  [
                    branch.city,
                    branch.pincode,
                  ]
                    .filter(Boolean)
                    .join(" • ")
                )
              : ""
          }
        </div>

      </div>


      ${
        currentManager
          ? `
            <div
              class="full"
              style="
                padding:12px;
                border:1px solid var(--line);
                border-radius:10px;
                margin-bottom:8px;
              "
            >

              <small>
                CURRENT MANAGER
              </small>

              <div
                style="
                  font-weight:700;
                  margin-top:4px;
                "
              >
                ${escapeHtml(
                  currentManager.name
                )}
              </div>

              <div class="row-sub">
                ${escapeHtml(
                  currentManager.email
                )}
              </div>

            </div>
          `
          : `
            <div
              class="full muted"
              style="
                font-size:12px;
                margin-bottom:8px;
              "
            >
              No manager assignment
              could be detected for
              this branch.
            </div>
          `
      }


      ${managerSelect}
    `,

    submit:
      currentManager
        ? "Change Manager"
        : "Assign Manager",

    onSubmit:
      async (data) => {

        await api(
          `/branches/${encodeURIComponent(
            branchUniqueId
          )}/manager`,
          {
            method:
              "PATCH",

            body:
              JSON.stringify({
                manager_unique_id:
                  data.manager_unique_id,
              }),
          }
        );


        delete state.relations.managers;


        toast(
          currentManager
            ? "Manager changed"
            : "Manager assigned",
          branch?.name ||
            ""
        );


        closeModal();

        navigate(
          "branches"
        );
      },
  });
}


// ============================================================
// ACTIVATE / DEACTIVATE
// ============================================================

async function toggleActive(
  key,
  id,
  current
) {
  const module =
    modules[key];


  try {
    await api(
      `${module.base}/${encodeURIComponent(id)}/${current ? "deactivate" : "activate"}`,
      {
        method:
          "PATCH",
      }
    );


    delete state.relations[key];


    toast(
      current
        ? "Deactivated"
        : "Activated"
    );


    navigate(key);

  } catch (e) {

    if (
      [401, 403]
        .includes(e.status)
    ) {
      renderUnauthorized(e);
    }

    else {
      toast(
        "Action failed",
        e.message,
        "error"
      );
    }
  }
}


// ============================================================
// DELETE
// ============================================================

function removeRow(
  key,
  id
) {
  const module =
    modules[key];


  const base =
    module.base ||
    (
      key === "branches"
        ? "/branches"
        : "/" + key
    );


  openModal({
    title:
      "Confirm deletion",

    kicker:
      "DESTRUCTIVE ACTION",

    body: `
      <div class="danger-box full">

        This will call

        <b>
          DELETE
          ${escapeHtml(
            base + "/" + id
          )}
        </b>.

        This action may be
        permanent depending on
        your backend.

      </div>
    `,

    submit:
      "Delete permanently",

    onSubmit:
      async () => {

        await api(
          `${base}/${encodeURIComponent(id)}`,
          {
            method:
              "DELETE",
          }
        );


        delete state.relations[key];


        toast(
          "Record deleted"
        );


        closeModal();

        navigate(key);
      },
  });
}


// ============================================================
// CATEGORIES
// ============================================================

async function renderCategories() {
  const [
    categories,
    subcategories,
  ] = await Promise.all([
    api("/categories"),
    api("/subcategories"),
  ]);


  state.data.categories =
    categories;

  state.data.subcategories =
    subcategories;


  state.relations.categories =
    categories;

  state.relations.subcategories =
    subcategories;


  $("#content")
    .innerHTML = `
      <div class="toolbar">

        <div class="search">

          <input
            id="cat-search"
            placeholder="Search category or subcategory..."
          >

        </div>


        <div class="toolbar-actions">

          <button
            class="secondary-btn"
            onclick="openSubcategory()"
          >
            ＋ Subcategory
          </button>

          <button
            class="primary-btn"
            onclick="openCategory()"
          >
            ＋ Category
          </button>

        </div>

      </div>


      <div class="catalog-layout">

        <div class="panel tree-panel">

          <div class="panel-head">

            <div>

              <h3>
                Category tree
              </h3>

              <p>
                ${categories.length}
                categories ·
                ${subcategories.length}
                subcategories
              </p>

            </div>

          </div>


          <div class="panel-body">

            ${
              categories
                .map(
                  (category) => `
                    <div class="tree-item">

                      <b>
                        ${escapeHtml(
                          category.name
                        )}
                      </b>

                      <span>
                        ${
                          subcategories.filter(
                            (sub) =>
                              sub.category_unique_id ===
                              category.unique_id
                          ).length
                        }
                      </span>

                    </div>


                    <div class="tree-sub">

                      ${
                        subcategories
                          .filter(
                            (sub) =>
                              sub.category_unique_id ===
                              category.unique_id
                          )
                          .map(
                            (sub) => `
                              <div class="tree-item">
                                ↳
                                ${escapeHtml(
                                  sub.name
                                )}
                              </div>
                            `
                          )
                          .join("")
                      }

                    </div>
                  `
                )
                .join("")
            }

          </div>

        </div>


        <div class="panel">

          <div class="panel-head">

            <div>

              <h3>
                Categories
              </h3>

              <p>
                Manage master grouping
                and nested subcategories
              </p>

            </div>

          </div>


          <div
            class="table-wrap"
            id="cat-table"
          >
            ${categoryTable(
              categories,
              subcategories
            )}
          </div>

        </div>

      </div>
    `;


  $("#cat-search")
    .oninput =
    (e) => {

      const q =
        e.target.value
          .toLowerCase();


      const filtered =
        categories.filter(
          (category) =>
            JSON.stringify(
              category
            )
              .toLowerCase()
              .includes(q) ||

            subcategories.some(
              (sub) =>
                sub.category_unique_id ===
                  category.unique_id &&
                JSON.stringify(sub)
                  .toLowerCase()
                  .includes(q)
            )
        );


      $("#cat-table")
        .innerHTML =
        categoryTable(
          filtered,
          subcategories
        );
    };
}


// ============================================================
// CATEGORY TABLE
// ============================================================

function categoryTable(
  categories,
  subcategories
) {
  if (
    !categories.length
  ) {
    return `
      <div class="empty">
        <b>
          No category found
        </b>
      </div>
    `;
  }


  return `
    <table class="data-table">

      <thead>
        <tr>
          <th>Category</th>
          <th>Subcategories</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>


      <tbody>

        ${
          categories
            .map(
              (category) => `
                <tr>

                  <td>

                    <span class="row-title">
                      ${escapeHtml(
                        category.name
                      )}
                    </span>

                    <span class="row-sub">
                      /${escapeHtml(
                        category.slug
                      )}
                    </span>

                  </td>


                  <td>

                    ${
                      subcategories
                        .filter(
                          (sub) =>
                            sub.category_unique_id ===
                            category.unique_id
                        )
                        .map(
                          (sub) => `
                            <span
                              class="badge role"
                              style="margin-right:4px"
                            >
                              ${escapeHtml(
                                sub.name
                              )}
                            </span>
                          `
                        )
                        .join("") ||
                      "—"
                    }

                  </td>


                  <td>
                    ${cell(
                      "is_active",
                      category.is_active,
                      category
                    )}
                  </td>


                  <td>

                    <div class="actions">

                      <button
                        class="action-btn"
                        onclick='openCategory(
                          ${JSON.stringify(
                            category.unique_id
                          )}
                        )'
                      >
                        Edit
                      </button>


                      <button
                        class="action-btn"
                        onclick='viewSubcategories(
                          ${JSON.stringify(
                            category.unique_id
                          )}
                        )'
                      >
                        View nested
                      </button>


                      <button
                        class="action-btn danger"
                        onclick='deleteCategory(
                          ${JSON.stringify(
                            category.unique_id
                          )}
                        )'
                      >
                        Delete
                      </button>

                    </div>

                  </td>

                </tr>
              `
            )
            .join("")
        }

      </tbody>

    </table>
  `;
}


// ============================================================
// CREATE / EDIT CATEGORY
// ============================================================

async function openCategory(
  id = null
) {
  const category =
    (
      state.data.categories ||
      []
    ).find(
      (x) =>
        x.unique_id === id
    ) || {};


  const schemaName =
    id
      ? "CategoryUpdate"
      : "CategoryCreate";


  const body =
    await formFields(
      schemaName,
      category
    );


  openModal({
    title:
      id
        ? "Edit category"
        : "Create category",

    body,

    submit:
      id
        ? "Save changes"
        : "Create",

    onSubmit:
      async (data) => {

        await api(
          id
            ? `/categories/${encodeURIComponent(id)}`
            : "/categories",
          {
            method:
              id
                ? "PATCH"
                : "POST",

            body:
              JSON.stringify(
                data
              ),
          }
        );


        delete state.relations.categories;


        toast(
          id
            ? "Category updated"
            : "Category created"
        );


        closeModal();

        navigate(
          "categories"
        );
      },
  });
}


// ============================================================
// CREATE SUBCATEGORY
// ============================================================

async function openSubcategory(
  id = null
) {
  const subcategory =
    (
      state.data.subcategories ||
      []
    ).find(
      (x) =>
        x.unique_id === id
    ) || {};


  const schemaName =
    id
      ? "SubCategoryUpdate"
      : "SubCategoryCreate";


  const body =
    await formFields(
      schemaName,
      subcategory
    );


  openModal({
    title:
      id
        ? "Edit subcategory"
        : "Create subcategory",

    body,

    submit:
      id
        ? "Save changes"
        : "Create",

    onSubmit:
      async (data) => {

        await api(
          id
            ? `/subcategories/${encodeURIComponent(id)}`
            : "/subcategories",
          {
            method:
              id
                ? "PATCH"
                : "POST",

            body:
              JSON.stringify(
                data
              ),
          }
        );


        delete state.relations.subcategories;


        toast(
          "Subcategory saved"
        );


        closeModal();

        navigate(
          "categories"
        );
      },
  });
}


// ============================================================
// VIEW SUBCATEGORIES
// ============================================================

async function viewSubcategories(id) {
  try {
    const result =
      await api(
        `/categories/${encodeURIComponent(id)}/subcategories`
      );


    openModal({
      title:
        "Category details",

      kicker:
        "NESTED SUBCATEGORIES",

      body: `
        <div class="full">

          <pre
            style="
              white-space:pre-wrap;
              font-size:11px;
              background:#f6f8f6;
              padding:14px;
              border-radius:12px;
            "
          >${escapeHtml(
            JSON.stringify(
              result,
              null,
              2
            )
          )}</pre>

        </div>
      `,

      submit:
        "Close",

      onSubmit:
        async () =>
          closeModal(),
    });

  } catch (e) {
    toast(
      "Could not load",
      e.message,
      "error"
    );
  }
}


// ============================================================
// DELETE CATEGORY
// ============================================================

function deleteCategory(id) {
  openModal({
    title:
      "Delete category",

    kicker:
      "DESTRUCTIVE ACTION",

    body: `
      <div class="danger-box full">

        Delete category

        <b>
          ${escapeHtml(id)}
        </b>?

        The backend will decide
        whether linked
        subcategories/products
        prevent deletion.

      </div>
    `,

    submit:
      "Delete",

    onSubmit:
      async () => {

        await api(
          `/categories/${encodeURIComponent(id)}`,
          {
            method:
              "DELETE",
          }
        );


        delete state.relations.categories;


        closeModal();

        navigate(
          "categories"
        );
      },
  });
}


// ============================================================
// INVENTORY
// ============================================================

// NOTE:
// GET /inventory currently does not return branch_unique_id or
// product_variant_unique_id. Because of that, this admin screen
// verifies the exact (branch, variant) pair using:
// GET /inventory/branch/{branch_unique_id}/variant/{variant_unique_id}
//
// Product names are resolved from:
// GET /products
// GET /products/{product_unique_id}/details
//
// This gives us a correct table:
// Branch -> Product -> Variant -> Inventory


async function mapWithConcurrency(items, limit, worker) {
  const results = new Array(items.length);
  let nextIndex = 0;

  async function runWorker() {
    while (true) {
      const index = nextIndex++;

      if (index >= items.length) {
        return;
      }

      try {
        results[index] = await worker(items[index], index);
      } catch (error) {
        results[index] = null;
        console.warn("Inventory lookup worker failed", error);
      }
    }
  }

  const workers = Array.from(
    { length: Math.min(limit, items.length) },
    () => runWorker()
  );

  await Promise.all(workers);

  return results;
}


async function loadInventoryProductLookup(force = false) {
  if (
    !force &&
    Array.isArray(state.data.inventoryProductLookup)
  ) {
    return state.data.inventoryProductLookup;
  }

  const products = await api(
    "/products?skip=0&limit=1000"
  );

  const details = await mapWithConcurrency(
    products,
    6,
    async (product) => {
      try {
        return await api(
          `/products/${encodeURIComponent(product.unique_id)}/details`
        );
      } catch (error) {
        console.warn(
          `Could not load product details: ${product.name}`,
          error
        );

        return {
          ...product,
          brand: null,
          subcategory: null,
          variants: [],
        };
      }
    }
  );

  const lookup = [];

  for (const product of details.filter(Boolean)) {
    for (const variant of product.variants || []) {
      lookup.push({
        product_unique_id: product.unique_id,
        product_name: product.name,
        product_slug: product.slug,
        product_is_active: product.is_active,

        brand_name: product.brand?.name || "—",
        subcategory_name: product.subcategory?.name || "—",

        product_variant_unique_id: variant.unique_id,
        sku: variant.sku,
        value: variant.value,
        unit: variant.unit,
        mrp: variant.mrp,
        selling_price: variant.selling_price,
        variant_is_active: variant.is_active,
      });
    }
  }

  state.data.inventoryProductLookup = lookup;

  return lookup;
}


async function getExactInventory(branchId, variantId) {
  try {
    return await api(
      `/inventory/branch/${encodeURIComponent(branchId)}/variant/${encodeURIComponent(variantId)}`
    );
  } catch (error) {
    // Missing mapping is normal while scanning possible combinations.
    if (error.status === 404) {
      return null;
    }

    throw error;
  }
}


async function loadAllInventoryAssignments(force = false) {
  if (
    !force &&
    Array.isArray(state.data.inventoryAssignments)
  ) {
    return state.data.inventoryAssignments;
  }

  const [branches, variantLookup] = await Promise.all([
    api("/branches/"),
    loadInventoryProductLookup(force),
  ]);

  state.data.branches = branches;
  state.relations.branches = branches;

  const pairs = [];

  for (const branch of branches) {
    for (const variant of variantLookup) {
      pairs.push({
        branch,
        variant,
      });
    }
  }

  const checked = await mapWithConcurrency(
    pairs,
    10,
    async ({ branch, variant }) => {
      const inventory = await getExactInventory(
        branch.unique_id,
        variant.product_variant_unique_id
      );

      if (!inventory) {
        return null;
      }

      return {
        branch_unique_id: branch.unique_id,
        branch_name: branch.name,
        branch_city: branch.city,
        branch_pincode: branch.pincode,

        product_unique_id: variant.product_unique_id,
        product_name: variant.product_name,
        product_slug: variant.product_slug,
        product_is_active: variant.product_is_active,

        brand_name: variant.brand_name,
        subcategory_name: variant.subcategory_name,

        product_variant_unique_id:
          variant.product_variant_unique_id,

        sku: variant.sku,
        value: variant.value,
        unit: variant.unit,
        mrp: variant.mrp,
        selling_price: variant.selling_price,
        variant_is_active: variant.variant_is_active,

        stock_quantity: inventory.stock_quantity,
        selling_price_override:
          inventory.selling_price_override,
        is_available: inventory.is_available,
        created_at: inventory.created_at,
        updated_at: inventory.updated_at,
      };
    }
  );

  const rows = checked
    .filter(Boolean)
    .sort((a, b) => {
      const branchCompare = String(a.branch_name).localeCompare(
        String(b.branch_name)
      );

      if (branchCompare !== 0) {
        return branchCompare;
      }

      const productCompare = String(a.product_name).localeCompare(
        String(b.product_name)
      );

      if (productCompare !== 0) {
        return productCompare;
      }

      return String(a.sku).localeCompare(String(b.sku));
    });

  state.data.inventoryAssignments = rows;
  state.data.inventory = rows;

  return rows;
}


async function renderInventory() {
  // Clear old cached result so Refresh always checks real inventory.
  delete state.data.inventoryAssignments;
  delete state.data.inventoryProductLookup;

  const branches = await api("/branches/");

  state.data.branches = branches;
  state.relations.branches = branches;

  // Render shell first so the user can see what is happening.
  $("#content").innerHTML = `
    <div class="toolbar">

      <div class="search">
        <input
          id="inv-search"
          placeholder="Search branch, product, SKU, brand..."
          disabled
        >
      </div>

      <div class="toolbar-actions">

        <select
          id="inv-branch-filter"
          disabled
          style="
            min-width:220px;
            padding:11px;
            border:1px solid var(--line);
            border-radius:10px;
          "
        >
          <option value="">
            All branches
          </option>

          ${branches
            .map(
              (branch) => `
                <option value="${escapeHtml(branch.unique_id)}">
                  ${escapeHtml(branch.name)}
                  ${branch.city ? ` — ${escapeHtml(branch.city)}` : ""}
                </option>
              `
            )
            .join("")}
        </select>

        <button
          class="secondary-btn"
          onclick="openStockAction()"
        >
          ± Adjust stock
        </button>

        <button
          class="primary-btn"
          onclick="openInventoryCreate()"
        >
          ＋ Assign Product
        </button>

      </div>
    </div>

    <div class="panel">
      <div class="panel-head">
        <div>
          <h3>
            Branch inventory
          </h3>

          <p id="inventory-count-text">
            Checking branch-product assignments…
          </p>
        </div>
      </div>

      <div class="panel-body" id="inventory-loading">
        <div class="skeleton"></div>
        <br>
        <div class="skeleton" style="width:82%"></div>
        <br>
        <div class="skeleton" style="width:64%"></div>
      </div>

      <div
        class="table-wrap"
        id="inv-table"
      ></div>
    </div>
  `;

  const rows = await loadAllInventoryAssignments(true);

  const loading = $("#inventory-loading");

  if (loading) {
    loading.remove();
  }

  const searchInput = $("#inv-search");
  const branchFilter = $("#inv-branch-filter");

  searchInput.disabled = false;
  branchFilter.disabled = false;

  $("#inventory-count-text").textContent =
    `${rows.length} actual branch-product variant assignment${
      rows.length === 1 ? "" : "s"
    }`;

  $("#inv-table").innerHTML = inventoryTable(rows);

  function applyFilters() {
    const query = searchInput.value.trim().toLowerCase();
    const branchId = branchFilter.value;

    const filtered = rows.filter((row) => {
      const branchMatches =
        !branchId || row.branch_unique_id === branchId;

      const queryMatches =
        !query ||
        [
          row.branch_name,
          row.branch_city,
          row.branch_pincode,
          row.product_name,
          row.product_slug,
          row.brand_name,
          row.subcategory_name,
          row.sku,
          row.value,
          row.unit,
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
          .includes(query);

      return branchMatches && queryMatches;
    });

    $("#inv-table").innerHTML = inventoryTable(filtered);

    $("#inventory-count-text").textContent =
      `${filtered.length} of ${rows.length} assignment${
        rows.length === 1 ? "" : "s"
      } shown`;
  }

  searchInput.oninput = applyFilters;
  branchFilter.onchange = applyFilters;
}


// ============================================================
// INVENTORY TABLE
// ============================================================

function inventoryTable(rows) {
  if (!rows.length) {
    return `
      <div class="empty">
        <div class="big">▥</div>

        <b>
          No assigned inventory found
        </b>

        <p>
          This filter/branch has no product variants assigned in inventory.
          Use “Assign Product” to create a branch-product mapping.
        </p>
      </div>
    `;
  }

  return `
    <table class="data-table">
      <thead>
        <tr>
          <th>Branch</th>
          <th>Product</th>
          <th>Brand</th>
          <th>Variant</th>
          <th>SKU</th>
          <th>Stock</th>
          <th>MRP</th>
          <th>Selling Price</th>
          <th>Inventory Status</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        ${rows
          .map((row) => {
            const effectivePrice =
              row.selling_price_override != null
                ? row.selling_price_override
                : row.selling_price;

            const sellableNow =
              row.is_available === true &&
              Number(row.stock_quantity) > 0 &&
              row.variant_is_active !== false &&
              row.product_is_active !== false;

            return `
              <tr>
                <td>
                  <span class="row-title">
                    ${escapeHtml(row.branch_name)}
                  </span>

                  <span class="row-sub">
                    ${escapeHtml(
                      [row.branch_city, row.branch_pincode]
                        .filter(Boolean)
                        .join(" • ")
                    )}
                  </span>
                </td>

                <td>
                  <span class="row-title">
                    ${escapeHtml(row.product_name)}
                  </span>

                  <span class="row-sub">
                    ${escapeHtml(row.subcategory_name)}
                  </span>
                </td>

                <td>
                  ${escapeHtml(row.brand_name)}
                </td>

                <td>
                  <b>
                    ${escapeHtml(row.value)} ${escapeHtml(row.unit)}
                  </b>
                </td>

                <td>
                  <span class="badge role">
                    ${escapeHtml(row.sku)}
                  </span>
                </td>

                <td>
                  <b>${escapeHtml(row.stock_quantity)}</b>
                </td>

                <td>
                  ₹${escapeHtml(row.mrp)}
                </td>

                <td>
                  <b>
                    ₹${escapeHtml(effectivePrice)}
                  </b>

                  <span class="row-sub">
                    ${
                      row.selling_price_override != null
                        ? "Branch override"
                        : "Default price"
                    }
                  </span>
                </td>

                <td>
                  <span class="badge ${sellableNow ? "on" : "off"}">
                    ● ${sellableNow ? "Sellable" : "Not sellable"}
                  </span>

                  <span class="row-sub">
                    inventory=${row.is_available ? "on" : "off"},
                    stock=${escapeHtml(row.stock_quantity)}
                  </span>
                </td>

                <td>
                  <div class="actions">
                    <button
                      class="action-btn"
                      onclick='openQuickInventoryStock(
                        ${JSON.stringify(row.branch_unique_id)},
                        ${JSON.stringify(row.product_variant_unique_id)},
                        ${JSON.stringify(row.product_name)},
                        ${JSON.stringify(`${row.value} ${row.unit}`)}
                      )'
                    >
                      Stock
                    </button>

                    <button
                      class="action-btn"
                      onclick='toggleInventoryAvailability(
                        ${JSON.stringify(row.branch_unique_id)},
                        ${JSON.stringify(row.product_variant_unique_id)},
                        ${!!row.is_available}
                      )'
                    >
                      ${row.is_available ? "Disable" : "Enable"}
                    </button>

                    <button
                      class="action-btn"
                      onclick='showRaw(${JSON.stringify(row)})'
                    >
                      Details
                    </button>

                    <button
                      class="action-btn danger"
                      onclick='removeInventoryAssignment(
                        ${JSON.stringify(row.branch_unique_id)},
                        ${JSON.stringify(row.product_variant_unique_id)},
                        ${JSON.stringify(row.branch_name)},
                        ${JSON.stringify(row.product_name)}
                      )'
                    >
                      Remove
                    </button>
                  </div>
                </td>
              </tr>
            `;
          })
          .join("")}
      </tbody>
    </table>
  `;
}


// ============================================================
// CREATE INVENTORY / ASSIGN PRODUCT TO BRANCH
// ============================================================

async function openInventoryCreate() {
  const [branches, variants] = await Promise.all([
    api("/branches/"),
    loadInventoryProductLookup(true),
  ]);

  const branchOptions = branches
    .filter((branch) => branch.is_active !== false)
    .map(
      (branch) => `
        <option value="${escapeHtml(branch.unique_id)}">
          ${escapeHtml(branch.name)}
          ${branch.city ? ` — ${escapeHtml(branch.city)}` : ""}
        </option>
      `
    )
    .join("");

  const variantOptions = variants
    .filter(
      (item) =>
        item.product_is_active !== false &&
        item.variant_is_active !== false
    )
    .map(
      (item) => `
        <option value="${escapeHtml(item.product_variant_unique_id)}">
          ${escapeHtml(item.product_name)} —
          ${escapeHtml(item.value)} ${escapeHtml(item.unit)} —
          ${escapeHtml(item.sku)}
        </option>
      `
    )
    .join("");

  openModal({
    title: "Assign product to branch",
    kicker: "BRANCH INVENTORY",

    body: `
      <label class="field">
        <span>Branch *</span>

        <select name="branch_unique_id" required>
          <option value="">Choose branch…</option>
          ${branchOptions}
        </select>
      </label>

      <label class="field full">
        <span>Product Variant *</span>

        <select name="product_variant_unique_id" required>
          <option value="">Choose product / variant…</option>
          ${variantOptions}
        </select>

        <small>
          Product name, size and SKU are shown; UUID is sent to the API automatically.
        </small>
      </label>

      <label class="field">
        <span>Stock Quantity *</span>

        <input
          name="stock_quantity"
          type="number"
          min="0"
          value="0"
          required
        >
      </label>

      <label class="field">
        <span>Selling Price Override</span>

        <input
          name="selling_price_override"
          type="number"
          min="0.01"
          step="0.01"
          placeholder="Leave blank for default price"
        >
      </label>

      <label class="field">
        <span>Available *</span>

        <select name="is_available" required>
          <option value="true" selected>Yes</option>
          <option value="false">No</option>
        </select>
      </label>
    `,

    submit: "Assign Product",

    onSubmit: async (data) => {
      await api("/inventory", {
        method: "POST",
        body: JSON.stringify(data),
      });

      delete state.data.inventoryAssignments;

      toast(
        "Product assigned",
        "This exact product variant is now mapped to the selected branch."
      );

      closeModal();
      navigate("inventory");
    },
  });
}


// ============================================================
// STOCK ACTION
// ============================================================

async function openStockAction() {
  const rows = await loadAllInventoryAssignments();

  if (!rows.length) {
    toast(
      "No inventory assignments",
      "Assign a product to a branch first.",
      "error"
    );

    return;
  }

  const branches = [
    ...new Map(
      rows.map((row) => [
        row.branch_unique_id,
        {
          unique_id: row.branch_unique_id,
          name: row.branch_name,
          city: row.branch_city,
        },
      ])
    ).values(),
  ];

  const branchOptions = branches
    .map(
      (branch) => `
        <option value="${escapeHtml(branch.unique_id)}">
          ${escapeHtml(branch.name)}
          ${branch.city ? ` — ${escapeHtml(branch.city)}` : ""}
        </option>
      `
    )
    .join("");

  openModal({
    title: "Adjust stock",
    kicker: "ASSIGNED INVENTORY ONLY",

    body: `
      <label class="field">
        <span>Branch *</span>

        <select
          id="stock-branch-select"
          name="branch_unique_id"
          required
        >
          <option value="">Choose branch…</option>
          ${branchOptions}
        </select>
      </label>

      <label class="field full">
        <span>Assigned Product Variant *</span>

        <select
          id="stock-variant-select"
          name="product_variant_unique_id"
          required
          disabled
        >
          <option value="">
            Choose branch first…
          </option>
        </select>
      </label>

      <label class="field">
        <span>Quantity *</span>

        <input
          name="quantity"
          type="number"
          min="1"
          required
        >
      </label>

      <label class="field">
        <span>Action</span>

        <select name="action">
          <option value="increase-stock">
            Increase stock
          </option>

          <option value="decrease-stock">
            Decrease stock
          </option>
        </select>
      </label>
    `,

    submit: "Apply stock change",

    onSubmit: async (data) => {
      await api(
        `/inventory/branch/${encodeURIComponent(
          data.branch_unique_id
        )}/variant/${encodeURIComponent(
          data.product_variant_unique_id
        )}/${data.action}`,
        {
          method: "PATCH",
          body: JSON.stringify({
            quantity: Number(data.quantity),
          }),
        }
      );

      delete state.data.inventoryAssignments;

      toast("Stock updated");

      closeModal();
      navigate("inventory");
    },
  });

  const branchSelect = $("#stock-branch-select");
  const variantSelect = $("#stock-variant-select");

  branchSelect.onchange = () => {
    const branchId = branchSelect.value;

    const assigned = rows.filter(
      (row) => row.branch_unique_id === branchId
    );

    variantSelect.innerHTML = `
      <option value="">
        Choose assigned product / variant…
      </option>

      ${assigned
        .map(
          (row) => `
            <option value="${escapeHtml(row.product_variant_unique_id)}">
              ${escapeHtml(row.product_name)} —
              ${escapeHtml(row.value)} ${escapeHtml(row.unit)} —
              ${escapeHtml(row.sku)} —
              stock ${escapeHtml(row.stock_quantity)}
            </option>
          `
        )
        .join("")}
    `;

    variantSelect.disabled = !branchId;
  };
}


// ============================================================
// QUICK STOCK UPDATE FROM TABLE ROW
// ============================================================

function openQuickInventoryStock(
  branchId,
  variantId,
  productName,
  variantName
) {
  openModal({
    title: `Adjust Stock — ${productName}`,
    kicker: variantName,

    body: `
      <label class="field">
        <span>Quantity *</span>

        <input
          name="quantity"
          type="number"
          min="1"
          required
        >
      </label>

      <label class="field">
        <span>Action</span>

        <select name="action">
          <option value="increase-stock">
            Increase stock
          </option>

          <option value="decrease-stock">
            Decrease stock
          </option>
        </select>
      </label>
    `,

    submit: "Update Stock",

    onSubmit: async (data) => {
      await api(
        `/inventory/branch/${encodeURIComponent(
          branchId
        )}/variant/${encodeURIComponent(
          variantId
        )}/${data.action}`,
        {
          method: "PATCH",
          body: JSON.stringify({
            quantity: Number(data.quantity),
          }),
        }
      );

      delete state.data.inventoryAssignments;

      toast("Stock updated", productName);

      closeModal();
      navigate("inventory");
    },
  });
}


// ============================================================
// ENABLE / DISABLE AN INVENTORY ASSIGNMENT
// ============================================================

async function toggleInventoryAvailability(
  branchId,
  variantId,
  currentlyAvailable
) {
  try {
    await api(
      `/inventory/branch/${encodeURIComponent(
        branchId
      )}/variant/${encodeURIComponent(
        variantId
      )}/${currentlyAvailable ? "deactivate" : "activate"}`,
      {
        method: "PATCH",
      }
    );

    delete state.data.inventoryAssignments;

    toast(
      currentlyAvailable
        ? "Inventory disabled"
        : "Inventory enabled"
    );

    navigate("inventory");
  } catch (error) {
    if ([401, 403].includes(error.status)) {
      return renderUnauthorized(error);
    }

    toast(
      "Inventory action failed",
      error.message,
      "error"
    );
  }
}


// ============================================================
// REMOVE BRANCH-PRODUCT INVENTORY MAPPING
// ============================================================

function removeInventoryAssignment(
  branchId,
  variantId,
  branchName,
  productName
) {
  openModal({
    title: "Remove inventory assignment",
    kicker: "DESTRUCTIVE ACTION",

    body: `
      <div class="danger-box full">
        Remove
        <b>${escapeHtml(productName)}</b>
        from
        <b>${escapeHtml(branchName)}</b>?

        <br><br>

        This removes only this branch + product variant inventory mapping.
      </div>
    `,

    submit: "Remove Assignment",

    onSubmit: async () => {
      await api(
        `/inventory/branch/${encodeURIComponent(
          branchId
        )}/variant/${encodeURIComponent(variantId)}`,
        {
          method: "DELETE",
        }
      );

      delete state.data.inventoryAssignments;

      toast(
        "Inventory assignment removed",
        `${productName} removed from ${branchName}`
      );

      closeModal();
      navigate("inventory");
    },
  });
}


// ============================================================
// BRANCH CATALOG
// ============================================================

async function renderCatalog() {
  const branches =
    await api(
      "/branches/"
    );


  state.data.branches =
    branches;

  state.relations.branches =
    branches;


  $("#content")
    .innerHTML = `
      <div class="toolbar">

        <div>

          <b
            style="
              font:800 16px Manrope
            "
          >
            Branch catalog preview
          </b>

          <span class="row-sub">
            Select a branch to call
            /branch-catalog/{branch_unique_id}
          </span>

        </div>


        <div class="toolbar-actions">

          <select
            id="catalog-branch"
            style="
              padding:11px;
              border:1px solid var(--line);
              border-radius:10px;
            "
          >

            <option value="">
              Choose branch…
            </option>

            ${
              branches
                .map(
                  (branch) => `
                    <option
                      value="${escapeHtml(branch.unique_id)}"
                    >
                      ${escapeHtml(branch.name)}
                      —
                      ${escapeHtml(branch.city)}
                    </option>
                  `
                )
                .join("")
            }

          </select>

        </div>

      </div>


      <div
        id="catalog-content"
        class="panel"
      >

        <div class="empty">

          <div class="big">
            ⊞
          </div>

          <b>
            Select a branch
          </b>

          <p>
            Products, brand,
            subcategory, images and
            variants returned by the
            branch catalog API will
            appear here.
          </p>

        </div>

      </div>
    `;


  $("#catalog-branch")
    .onchange =
    async (e) => {

      if (
        !e.target.value
      ) {
        return;
      }


      const box =
        $("#catalog-content");


      box.innerHTML = `
        <div class="panel-body">

          <div class="skeleton">
          </div>

          <br>

          <div class="skeleton">
          </div>

        </div>
      `;


      try {
        const rows =
          await api(
            `/branch-catalog/${encodeURIComponent(
              e.target.value
            )}`
          );


        box.innerHTML = `
          <div class="panel-head">

            <div>

              <h3>
                Available catalog
              </h3>

              <p>
                ${rows.length}
                products returned
              </p>

            </div>

          </div>


          <div class="panel-body">

            <div class="product-grid">

              ${
                rows
                  .map(
                    (product) => `
                      <div class="product-card">

                        <div class="product-img">

                          ${
                            product.images?.[0]?.image_url
                              ? `
                                <img
                                  src="${escapeHtml(
                                    product.images[0].image_url
                                  )}"
                                  alt=""
                                >
                              `
                              : "◫"
                          }

                        </div>


                        <div class="product-info">

                          <h4>
                            ${escapeHtml(
                              product.name
                            )}
                          </h4>

                          <p>
                            ${escapeHtml(
                              product.brand?.name ||
                              "No brand"
                            )}
                            ·
                            ${escapeHtml(
                              product.subcategory?.name ||
                              "No subcategory"
                            )}
                          </p>


                          <div class="product-foot">

                            <span class="badge on">
                              ${
                                product.variants?.length ||
                                0
                              }
                              variants
                            </span>


                            <button
                              class="action-btn"
                              onclick='showRaw(
                                ${JSON.stringify(product)}
                              )'
                            >
                              Details
                            </button>

                          </div>

                        </div>

                      </div>
                    `
                  )
                  .join("")
              }

            </div>

          </div>
        `;

      } catch (err) {
        box.innerHTML = "";

        handlePageError(
          err
        );
      }
    };
}


// ============================================================
// PRODUCT IMAGES
//
// Product UUID input replaced by Product dropdown
// ============================================================

async function renderImages() {
  const products =
    await loadRelation(
      "product_unique_id",
      true
    );


  const productOptions =
    products
      .map(
        (product) => `
          <option
            value="${escapeHtml(product.unique_id)}"
          >
            ${escapeHtml(
              relationConfig
                .product_unique_id
                .label(product)
            )}
          </option>
        `
      )
      .join("");


  const body = `
    <div class="toolbar">

      <div>

        <b
          style="
            font:800 16px Manrope
          "
        >
          Product images
        </b>

        <span class="row-sub">
          Choose product instead
          of entering UUID manually.
        </span>

      </div>


      <div class="toolbar-actions">

        <button
          class="primary-btn"
          onclick="openCreate('images')"
        >
          ＋ Add image
        </button>

      </div>

    </div>


    <div class="panel">

      <div class="panel-body">

        <div
          style="
            display:flex;
            gap:8px;
            align-items:center;
          "
        >

          <select
            id="img-product-id"
            style="
              flex:1;
              padding:11px;
              border:1px solid var(--line);
              border-radius:10px;
            "
          >

            <option value="">
              Choose product
            </option>

            ${productOptions}

          </select>


          <button
            id="load-images"
            class="secondary-btn"
          >
            Load images
          </button>

        </div>

      </div>


      <div
        id="images-result"
      ></div>

    </div>
  `;


  $("#content")
    .innerHTML =
    body;


  $("#load-images")
    .onclick =
    async () => {

      const id =
        $("#img-product-id")
          .value
          .trim();


      if (!id) {
        toast(
          "Choose product",
          "Select a product first",
          "error"
        );

        return;
      }


      try {
        const rows =
          await api(
            `/product-images/product/${encodeURIComponent(id)}`
          );


        state.data.images =
          rows;


        $("#images-result")
          .innerHTML = `
            <div class="table-wrap">
              ${tableFor(
                "images",
                rows
              )}
            </div>
          `;

      } catch (e) {
        handlePageError(e);
      }
    };
}


// ============================================================
// ADMIN PROFILE
// ============================================================

async function renderProfile() {
  try {
    const profile =
      await api(
        "/admin/get"
      );


    state.user =
      profile;


    saveSession();

    setUserUI();


    $("#content")
      .innerHTML = `
        <div class="grid-2">

          <div class="panel">

            <div class="panel-head">

              <div>

                <h3>
                  Super Admin profile
                </h3>

                <p>
                  GET /admin/get
                </p>

              </div>


              <button
                class="primary-btn"
                onclick='editAdmin(
                  ${JSON.stringify(profile)}
                )'
              >
                Edit profile
              </button>

            </div>


            <div class="panel-body">

              <div class="activity-list">

                ${
                  Object.entries(profile)
                    .map(
                      ([key, value]) => `
                        <div class="activity-row">

                          <span
                            class="activity-dot"
                          ></span>

                          <div>

                            <b>
                              ${escapeHtml(
                                key.replaceAll("_", " ")
                              )}
                            </b>

                            <span>
                              ${escapeHtml(value)}
                            </span>

                          </div>

                        </div>
                      `
                    )
                    .join("")
                }

              </div>

            </div>

          </div>


          <div class="panel">

            <div class="panel-head">

              <div>

                <h3>
                  Danger zone
                </h3>

                <p>
                  Protected admin actions
                </p>

              </div>

            </div>


            <div class="panel-body">

              <div class="danger-box">
                Deleting the Super Admin
                can lock you out of
                protected administrative
                APIs.
              </div>

              <br>


              <button
                class="secondary-btn"
                style="color:#b3453f"
                onclick="deleteAdmin()"
              >
                Delete Super Admin
              </button>

            </div>

          </div>

        </div>
      `;

  } catch (e) {
    handlePageError(e);
  }
}


// ============================================================
// EDIT ADMIN
// ============================================================

async function editAdmin(profile) {
  const body =
    await formFields(
      "UserUpdate",
      {
        name:
          profile.name,

        updated_at:
          new Date()
            .toISOString()
            .slice(0, 16),
      }
    );


  openModal({
    title:
      "Edit Super Admin",

    body,

    onSubmit:
      async (data) => {

        if (
          data.updated_at
        ) {
          data.updated_at =
            new Date(
              data.updated_at
            ).toISOString();
        }


        await api(
          "/admin/update",
          {
            method:
              "PATCH",

            body:
              JSON.stringify(
                data
              ),
          }
        );


        toast(
          "Admin updated"
        );


        closeModal();

        navigate(
          "profile"
        );
      },
  });
}


// ============================================================
// DELETE ADMIN
// ============================================================

function deleteAdmin() {
  openModal({
    title:
      "Delete Super Admin",

    kicker:
      "DANGER ZONE",

    body: `
      <div class="danger-box full">

        This calls
        DELETE /admin/delete.

        Make sure you understand
        your backend lifecycle
        before continuing.

      </div>
    `,

    submit:
      "Delete Admin",

    onSubmit:
      async () => {

        await api(
          "/admin/delete",
          {
            method:
              "DELETE",
          }
        );


        logout();
      },
  });
}


// ============================================================
// API CONSOLE
// ============================================================

async function renderConsole() {
  const spec =
    await loadSpec();


  const groups = {};


  for (
    const [path, operations]
    of Object.entries(
      spec.paths
    )
  ) {
    for (
      const [method, operation]
      of Object.entries(
        operations
      )
    ) {
      if (
        ![
          "get",
          "post",
          "patch",
          "delete",
          "put",
        ].includes(method)
      ) {
        continue;
      }


      const tag =
        (
          operation.tags ||
          ["Other"]
        )[0];


      (
        groups[tag] ??= []
      ).push({
        path,
        method,
        op:
          operation,
      });
    }
  }


  $("#content")
    .innerHTML = `
      <div class="toolbar">

        <div class="search">

          <input
            id="api-search"
            placeholder="Search all ${
              Object.values(groups)
                .flat()
                .length
            } API operations..."
          >

        </div>


        <div class="toolbar-actions">

          <span class="badge role">
            OpenAPI
            ${escapeHtml(
              spec.openapi
            )}
          </span>

        </div>

      </div>


      <div id="api-groups">
        ${consoleGroups(groups)}
      </div>
    `;


  $("#api-search")
    .oninput =
    (e) => {

      const q =
        e.target.value
          .toLowerCase();


      const filteredGroups =
        {};


      for (
        const [tag, rows]
        of Object.entries(
          groups
        )
      ) {
        const filtered =
          rows.filter(
            (x) =>
              (
                x.path +
                " " +
                x.method +
                " " +
                (x.op.summary || "") +
                " " +
                tag
              )
                .toLowerCase()
                .includes(q)
          );


        if (
          filtered.length
        ) {
          filteredGroups[tag] =
            filtered;
        }
      }


      $("#api-groups")
        .innerHTML =
        consoleGroups(
          filteredGroups
        );
    };
}


// ============================================================
// API GROUPS
// ============================================================

function consoleGroups(
  groups
) {
  return (
    Object.entries(groups)
      .map(
        ([tag, rows]) => `
          <div class="panel api-group">

            <div class="panel-head">

              <div>

                <h3>
                  ${escapeHtml(tag)}
                </h3>

                <p>
                  ${rows.length}
                  operations
                </p>

              </div>

            </div>


            ${
              rows
                .map(
                  (x) => `
                    <div class="api-row">

                      <span
                        class="method ${x.method}"
                      >
                        ${x.method.toUpperCase()}
                      </span>


                      <div>

                        <span class="api-path">
                          ${escapeHtml(
                            x.path
                          )}
                        </span>

                        <span class="api-summary">
                          ${escapeHtml(
                            x.op.summary ||
                            ""
                          )}
                        </span>

                      </div>


                      <button
                        class="action-btn"
                        onclick='invokeApi(
                          ${JSON.stringify(x.path)},
                          ${JSON.stringify(x.method)},
                          ${JSON.stringify(
                            x.op.requestBody
                              ?.content
                              ?.["application/json"]
                              ?.schema
                              ?.$ref
                              ?.split("/")
                              .pop() ||
                            ""
                          )}
                        )'
                      >
                        Run
                      </button>

                    </div>
                  `
                )
                .join("")
            }

          </div>
        `
      )
      .join("") ||

    `
      <div class="empty">
        <b>
          No API operation matched
        </b>
      </div>
    `
  );
}


// ============================================================
// API CONSOLE PARAM FIELD
//
// Also replaces path UUID values with dropdowns when possible.
// ============================================================

async function pathParamHtml(
  parameterName
) {
  // path_ prefix will be added to form field
  // but relationConfig uses original field name.

  if (
    relationConfig[
      parameterName
    ]
  ) {
    await loadRelation(
      parameterName
    );


    const config =
      relationConfig[
        parameterName
      ];


    const rows =
      state.relations[
        config.cache
      ] || [];


    return `
      <label class="field">

        <span>
          ${parameterName.replaceAll("_", " ")}
          *
        </span>


        <select
          name="path_${parameterName}"
          required
        >

          <option value="">
            ${config.placeholder}
          </option>


          ${
            rows
              .map(
                (row) => `
                  <option
                    value="${escapeHtml(row.unique_id)}"
                  >
                    ${escapeHtml(
                      config.label(row)
                    )}
                  </option>
                `
              )
              .join("")
          }

        </select>

      </label>
    `;
  }


  return `
    <label class="field">

      <span>
        ${parameterName.replaceAll("_", " ")}
        *
      </span>

      <input
        name="path_${parameterName}"
        required
      >

    </label>
  `;
}


// ============================================================
// RUN API
// ============================================================

async function invokeApi(
  path,
  method,
  schemaName
) {
  const params =
    [
      ...path.matchAll(
        /\{([^}]+)\}/g
      ),
    ].map(
      (match) =>
        match[1]
    );


  const paramParts =
    await Promise.all(
      params.map(
        (param) =>
          pathParamHtml(
            param
          )
      )
    );


  const paramFields =
    paramParts.join("");


  const requestBody =
    schemaName
      ? await formFields(
          schemaName
        )
      : "";


  openModal({
    title:
      `${method.toUpperCase()} ${path}`,

    kicker:
      "API CONSOLE",

    body:
      paramFields +
      requestBody +
      (
        requestBody
          ? ""
          : `
            <div
              class="full muted"
              style="
                font-size:11px;
              "
            >
              This operation has no
              JSON request body in
              the OpenAPI schema.
            </div>
          `
      ),

    submit:
      "Run request",

    onSubmit:
      async (data) => {

        let resolvedPath =
          path;


        for (
          const name
          of params
        ) {
          resolvedPath =
            resolvedPath.replace(
              `{${name}}`,
              encodeURIComponent(
                data[
                  `path_${name}`
                ]
              )
            );


          delete data[
            `path_${name}`
          ];
        }


        const options = {
          method:
            method.toUpperCase(),
        };


        if (
          ![
            "GET",
            "DELETE",
          ].includes(
            options.method
          ) &&
          Object.keys(data)
            .length
        ) {
          options.body =
            JSON.stringify(
              data
            );
        }


        try {
          const result =
            await api(
              resolvedPath,
              options
            );


          $("#modal-body")
            .innerHTML = `
              <div class="full">

                <pre
                  style="
                    white-space:pre-wrap;
                    max-height:55vh;
                    overflow:auto;
                    font-size:11px;
                    background:#f6f8f6;
                    padding:14px;
                    border-radius:12px;
                  "
                >${escapeHtml(
                  JSON.stringify(
                    result,
                    null,
                    2
                  )
                )}</pre>

              </div>
            `;


          $("#modal-submit")
            .textContent =
            "Close";


          state.modal.onSubmit =
            async () =>
              closeModal();

        } catch (e) {
          if (
            [401, 403]
              .includes(e.status)
          ) {
            closeModal();

            renderUnauthorized(
              e
            );
          }

          else {
            toast(
              "API request failed",
              e.message,
              "error"
            );
          }
        }
      },
  });
}


// ============================================================
// RAW RESPONSE
// ============================================================

function showRaw(data) {
  openModal({
    title:
      "Record details",

    kicker:
      "RAW API RESPONSE",

    body: `
      <div class="full">

        <pre
          style="
            white-space:pre-wrap;
            max-height:60vh;
            overflow:auto;
            font-size:11px;
            background:#f6f8f6;
            padding:14px;
            border-radius:12px;
          "
        >${escapeHtml(
          JSON.stringify(
            data,
            null,
            2
          )
        )}</pre>

      </div>
    `,

    submit:
      "Close",

    onSubmit:
      async () =>
        closeModal(),
  });
}


// ============================================================
// LOGOUT
// ============================================================

function logout() {
  sessionStorage.removeItem(
    "blink_access"
  );

  sessionStorage.removeItem(
    "blink_refresh"
  );

  sessionStorage.removeItem(
    "blink_user"
  );


  state.access =
    "";

  state.refresh =
    "";

  state.user =
    null;

  state.relations =
    {};


  $("#app-view")
    .classList
    .add("hidden");


  $("#login-view")
    .classList
    .remove("hidden");
}


// ============================================================
// EVENT LISTENERS
// ============================================================

$("#login-form")
  .addEventListener(
    "submit",
    login
  );


$("#base-url")
  .value =
  state.base;


$("#toggle-password")
  .onclick =
  () => {
    $("#login-password")
      .type =
      $("#login-password")
        .type === "password"
        ? "text"
        : "password";
  };


$("#logout-btn")
  .onclick =
  logout;


$("#refresh-page")
  .onclick =
  () =>
    navigate(
      state.page
    );


$("#menu-btn")
  .onclick =
  () =>
    $("#sidebar")
      .classList
      .toggle("open");


$$("[data-close-modal]")
  .forEach(
    (element) => {
      element.onclick =
        closeModal;
    }
  );


// ============================================================
// MODAL FORM SUBMIT
// ============================================================

$("#modal-form")
  .onsubmit =
  async (event) => {
    event.preventDefault();


    if (
      !state.modal?.onSubmit
    ) {
      return;
    }


    const button =
      $("#modal-submit");


    const oldText =
      button.textContent;


    button.disabled =
      true;


    button.textContent =
      "Working…";


    try {
      await state.modal.onSubmit(
        formObject(
          event.target
        )
      );
    } catch (err) {

      if (
        [401, 403]
          .includes(
            err.status
          )
      ) {
        closeModal();

        renderUnauthorized(
          err
        );
      }

      else {
        toast(
          "Request failed",
          err.message,
          "error"
        );
      }

    } finally {

      button.disabled =
        false;


      if (
        !$("#modal")
          .classList
          .contains("hidden")
      ) {
        button.textContent =
          oldText;
      }
    }
  };


// ============================================================
// AUTO LOGIN IF TOKEN EXISTS
// ============================================================

if (
  state.access
) {
  showApp();
}