const state = {
  drop: {},
  products: [],
  selected: new Set(),
  search: "",
  availableOnly: true,
};

const els = {
  active: document.querySelector("#active"),
  title: document.querySelector("#title"),
  subtitle: document.querySelector("#subtitle"),
  duration: document.querySelector("#duration"),
  expiresAt: document.querySelector("#expires-at"),
  expiredTitle: document.querySelector("#expired-title"),
  expiredMessage: document.querySelector("#expired-message"),
  applyDuration: document.querySelector("#apply-duration"),
  clearSelection: document.querySelector("#clear-selection"),
  search: document.querySelector("#search"),
  availableOnly: document.querySelector("#available-only"),
  productGrid: document.querySelector("#product-grid"),
  selectedCount: document.querySelector("#selected-count"),
  summary: document.querySelector("#drop-summary"),
  save: document.querySelector("#save"),
  publish: document.querySelector("#publish"),
  status: document.querySelector("#status"),
};

const money = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
const normalize = (value) =>
  String(value || "")
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();

const escapeHtml = (value) =>
  String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

function toLocalInputValue(dateLike) {
  const date = new Date(dateLike);
  if (!Number.isFinite(date.getTime())) return "";
  const pad = (value) => String(value).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function parsePrice(value) {
  const numeric = Number(String(value || "").replace("R$", "").replace(/\./g, "").replace(",", "."));
  return Number.isFinite(numeric) ? numeric : 0;
}

function isUnavailable(product) {
  return Boolean(product.sold || product.reserved || product.hidden) || ["vendido", "reservado", "oculto"].includes(normalize(product.status));
}

function visibleProducts() {
  return state.products.filter((product) => {
    const text = normalize(`${product.code} ${product.title} ${product.category}`);
    if (state.search && !text.includes(normalize(state.search))) return false;
    if (state.availableOnly && isUnavailable(product)) return false;
    return true;
  });
}

function productImage(product) {
  if (!product.image) return `<div class="image-fallback">Sem foto</div>`;
  return `<img src="${escapeHtml(product.image)}" alt="${escapeHtml(product.title)}" loading="lazy" />`;
}

function renderProducts() {
  const products = visibleProducts();
  els.productGrid.replaceChildren();

  if (!products.length) {
    els.productGrid.innerHTML = `<p class="empty">Nenhum produto encontrado.</p>`;
    return;
  }

  for (const product of products) {
    const selected = state.selected.has(product.code);
    const unavailable = isUnavailable(product);
    const card = document.createElement("article");
    card.className = `product-card ${selected ? "selected" : ""} ${unavailable ? "unavailable" : ""}`;
    const price = parsePrice(product.price);
    card.innerHTML = `
      ${productImage(product)}
      <div class="product-copy">
        <strong>${escapeHtml(product.code)}</strong>
        <span>${escapeHtml(product.title)}</span>
        <small>${escapeHtml(product.category || "Sem categoria")} · ${price ? money.format(price) : escapeHtml(product.price || "Sem preco")}</small>
        ${unavailable ? `<small>Indisponivel para novo drop</small>` : `<small>${selected ? "Selecionado" : "Toque para selecionar"}</small>`}
      </div>
    `;
    if (!unavailable || selected) {
      card.addEventListener("click", () => {
        if (state.selected.has(product.code)) state.selected.delete(product.code);
        else state.selected.add(product.code);
        renderProducts();
        renderSummary();
      });
    }
    els.productGrid.append(card);
  }
}

function readForm() {
  return {
    active: els.active.checked,
    title: els.title.value.trim(),
    subtitle: els.subtitle.value.trim(),
    expiresAt: els.expiresAt.value ? new Date(els.expiresAt.value).toISOString() : "",
    expiredTitle: els.expiredTitle.value.trim(),
    expiredMessage: els.expiredMessage.value.trim(),
    productCodes: [...state.selected],
  };
}

function renderSummary() {
  const drop = readForm();
  const expiry = drop.expiresAt ? new Date(drop.expiresAt) : null;
  const validExpiry = expiry && Number.isFinite(expiry.getTime());
  const codes = drop.productCodes;
  els.selectedCount.textContent = `${codes.length} selecionado${codes.length === 1 ? "" : "s"}`;
  els.summary.innerHTML = `
    <h3>${escapeHtml(drop.title || "Drop sem titulo")}</h3>
    <p>${escapeHtml(drop.subtitle || "Sem mensagem")}</p>
    <div class="summary-row"><span>Status</span><strong>${drop.active ? "Ativo" : "Inativo"}</strong></div>
    <div class="summary-row"><span>Expiracao</span><strong>${validExpiry ? expiry.toLocaleString("pt-BR") : "Nao definida"}</strong></div>
    <div class="summary-row"><span>Produtos</span><strong>${codes.length}</strong></div>
    <div class="selected-codes">${codes.map((code) => `<span>${escapeHtml(code)}</span>`).join("") || `<small>Nenhum produto selecionado</small>`}</div>
  `;
}

function setForm(drop) {
  els.active.checked = Boolean(drop.active);
  els.title.value = drop.title || "3 Achados do Dia";
  els.subtitle.value = drop.subtitle || "Produtos salvados liberados por tempo limitado. Unidade unica. Quem chamar primeiro tem prioridade.";
  els.expiresAt.value = toLocalInputValue(drop.expiresAt || Date.now() + 60 * 60 * 1000);
  els.expiredTitle.value = drop.expiredTitle || "Link expirado";
  els.expiredMessage.value = drop.expiredMessage || "Esse drop foi encerrado. Aguarde o proximo link no grupo.";
  state.selected = new Set(drop.productCodes || []);
}

function applyDuration() {
  const minutes = Number(els.duration.value || 60);
  els.expiresAt.value = toLocalInputValue(Date.now() + minutes * 60 * 1000);
  renderSummary();
}

async function request(url, options) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.ok === false) throw new Error(data.message || `Falha HTTP ${response.status}`);
  return data;
}

