const $ = (s, root=document) => root.querySelector(s);
const $$ = (s, root=document) => [...root.querySelectorAll(s)];

const state = {
  apiUrl: localStorage.getItem("blinkit_customer_api") || "http://127.0.0.1:8000",
  accessToken: localStorage.getItem("blinkit_customer_access") || "",
  refreshToken: localStorage.getItem("blinkit_customer_refresh") || "",
  customerId: localStorage.getItem("blinkit_customer_id") || "",
  customer: safeJSON(localStorage.getItem("blinkit_customer_profile")) || null,
  branch: safeJSON(localStorage.getItem("blinkit_customer_branch")) || null,
  branches: [],
  catalog: [],
  cart: null,
  orders: [],
  selectedAddressId: localStorage.getItem("blinkit_customer_address") || "",
  category: "all",
  search: "",
  sort: "featured",
};

function safeJSON(v){ try { return JSON.parse(v) } catch { return null } }
function money(v){ const n=Number(v||0); return `₹${Number.isInteger(n)?n:n.toFixed(2)}` }
function escapeHTML(v=""){ return String(v).replace(/[&<>"']/g, m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m])) }
function toast(message, type="success"){
  const el=document.createElement("div"); el.className=`toast ${type}`; el.textContent=message;
  $("#toastHost").appendChild(el); setTimeout(()=>el.remove(),3600);
}
function tokenPayload(token){
  try{
    const p=token.split(".")[1]; if(!p) return {};
    const normalized=p.replace(/-/g,"+").replace(/_/g,"/");
    return JSON.parse(decodeURIComponent(atob(normalized).split("").map(c=>"%"+("00"+c.charCodeAt(0).toString(16)).slice(-2)).join("")));
  }catch{return {}}
}
function inferCustomerId(){
  if(state.customerId) return state.customerId;
  if(state.customer?.unique_id) return state.customer.unique_id;
  const p=tokenPayload(state.accessToken);
  const candidates=[p.customer_unique_id,p.unique_id,p.user_id,p.sub,p.id];
  const id=candidates.find(v=>typeof v==="string" && v.length>10);
  if(id){ state.customerId=id; localStorage.setItem("blinkit_customer_id",id); }
  return state.customerId;
}
async function api(path, options={}, retry=true){
  const headers={"Content-Type":"application/json",...(options.headers||{})};
  if(state.accessToken) headers.Authorization=`Bearer ${state.accessToken}`;
  let res;
  try{ res=await fetch(`${state.apiUrl.replace(/\/$/,"")}${path}`,{...options,headers}); }
  catch(e){ throw new Error("Network error. Check backend URL, CORS, and server status.") }
  if(res.status===401 && retry && state.refreshToken){
    const ok=await refreshAccess();
    if(ok) return api(path,options,false);
  }
  let body=null; const text=await res.text();
  if(text){ try{body=JSON.parse(text)}catch{body=text} }
  if(!res.ok){
    const detail=typeof body==="object" ? (body?.detail ? JSON.stringify(body.detail) : JSON.stringify(body)) : body;
    const err=new Error(detail || `HTTP ${res.status}`); err.status=res.status; throw err;
  }
  return body;
}
async function refreshAccess(){
  try{
    const res=await fetch(`${state.apiUrl.replace(/\/$/,"")}/auth/refresh`,{
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({refresh_token:state.refreshToken})
    });
    if(!res.ok) return false;
    const data=await res.json();
    state.accessToken=data.access_token; if(data.refresh_token) state.refreshToken=data.refresh_token;
    localStorage.setItem("blinkit_customer_access",state.accessToken);
    if(state.refreshToken) localStorage.setItem("blinkit_customer_refresh",state.refreshToken);
    return true;
  }catch{return false}
}
function persistAuth(){
  localStorage.setItem("blinkit_customer_api",state.apiUrl);
  localStorage.setItem("blinkit_customer_access",state.accessToken);
  localStorage.setItem("blinkit_customer_refresh",state.refreshToken);
  if(state.customerId) localStorage.setItem("blinkit_customer_id",state.customerId);
  if(state.customer) localStorage.setItem("blinkit_customer_profile",JSON.stringify(state.customer));
}
function showLoggedInUI(){
  $("#guestHero").classList.toggle("hidden",!!state.accessToken);
  $("#shopView").classList.toggle("hidden",!state.accessToken);
  $("#accountText").textContent=state.customer?.name?.split(" ")[0] || (state.accessToken?"Account":"Login");
  $("#profileName").textContent=state.customer?.name || "Customer";
  $("#profileEmail").textContent=state.customer?.email || "Authenticated customer";
  $("#profileRole").textContent=state.customer?.role || tokenPayload(state.accessToken)?.role || "customer";
  $("#settingsApiUrl").value=state.apiUrl;
  $("#settingsCustomerId").value=inferCustomerId() || "";
  updateBranchHeader();
}
function openDrawer(id){
  $("#overlay").classList.add("show"); $("#"+id).classList.add("open");
}
function closeDrawers(){
  $("#overlay").classList.remove("show"); $$(".drawer.open").forEach(x=>x.classList.remove("open"));
}
function openDialog(id){ const d=$("#"+id); if(!d.open)d.showModal() }
function updateBranchHeader(){
  if(state.branch){
    $("#deliveryTitle").textContent=state.branch.name;
    $("#deliverySub").textContent=`${state.branch.city} · ${state.branch.pincode}`;
  }else{
    $("#deliveryTitle").textContent="Select a branch"; $("#deliverySub").textContent="Choose where you want to shop";
  }
}

async function login(email,password){
  const data=await api("/auth/login",{method:"POST",body:JSON.stringify({email,password})},false);
  state.accessToken=data.access_token; state.refreshToken=data.refresh_token;
  inferCustomerId(); persistAuth(); showLoggedInUI();
  await bootstrapCustomer();
}
async function bootstrapCustomer(){
  try{ await loadBranches(); }catch(e){toast(readableError(e),"error")}
  if(state.branch){ await loadCatalog(); await loadCart(); }
  if(inferCustomerId()) await loadCustomerProfile();
}
async function loadCustomerProfile(){
  const id=inferCustomerId(); if(!id)return;
  try{
    const customer=await api(`/customers/${encodeURIComponent(id)}/details`);
    state.customer=customer; localStorage.setItem("blinkit_customer_profile",JSON.stringify(customer)); showLoggedInUI(); renderAddresses(customer.addresses||[]);
  }catch(e){
    $("#addressHint").textContent=`Profile endpoint unavailable for this token: ${readableError(e)}`;
  }
}
async function loadBranches(){
  state.branches=await api("/branches/") || [];
  renderBranches();
  if(!state.branch){
    const active=state.branches.filter(b=>b.is_active!==false);
    if(active.length===1){ await selectBranch(active[0]); }
    else if(active.length>0) openDialog("branchModal");
  }
}
function renderBranches(){
  const list=$("#branchList"); list.innerHTML="";
  const active=state.branches.filter(b=>b.is_active!==false);
  if(!active.length){list.innerHTML='<div class="hint-card">No active branches returned by the API.</div>';return}
  active.forEach(b=>{
    const btn=document.createElement("button");btn.className="branch-option";
    btn.innerHTML=`<span><b>${escapeHTML(b.name)}</b><small>${escapeHTML(b.address)}, ${escapeHTML(b.city)} · ${escapeHTML(b.pincode)}</small></span><span>Choose →</span>`;
    btn.onclick=()=>selectBranch(b); list.appendChild(btn);
  })
}
async function selectBranch(branch){
  state.branch=branch; localStorage.setItem("blinkit_customer_branch",JSON.stringify(branch)); updateBranchHeader();
  $("#branchModal").close();
  try{
    await ensureCartForBranch();
    await loadCatalog();
  }catch(e){toast(readableError(e),"error")}
}
async function ensureCartForBranch(){
  let current=null;
  try{ current=await api("/cart"); }catch(e){ if(e.status!==404){} }
  if(current?.branch?.unique_id && current.branch.unique_id!==state.branch.unique_id){
    try{await api("/cart/delete",{method:"DELETE"})}catch{}
    current=null;
  }
  if(!current){
    try{ current=await api("/cart",{method:"POST",body:JSON.stringify({branch_unique_id:state.branch.unique_id})}); }
    catch(e){
      // Some backends may return existing cart on GET but a non-404 on missing state; surface meaningful issue.
      if(e.status!==409) throw e;
      current=await api("/cart");
    }
  }
  state.cart=current; renderCart();
}
async function loadCatalog(){
  if(!state.branch)return;
  $("#catalogStatus").textContent="Loading live catalog…";
  try{
    state.catalog=await api(`/branch-catalog/${encodeURIComponent(state.branch.unique_id)}`)||[];
    $("#catalogStatus").textContent=`${state.branch.name} catalog loaded`;
    renderCategories(); renderProducts();
  }catch(e){
    $("#catalogStatus").textContent="Catalog load failed"; state.catalog=[]; renderCategories(); renderProducts(); throw e;
  }
}
function catalogCategories(){
  const map=new Map();
  state.catalog.forEach(p=>{
    const s=p.subcategory;
    if(s?.unique_id && !map.has(s.unique_id)) map.set(s.unique_id,{id:s.unique_id,name:s.name,slug:s.slug,count:0});
    if(s?.unique_id) map.get(s.unique_id).count++;
  });
  return [...map.values()];
}
function renderCategories(){
  const rail=$("#categoryRail"); rail.innerHTML="";
  const cats=[{id:"all",name:"All items",count:state.catalog.length},...catalogCategories()];
  const icons=["🛍️","🥛","🍪","🥤","🧀","🧼","🍚","🥦"];
  cats.forEach((c,i)=>{
    const b=document.createElement("button"); b.className=`category-pill ${state.category===c.id?"active":""}`;
    b.innerHTML=`<span class="cat-icon">${icons[i%icons.length]}</span><b>${escapeHTML(c.name)}</b><small>${c.count} products</small>`;
    b.onclick=()=>{state.category=c.id;renderCategories();renderProducts()}; rail.appendChild(b);
  })
}
function filteredProducts(){
  let arr=[...state.catalog];
  if(state.category!=="all") arr=arr.filter(p=>p.subcategory?.unique_id===state.category);
  const q=state.search.trim().toLowerCase();
  if(q) arr=arr.filter(p=>[p.name,p.description,p.brand?.name,p.subcategory?.name].some(v=>String(v||"").toLowerCase().includes(q)));
  const firstPrice=p=>Number((p.variants||[]).find(v=>v.is_available!==false)?.selling_price || Infinity);
  if(state.sort==="price-asc")arr.sort((a,b)=>firstPrice(a)-firstPrice(b));
  if(state.sort==="price-desc")arr.sort((a,b)=>firstPrice(b)-firstPrice(a));
  if(state.sort==="name")arr.sort((a,b)=>a.name.localeCompare(b.name));
  return arr;
}
function primaryImage(p){return (p.images||[]).find(i=>i.is_primary)?.image_url || (p.images||[])[0]?.image_url || ""}
function renderProducts(){
  const arr=filteredProducts(), grid=$("#productGrid"); grid.innerHTML="";
  $("#catalogCount").textContent=`${arr.length} items`;
  const category=catalogCategories().find(c=>c.id===state.category);
  $("#catalogTitle").textContent=category?.name || (state.search?`Results for “${state.search}”`:"All products");
  $("#emptyCatalog").classList.toggle("hidden",arr.length>0);
  arr.forEach((p,index)=>{
    const available=(p.variants||[]).filter(v=>v.is_available!==false);
    const v=available[0] || (p.variants||[])[0];
    const mrp=Number(v?.mrp||0), sell=Number(v?.selling_price||0), discount=mrp>sell&&mrp?Math.round((mrp-sell)*100/mrp):0;
    const card=document.createElement("article");card.className="product-card";
    const img=primaryImage(p);
    card.innerHTML=`
      <div class="product-image" data-product-open="${escapeHTML(p.unique_id)}">
        ${img?`<img src="${escapeHTML(img)}" alt="${escapeHTML(p.name)}" onerror="this.style.display='none';this.nextElementSibling.style.display='block'"><span class="fallback" style="display:none">🛍️</span>`:`<span class="fallback">🛍️</span>`}
        ${discount?`<span class="discount-chip">${discount}% OFF</span>`:""}
      </div>
      <span class="time">⚡ QUICK PICK</span>
      <h3>${escapeHTML(p.name)}</h3>
      <p class="brand-name">${escapeHTML(p.brand?.name||"")} · ${escapeHTML(p.subcategory?.name||"")}</p>
      <select class="variant-select" data-product="${escapeHTML(p.unique_id)}">
        ${(p.variants||[]).map(x=>`<option value="${escapeHTML(x.unique_id)}" ${x.is_available===false?"disabled":""}>${escapeHTML(x.value)} ${escapeHTML(x.unit)} ${x.is_available===false?"— unavailable":""}</option>`).join("")}
      </select>
      <div class="price-add">
        <div class="price"><strong data-price-for="${escapeHTML(p.unique_id)}">${v?money(v.selling_price):"—"}</strong>${mrp>sell?`<del data-mrp-for="${escapeHTML(p.unique_id)}">${money(v.mrp)}</del>`:"<del></del>"}</div>
        <button class="add-btn" data-add="${escapeHTML(p.unique_id)}" ${!available.length?"disabled":""}>ADD</button>
      </div>`;
    grid.appendChild(card);
  });
  $$("[data-product-open]").forEach(el=>el.onclick=()=>openProduct(el.dataset.productOpen));
  $$(".variant-select").forEach(sel=>sel.onchange=()=>{
    const p=state.catalog.find(x=>x.unique_id===sel.dataset.product),v=p?.variants?.find(x=>x.unique_id===sel.value);
    const pc=sel.closest(".product-card");
    $(`[data-price-for="${CSS.escape(sel.dataset.product)}"]`,pc).textContent=money(v?.selling_price);
    const del=$(`[data-mrp-for="${CSS.escape(sel.dataset.product)}"]`,pc); if(del)del.textContent=Number(v?.mrp)>Number(v?.selling_price)?money(v?.mrp):"";
  });
  $$("[data-add]").forEach(btn=>btn.onclick=async()=>{
    const card=btn.closest(".product-card"),sel=$(".variant-select",card);
    await addToCart(sel.value,1);
  });
}
function openProduct(id){
  const p=state.catalog.find(x=>x.unique_id===id); if(!p)return;
  const variants=p.variants||[]; const img=primaryImage(p);
  $("#productModalBody").innerHTML=`<div class="product-detail">
    <div class="detail-image">${img?`<img src="${escapeHTML(img)}" alt="${escapeHTML(p.name)}">`:`<span class="fallback">🛍️</span>`}</div>
    <div class="detail-info"><p class="eyebrow">${escapeHTML(p.brand?.name||"Product")}</p><h2>${escapeHTML(p.name)}</h2>
    <p class="description">${escapeHTML(p.description||"Freshly available from your selected branch catalog.")}</p>
    <div class="variant-stack">${variants.map((v,i)=>`<label class="variant-option ${i===0?"selected":""}"><span><input type="radio" name="detailVariant" value="${escapeHTML(v.unique_id)}" ${i===0?"checked":""} ${v.is_available===false?"disabled":""}> <b>${escapeHTML(v.value)} ${escapeHTML(v.unit)}</b><br><small>${escapeHTML(v.sku)}</small></span><strong>${money(v.selling_price)}</strong></label>`).join("")}</div>
    <button id="detailAddBtn" class="primary-btn full" ${!variants.some(v=>v.is_available!==false)?"disabled":""}>Add to cart</button></div></div>`;
  $$('input[name="detailVariant"]').forEach(r=>r.onchange=()=>{$$(".variant-option").forEach(x=>x.classList.remove("selected"));r.closest(".variant-option").classList.add("selected")});
  $("#detailAddBtn").onclick=async()=>{const r=$('input[name="detailVariant"]:checked');if(r){await addToCart(r.value,1);$("#productModal").close()}};
  openDialog("productModal");
}
async function addToCart(variantId,quantity){
  if(!state.branch){openDialog("branchModal");return}
  try{
    await ensureCartForBranch();
    await api("/cart/items",{method:"POST",body:JSON.stringify({product_variant_unique_id:variantId,quantity})});
    await loadCart(); toast("Added to cart");
  }catch(e){toast(readableError(e),"error")}
}
async function loadCart(){
  if(!state.accessToken)return;
  try{state.cart=await api("/cart");}catch(e){if(e.status===404)state.cart=null;else throw e}
  renderCart();
}
function cartTotals(){
  const items=state.cart?.items||[];
  let total=0,count=0;
  items.forEach(i=>{const v=i.product_variant||{};total+=Number(v.selling_price||0)*Number(i.quantity||0);count+=Number(i.quantity||0)});
  return {total,count};
}
function renderCart(){
  const items=state.cart?.items||[],host=$("#cartItems");host.innerHTML="";
  items.forEach(i=>{
    const v=i.product_variant||{},row=document.createElement("div");row.className="cart-item";
    row.innerHTML=`<div class="cart-thumb">🛍️</div><div class="cart-copy"><b>${escapeHTML(v.sku||"Product")}</b><small>${escapeHTML(v.value||"")} ${escapeHTML(v.unit||"")}</small><div class="cart-price">${money(Number(v.selling_price||0)*i.quantity)}</div></div><div class="qty-control"><button data-minus="${escapeHTML(v.unique_id)}">−</button><span>${i.quantity}</span><button data-plus="${escapeHTML(v.unique_id)}">+</button></div>`;
    host.appendChild(row);
  });
  const {total,count}=cartTotals();
  $("#cartMeta").textContent=`${count} item${count===1?"":"s"}`;$("#cartTotal").textContent=money(total);
  $("#billSubtotal").textContent=money(total);$("#billTotal").textContent=money(total);$("#checkoutTotal").textContent=`${money(total)} →`;
  $("#cartEmpty").classList.toggle("hidden",items.length>0);$("#cartSummary").classList.toggle("hidden",!items.length);
  if(state.cart?.branch){$("#cartBranchNote").textContent=`Shopping from ${state.cart.branch.name}, ${state.cart.branch.city}`;$("#cartBranchNote").classList.remove("hidden")}
  else $("#cartBranchNote").classList.add("hidden");
  $$("[data-minus]").forEach(b=>b.onclick=()=>changeQty(b.dataset.minus,-1));
  $$("[data-plus]").forEach(b=>b.onclick=()=>changeQty(b.dataset.plus,1));
}
async function changeQty(variantId,delta){
  const item=(state.cart?.items||[]).find(i=>i.product_variant?.unique_id===variantId); if(!item)return;
  const next=item.quantity+delta;
  try{
    if(next<=0) await api(`/cart/items/${encodeURIComponent(variantId)}`,{method:"DELETE"});
    else await api(`/cart/items/${encodeURIComponent(variantId)}`,{method:"PATCH",body:JSON.stringify({quantity:next})});
    await loadCart();
  }catch(e){toast(readableError(e),"error")}
}
function renderAddresses(addresses){
  const list=$("#addressList");list.innerHTML="";
  if(!addresses?.length){
    state.selectedAddressId="";
    localStorage.removeItem("blinkit_customer_address");
    list.innerHTML='<div class="hint-card">No saved addresses yet. Add an address before checkout.</div>';
    return;
  }

  // Keep selected address if it still exists; otherwise prefer default address.
  const selectedStillExists=addresses.some(a=>a.unique_id===state.selectedAddressId);
  if(!selectedStillExists){
    const preferred=addresses.find(a=>a.is_default) || addresses[0];
    state.selectedAddressId=preferred?.unique_id || "";
    if(state.selectedAddressId) localStorage.setItem("blinkit_customer_address",state.selectedAddressId);
  }

  addresses.forEach(a=>{
    const el=document.createElement("button");
    el.type="button";
    el.className=`address-card address-choice ${state.selectedAddressId===a.unique_id?"selected":""}`;
    el.dataset.addressId=a.unique_id || "";
    el.innerHTML=`
      <span>
        <b>${escapeHTML(a.label||"Address")} ${a.is_default?'<span class="default-chip">DEFAULT</span>':""}</b>
        <p>${escapeHTML(a.address_line||"")}${a.landmark?`, ${escapeHTML(a.landmark)}`:""}<br>${escapeHTML(a.city||"")}, ${escapeHTML(a.state||"")} · ${escapeHTML(a.pincode||"")}</p>
      </span>
      <span>${state.selectedAddressId===a.unique_id?"✓ Selected":"Use this"}</span>
    `;
    el.onclick=()=>{
      state.selectedAddressId=a.unique_id || "";
      if(state.selectedAddressId) localStorage.setItem("blinkit_customer_address",state.selectedAddressId);
      renderAddresses(state.customer?.addresses||[]);
      toast("Delivery address selected");
    };
    list.appendChild(el);
  });
}

function getSelectedAddress(){
  const addresses=state.customer?.addresses||[];
  return addresses.find(a=>a.unique_id===state.selectedAddressId) || null;
}

function readableError(e){
  let m=e?.message||String(e);
  try{
    const parsed=JSON.parse(m);
    if(Array.isArray(parsed)) return parsed.map(x=>x.msg||JSON.stringify(x)).join(", ");
    if(parsed?.detail)return String(parsed.detail);
  }catch{}
  return m.replace(/^"|"$/g,"");
}

$$("[data-open-auth]").forEach(b=>b.onclick=()=>{openDialog("authModal");switchAuth(b.dataset.openAuth)});
$$("[data-dialog-close]").forEach(b=>b.onclick=()=>$("#"+b.dataset.dialogClose).close());
$$("[data-close]").forEach(b=>b.onclick=closeDrawers);
$("#overlay").onclick=closeDrawers;
$("#accountBtn").onclick=()=>state.accessToken?openDrawer("accountDrawer"):openDialog("authModal");
$("#cartBtn").onclick=async()=>{if(!state.accessToken){openDialog("authModal");return}try{await loadCart()}catch(e){toast(readableError(e),"error")}openDrawer("cartDrawer")};
$("#locationBtn").onclick=async()=>{if(!state.accessToken){openDialog("authModal");return}if(!state.branches.length){try{await loadBranches()}catch(e){toast(readableError(e),"error")}}openDialog("branchModal")};
$("#checkoutBtn").onclick=()=>openCheckout();
// $("#clearCartBtn").onclick=async()=>{try{await api("/cart/clear",{method:"DELETE"});await loadCart();toast("Cart cleared")}catch(e){toast(readableError(e),"error")}};
$("#clearCartBtn").onclick = async () => {
  try {

    await api(
      "/cart/delete",
      {
        method: "DELETE"
      }
    );

    state.cart = null;

    if ("cartItems" in state) {
      state.cartItems = [];
    }

    toast(
      "Cart deleted successfully"
    );

    closeDrawers();

  } catch (e) {

    console.error(
      "Delete cart failed:",
      e
    );

    toast(
      readableError(e),
      "error"
    );
  }
};
$("#refreshCatalog").onclick=()=>loadCatalog().catch(e=>toast(readableError(e),"error"));
$("#searchInput").oninput=e=>{state.search=e.target.value;renderProducts()};
$("#sortSelect").onchange=e=>{state.sort=e.target.value;renderProducts()};
document.addEventListener("keydown",e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==="k"){e.preventDefault();$("#searchInput").focus()}});

function switchAuth(tab){
  $$("[data-auth-tab]").forEach(x=>x.classList.toggle("active",x.dataset.authTab===tab));
  $("#loginForm").classList.toggle("hidden",tab!=="login");$("#registerForm").classList.toggle("hidden",tab!=="register");
}
$$("[data-auth-tab]").forEach(b=>b.onclick=()=>switchAuth(b.dataset.authTab));
$("#loginForm").onsubmit=async e=>{
  e.preventDefault();const fd=new FormData(e.target),btn=$('button[type="submit"]',e.target);btn.disabled=true;btn.textContent="Logging in…";
  try{await login(fd.get("email"),fd.get("password"));$("#authModal").close();toast("Welcome back!")}
  catch(err){toast(readableError(err),"error")}finally{btn.disabled=false;btn.textContent="Login"}
};
$("#registerForm").onsubmit=async e=>{
  e.preventDefault();const fd=new FormData(e.target),btn=$('button[type="submit"]',e.target);btn.disabled=true;btn.textContent="Creating…";
  const payload={name:fd.get("name"),email:fd.get("email"),phone:fd.get("phone"),password:fd.get("password")};
  try{
    const customer=await api("/customers/register",{method:"POST",body:JSON.stringify(payload)},false);
    state.customer=customer;state.customerId=customer.unique_id||"";persistAuth();
    await login(payload.email,payload.password);$("#authModal").close();toast("Account created successfully");
  }catch(err){toast(readableError(err),"error")}finally{btn.disabled=false;btn.textContent="Create account"}
};
$("#addAddressBtn").onclick=()=>{if(!inferCustomerId()){toast("Customer unique ID is required for address APIs.","error");return}openDialog("addressModal")};
$("#addressForm").onsubmit=async e=>{
  e.preventDefault();const id=inferCustomerId();if(!id){toast("Set your customer unique ID first.","error");return}
  const fd=new FormData(e.target),payload={label:fd.get("label"),address_line:fd.get("address_line"),landmark:fd.get("landmark")||null,city:fd.get("city"),state:fd.get("state"),pincode:fd.get("pincode"),is_default:fd.get("is_default")==="on"};
  try{await api(`/customers/${encodeURIComponent(id)}/addresses`,{method:"POST",body:JSON.stringify(payload)});$("#addressModal").close();e.target.reset();await loadCustomerProfile();toast("Address saved")}
  catch(err){toast(readableError(err),"error")}
};
$("#saveSettingsBtn").onclick=async()=>{
  state.apiUrl=$("#settingsApiUrl").value.trim().replace(/\/$/,"");state.customerId=$("#settingsCustomerId").value.trim();
  localStorage.setItem("blinkit_customer_api",state.apiUrl);localStorage.setItem("blinkit_customer_id",state.customerId);toast("Settings saved");
  if(state.accessToken){await bootstrapCustomer()}
};
$("#logoutBtn").onclick=()=>{
  ["blinkit_customer_access","blinkit_customer_refresh","blinkit_customer_id","blinkit_customer_profile","blinkit_customer_branch","blinkit_customer_address"].forEach(k=>localStorage.removeItem(k));
  state.accessToken="";state.refreshToken="";state.customerId="";state.customer=null;state.branch=null;state.cart=null;state.catalog=[];state.orders=[];state.selectedAddressId="";
  closeDrawers();showLoggedInUI();renderCart();toast("Logged out");
};


// ============================================================
// CUSTOMER ORDERS + CHECKOUT
// ============================================================

function ensureOrdersUI(){
  if($("#customerCheckoutModal")) return;

  const style=document.createElement("style");
  style.textContent=`
    .address-choice{width:100%;text-align:left;display:flex;justify-content:space-between;gap:14px;align-items:center;cursor:pointer}
    .address-choice.selected{outline:2px solid #0c831f;outline-offset:1px}
    .orders-toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:10px 0 16px}
    .orders-list{display:grid;gap:12px}
    .order-card{border:1px solid #e7e7e7;border-radius:14px;padding:14px;background:#fff}
    .order-card-top,.order-card-actions,.order-row,.checkout-row{display:flex;justify-content:space-between;gap:12px;align-items:center}
    .order-card-top{margin-bottom:10px}
    .order-card small,.order-detail small{color:#777}
    .order-status{font-size:12px;font-weight:800;text-transform:uppercase;padding:5px 9px;border-radius:999px;background:#f1f3f5}
    .order-card-actions{margin-top:12px;flex-wrap:wrap}
    .order-card-actions button{cursor:pointer}
    .order-detail-items{display:grid;gap:9px;margin:14px 0}
    .order-item{padding:10px 0;border-bottom:1px solid #eee}
    .order-summary-box{border-top:1px solid #eee;margin-top:14px;padding-top:12px;display:grid;gap:8px}
    .order-total-row{font-size:17px;font-weight:800}
    .checkout-address{padding:12px;border:1px solid #e7e7e7;border-radius:12px;margin:12px 0}
    .checkout-note{width:100%;min-height:78px;resize:vertical;padding:10px;border:1px solid #ddd;border-radius:10px;box-sizing:border-box}
    .checkout-payment{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px}
    .order-empty{text-align:center;padding:28px 12px;color:#777}
    .order-modal-box{min-width:min(560px,92vw);max-width:680px}
    .order-modal-scroll{max-height:68vh;overflow:auto}
  `;
  document.head.appendChild(style);

  const checkout=document.createElement("dialog");
  checkout.id="customerCheckoutModal";
  checkout.innerHTML=`
    <div class="order-modal-box">
      <div class="dialog-head">
        <div>
          <p class="eyebrow">CHECKOUT</p>
          <h2>Place your order</h2>
        </div>
        <button type="button" data-order-dialog-close="customerCheckoutModal">×</button>
      </div>

      <div id="customerCheckoutBody"></div>

      <div style="display:flex;gap:10px;justify-content:flex-end;margin-top:16px">
        <button type="button" class="secondary-btn" data-order-dialog-close="customerCheckoutModal">Cancel</button>
        <button type="button" class="primary-btn" id="placeOrderBtn">Place order</button>
      </div>
    </div>
  `;
  document.body.appendChild(checkout);

  const orders=document.createElement("dialog");
  orders.id="customerOrdersModal";
  orders.innerHTML=`
    <div class="order-modal-box">
      <div class="dialog-head">
        <div>
          <p class="eyebrow">YOUR PURCHASES</p>
          <h2>My Orders</h2>
        </div>
        <button type="button" data-order-dialog-close="customerOrdersModal">×</button>
      </div>

      <div class="orders-toolbar">
        <span id="ordersMeta">Loading…</span>
        <button type="button" class="secondary-btn" id="refreshOrdersBtn">Refresh</button>
      </div>

      <div class="order-modal-scroll">
        <div id="customerOrdersList" class="orders-list"></div>
      </div>
    </div>
  `;
  document.body.appendChild(orders);

  const detail=document.createElement("dialog");
  detail.id="customerOrderDetailModal";
  detail.innerHTML=`
    <div class="order-modal-box">
      <div class="dialog-head">
        <div>
          <p class="eyebrow">ORDER DETAILS</p>
          <h2 id="orderDetailTitle">Order</h2>
        </div>
        <button type="button" data-order-dialog-close="customerOrderDetailModal">×</button>
      </div>
      <div id="customerOrderDetailBody" class="order-modal-scroll"></div>
    </div>
  `;
  document.body.appendChild(detail);

  $$("[data-order-dialog-close]").forEach(btn=>{
    btn.onclick=()=>$("#"+btn.dataset.orderDialogClose)?.close();
  });

  $("#placeOrderBtn").onclick=submitOrderFromCheckout;
  $("#refreshOrdersBtn").onclick=()=>loadMyOrders().catch(e=>toast(readableError(e),"error"));

  // Add "My Orders" shortcut to the existing account drawer if available.
  const account=$("#accountDrawer");
  if(account && !$("#myOrdersBtn")){
    const btn=document.createElement("button");
    btn.id="myOrdersBtn";
    btn.type="button";
    btn.className="secondary-btn full";
    btn.style.marginTop="10px";
    btn.textContent="My Orders";
    btn.onclick=openMyOrders;
    const logout=$("#logoutBtn");
    if(logout?.parentNode) logout.parentNode.insertBefore(btn,logout);
    else account.appendChild(btn);
  }
}

function openCheckout(){
  ensureOrdersUI();

  if(!state.accessToken){
    openDialog("authModal");
    return;
  }

  const items=state.cart?.items||[];
  if(!items.length){
    toast("Your cart is empty.","error");
    return;
  }

  const selected=getSelectedAddress();
  const {total,count}=cartTotals();

  $("#customerCheckoutBody").innerHTML=`
    <div class="checkout-row">
      <span>${count} item${count===1?"":"s"}</span>
      <strong>${money(total)}</strong>
    </div>

    <div class="checkout-address">
      <small>Deliver to</small>
      ${
        selected
          ? `<div><b>${escapeHTML(selected.label||"Address")}</b><p>${escapeHTML(selected.address_line||"")}${selected.landmark?`, ${escapeHTML(selected.landmark)}`:""}<br>${escapeHTML(selected.city||"")}, ${escapeHTML(selected.state||"")} · ${escapeHTML(selected.pincode||"")}</p></div>`
          : `<div><b>No delivery address selected</b><p>Open Account → Addresses and choose/add an address.</p></div>`
      }
    </div>

    <label style="display:grid;gap:6px;margin:12px 0">
      <span>Payment method</span>
      <select id="checkoutPaymentMethod" class="checkout-payment">
        <option value="cod">Cash on Delivery</option>
      </select>
    </label>

    <label style="display:grid;gap:6px">
      <span>Order note (optional)</span>
      <textarea id="checkoutCustomerNote" class="checkout-note" maxlength="500" placeholder="Any delivery instructions?"></textarea>
    </label>
  `;

  $("#placeOrderBtn").disabled=!selected;
  openDialog("customerCheckoutModal");
}

async function submitOrderFromCheckout(){
  const selected=getSelectedAddress();
  if(!selected?.unique_id){
    toast("Please select a delivery address first.","error");
    return;
  }

  const btn=$("#placeOrderBtn");
  const payment=$("#checkoutPaymentMethod")?.value || "cod";
  const note=$("#checkoutCustomerNote")?.value?.trim() || "";

  btn.disabled=true;
  const oldText=btn.textContent;
  btn.textContent="Placing order…";

  try{
    const order=await api("/orders",{
      method:"POST",
      body:JSON.stringify({
        address_unique_id:selected.unique_id,
        payment_method:payment,
        customer_note:note
      })
    });

    $("#customerCheckoutModal").close();

    // A successful order normally consumes the cart on the backend.
    state.cart=null;
    renderCart();

    try{ await loadCart(); }catch(e){ if(e.status!==404) console.warn("Cart reload after order:",e); }

    toast("Order placed successfully");
    await openOrderDetails(order?.unique_id,order);
  }catch(e){
    toast(readableError(e),"error");
  }finally{
    btn.disabled=false;
    btn.textContent=oldText;
  }
}

async function loadMyOrders(){
  if(!state.accessToken){
    openDialog("authModal");
    return [];
  }

  ensureOrdersUI();
  $("#ordersMeta").textContent="Loading orders…";
  $("#customerOrdersList").innerHTML='<div class="order-empty">Loading…</div>';

  const rows=await api("/orders/my?skip=0&limit=100");
  state.orders=Array.isArray(rows)?rows:[];

  $("#ordersMeta").textContent=`${state.orders.length} order${state.orders.length===1?"":"s"}`;
  renderMyOrders();
  return state.orders;
}

function renderMyOrders(){
  const host=$("#customerOrdersList");
  if(!host)return;

  if(!state.orders.length){
    host.innerHTML='<div class="order-empty"><b>No orders yet</b><br><small>Your placed orders will appear here.</small></div>';
    return;
  }

  host.innerHTML=state.orders.map(order=>{
    const status=String(order.status||"pending").toLowerCase();
    const canCancel=!["cancelled","canceled","delivered","completed"].includes(status);

    return `
      <article class="order-card">
        <div class="order-card-top">
          <div>
            <small>Order ID</small><br>
            <b>${escapeHTML(String(order.unique_id||"").slice(0,8))}</b>
          </div>
          <span class="order-status">${escapeHTML(order.status||"pending")}</span>
        </div>

        <div class="order-row"><span>Total</span><b>${money(order.total_amount)}</b></div>
        <div class="order-row"><span>Payment</span><span>${escapeHTML(order.payment_method||"-")} · ${escapeHTML(order.payment_status||"-")}</span></div>
        <div class="order-row"><span>Placed</span><small>${escapeHTML(formatDateTime(order.created_at))}</small></div>

        <div class="order-card-actions">
          <button type="button" class="secondary-btn" data-view-customer-order="${escapeHTML(order.unique_id||"")}">View details</button>
          ${canCancel?`<button type="button" class="secondary-btn" data-cancel-customer-order="${escapeHTML(order.unique_id||"")}">Cancel order</button>`:""}
        </div>
      </article>
    `;
  }).join("");

  $$("[data-view-customer-order]",host).forEach(btn=>{
    btn.onclick=()=>openOrderDetails(btn.dataset.viewCustomerOrder);
  });

  $$("[data-cancel-customer-order]",host).forEach(btn=>{
    btn.onclick=()=>cancelMyOrder(btn.dataset.cancelCustomerOrder);
  });
}

async function openMyOrders(){
  if(!state.accessToken){
    openDialog("authModal");
    return;
  }

  ensureOrdersUI();
  openDialog("customerOrdersModal");
  try{
    await loadMyOrders();
  }catch(e){
    $("#ordersMeta").textContent="Could not load orders";
    $("#customerOrdersList").innerHTML=`<div class="order-empty">${escapeHTML(readableError(e))}</div>`;
    toast(readableError(e),"error");
  }
}

async function openOrderDetails(orderId,prefetched=null){
  if(!orderId && !prefetched)return;
  ensureOrdersUI();

  let order=prefetched;
  if(!order?.items || !order?.history){
    try{
      order=await api(`/orders/my/${encodeURIComponent(orderId)}`);
    }catch(e){
      toast(readableError(e),"error");
      return;
    }
  }

  $("#orderDetailTitle").textContent=`Order ${String(order.unique_id||"").slice(0,8)}`;
  $("#customerOrderDetailBody").innerHTML=orderDetailsHTML(order);
  openDialog("customerOrderDetailModal");

  const cancelBtn=$("#cancelOrderFromDetailBtn");
  if(cancelBtn){
    cancelBtn.onclick=()=>cancelMyOrder(order.unique_id,true);
  }
}

function orderDetailsHTML(order){
  const items=Array.isArray(order.items)?order.items:[];
  const history=Array.isArray(order.history)?order.history:[];
  const status=String(order.status||"").toLowerCase();
  const canCancel=!["cancelled","canceled","delivered","completed"].includes(status);

  return `
    <div class="order-detail">
      <div class="order-card-top">
        <div>
          <small>Status</small><br>
          <span class="order-status">${escapeHTML(order.status||"-")}</span>
        </div>
        <div style="text-align:right">
          <small>Total</small><br>
          <b>${money(order.total_amount)}</b>
        </div>
      </div>

      <div class="checkout-address">
        <small>Delivery address</small>
        <p>
          <b>${escapeHTML(order.address_label||"Address")}</b><br>
          ${escapeHTML(order.address_line||"")}
          ${order.landmark?`, ${escapeHTML(order.landmark)}`:""}<br>
          ${escapeHTML(order.city||"")}, ${escapeHTML(order.state||"")} · ${escapeHTML(order.pincode||"")}
        </p>
      </div>

      <h3>Items</h3>
      <div class="order-detail-items">
        ${
          items.length
            ? items.map(item=>`
                <div class="order-item order-row">
                  <div>
                    <b>${escapeHTML(item.product_name||"Product")}</b><br>
                    <small>${escapeHTML([item.variant_value,item.variant_unit].filter(Boolean).join(" "))} · Qty ${Number(item.quantity||0)}</small>
                  </div>
                  <b>${money(item.total_price)}</b>
                </div>
              `).join("")
            : '<div class="order-empty">No item details returned.</div>'
        }
      </div>

      <div class="order-summary-box">
        <div class="order-row"><span>Subtotal</span><span>${money(order.subtotal)}</span></div>
        <div class="order-row"><span>Delivery charge</span><span>${money(order.delivery_charge)}</span></div>
        <div class="order-row"><span>Discount</span><span>− ${money(order.discount_amount)}</span></div>
        <div class="order-row order-total-row"><span>Total</span><span>${money(order.total_amount)}</span></div>
        <div class="order-row"><span>Payment</span><span>${escapeHTML(order.payment_method||"-")} · ${escapeHTML(order.payment_status||"-")}</span></div>
      </div>

      ${order.customer_note?`<div class="checkout-address"><small>Customer note</small><p>${escapeHTML(order.customer_note)}</p></div>`:""}

      ${
        history.length
          ? `<h3>Order history</h3>
             <div class="order-detail-items">
               ${history.map(h=>`
                 <div class="order-item">
                   <b>${escapeHTML(h.status||"-")}</b>
                   ${h.note?`<p>${escapeHTML(h.note)}</p>`:""}
                   <small>${escapeHTML(formatDateTime(h.created_at))}</small>
                 </div>
               `).join("")}
             </div>`
          : ""
      }

      ${canCancel?`<button type="button" id="cancelOrderFromDetailBtn" class="secondary-btn full">Cancel order</button>`:""}
    </div>
  `;
}

async function cancelMyOrder(orderId,fromDetail=false){
  if(!orderId)return;
  if(!confirm("Are you sure you want to cancel this order?"))return;

  try{
    await api(`/orders/my/${encodeURIComponent(orderId)}/cancel`,{method:"PATCH"});
    toast("Order cancelled");

    if(fromDetail && $("#customerOrderDetailModal")?.open){
      $("#customerOrderDetailModal").close();
    }

    if($("#customerOrdersModal")?.open){
      await loadMyOrders();
    }else{
      // Keep cached list fresh when possible.
      state.orders=state.orders.map(o=>o.unique_id===orderId?{...o,status:"cancelled"}:o);
    }
  }catch(e){
    toast(readableError(e),"error");
  }
}

function formatDateTime(value){
  if(!value)return "-";
  const d=new Date(value);
  return Number.isNaN(d.getTime())?String(value):d.toLocaleString("en-IN");
}

// Create order UI on initial script load.
ensureOrdersUI();


showLoggedInUI();
if(state.accessToken) bootstrapCustomer();