async function save(publish = false) {
  const drop = readForm();
  if (publish && !drop.productCodes.length) throw new Error("Selecione pelo menos um produto para publicar o drop.");
  if (publish && !drop.expiresAt) throw new Error("Defina a expiracao do drop.");

  els.save.disabled = true;
  els.publish.disabled = true;
  els.status.textContent = publish ? "Publicando drop..." : "Salvando...";
  try {
    const result = await request(publish ? "/api/drop/publish" : "/api/drop", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(drop),
    });
    state.drop = result.drop || drop;
    els.status.textContent = result.message || (publish ? "Drop publicado." : "Rascunho salvo.");
  } finally {
    els.save.disabled = false;
    els.publish.disabled = false;
  }
}

function bindForm() {
  for (const element of [els.active, els.title, els.subtitle, els.expiresAt, els.expiredTitle, els.expiredMessage]) {
    element.addEventListener(element.type === "checkbox" ? "change" : "input", renderSummary);
  }
  els.applyDuration.addEventListener("click", applyDuration);
  els.clearSelection.addEventListener("click", () => {
    state.selected.clear();
    renderProducts();
    renderSummary();
  });
  els.search.addEventListener("input", (event) => {
    state.search = event.target.value;
    renderProducts();
  });
  els.availableOnly.addEventListener("change", (event) => {
    state.availableOnly = event.target.checked;
    renderProducts();
  });
  els.save.addEventListener("click", () => save(false).catch((error) => (els.status.textContent = error.message)));
  els.publish.addEventListener("click", () => save(true).catch((error) => (els.status.textContent = error.message)));
}

async function boot() {
  const [drop, productData] = await Promise.all([request("/api/drop"), request("/api/drop-products")]);
  state.drop = drop;
  state.products = productData.products || [];
  setForm(drop);
  bindForm();
  renderProducts();
  renderSummary();
}

boot().catch((error) => {
  els.status.textContent = error.message;
  els.productGrid.innerHTML = `<p class="empty">${escapeHtml(error.message)}</p>`;
});
