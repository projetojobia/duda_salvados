const state = {
  products: [],
  overrides: {},
  productOverrides: {},
  selected: "",
  search: "",
  missingOnly: false,
};

const els = {
  list: document.querySelector("#list"),
  editor: document.querySelector("#editor"),
  search: document.querySelector("#search"),
  missing: document.querySelector("#missing"),
  save: document.querySelector("#save"),
  publish: document.querySelector("#publish"),
  publishStatus: document.querySelector("#publish-status"),
};

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

function ensureOverride(code) {
  if (!state.overrides[code]) state.overrides[code] = { primary: "", order: [], hidden: [] };
  const override = state.overrides[code];
  override.primary ||= "";
  override.order ||= [];
  override.hidden ||= [];
  return override;
}

function ensureProductOverride(code) {
  if (!state.productOverrides[code]) state.productOverrides[code] = { title: "", sold: false, hidden: false };
  state.productOverrides[code].title ||= "";
  state.productOverrides[code].sold = Boolean(state.productOverrides[code].sold);
  state.productOverrides[code].hidden = Boolean(state.productOverrides[code].hidden);
  return state.productOverrides[code];
}

function visibleProducts() {
  return state.products.filter((product) => {
    const text = normalize(`${product.code} ${product.customTitle || product.title} ${product.category}`);
    const noPhotos = product.sourcePhotos.length === 0;
    return (!state.search || text.includes(normalize(state.search))) && (!state.missingOnly || noPhotos);
  });
}

function renderList() {
  els.list.replaceChildren();
  for (const product of visibleProducts()) {
    const button = document.createElement("button");
    button.className = `item ${state.selected === product.code ? "active" : ""}`;
    const sold = ensureProductOverride(product.code).sold;
    const hidden = ensureProductOverride(product.code).hidden;
    const flags = [hidden ? "Oculto" : "", sold ? "Vendido" : ""].filter(Boolean).join(" | ");
    button.innerHTML = `<strong>${escapeHtml(product.code)}</strong><span>${escapeHtml(product.customTitle || product.title)}</span><small>${flags ? `${flags} | ` : ""}${product.sourcePhotos.length} arquivo(s)</small>`;
    button.addEventListener("click", () => {
      state.selected = product.code;
      render();
    });
    els.list.append(button);
  }
}

function orderedPhotos(product) {
  const override = ensureOverride(product.code);
  const byName = new Map(product.sourcePhotos.map((photo) => [photo.fileName, photo]));
  const ordered = [];
  for (const name of override.order) {
    if (byName.has(name)) {
      ordered.push(byName.get(name));
      byName.delete(name);
    }
  }
  ordered.push(...byName.values());
  return ordered;
}

function movePhoto(code, fileName, direction) {
  const product = state.products.find((item) => item.code === code);
  const override = ensureOverride(code);
  const names = orderedPhotos(product).map((photo) => photo.fileName);
  const index = names.indexOf(fileName);
  const next = index + direction;
  if (index < 0 || next < 0 || next >= names.length) return;
  [names[index], names[next]] = [names[next], names[index]];
  override.order = names;
  renderEditor();
}

function toggleHidden(code, fileName) {
  const override = ensureOverride(code);
  if (override.hidden.includes(fileName)) {
    override.hidden = override.hidden.filter((name) => name !== fileName);
  } else {
    override.hidden.push(fileName);
    if (override.primary === fileName) override.primary = "";
  }
  renderEditor();
}

function setPrimary(code, fileName) {
  const override = ensureOverride(code);
  override.primary = fileName;
  override.hidden = override.hidden.filter((name) => name !== fileName);
  const names = orderedPhotos(state.products.find((item) => item.code === code)).map((photo) => photo.fileName);
  override.order = [fileName, ...names.filter((name) => name !== fileName)];
  renderEditor();
}

function updateTitle(code, title) {
  const override = ensureProductOverride(code);
  override.title = title.trim();
  const product = state.products.find((item) => item.code === code);
  if (product) product.customTitle = override.title;
  renderList();
}

function updateSold(code, sold) {
  const override = ensureProductOverride(code);
  override.sold = sold;
  renderList();
}

function updateHidden(code, hidden) {
  const override = ensureProductOverride(code);
  override.hidden = hidden;
  renderList();
}

async function uploadMedia(code, input) {
  const file = input.files?.[0];
  if (!file) return;
  const form = new FormData();
  form.append("code", code);
  form.append("media", file);
  const response = await fetch("/api/upload", { method: "POST", body: form });
  if (!response.ok) throw new Error(await response.text());
  await loadData(code);
}

function renderEditor() {
  const product = state.products.find((item) => item.code === state.selected);
  if (!product) {
    els.editor.innerHTML = `<p class="empty">Selecione um produto.</p>`;
    return;
  }
  const override = ensureOverride(product.code);
  const productOverride = ensureProductOverride(product.code);
  const photos = orderedPhotos(product);
  const primary = override.primary || photos.find((photo) => !override.hidden.includes(photo.fileName))?.fileName || "";

  els.editor.replaceChildren();
  const head = document.createElement("div");
  head.className = "editor-head";
  head.innerHTML = `
    <div>
      <h2>${escapeHtml(product.code)} - ${escapeHtml(product.customTitle || product.title)}</h2>
      <p class="meta">${escapeHtml(product.category)} | ${escapeHtml(product.status)} | R$ ${escapeHtml(product.price)}</p>
    </div>
    <button id="clear-product">Limpar escolhas deste produto</button>
  `;
  els.editor.append(head);
  head.querySelector("#clear-product").addEventListener("click", () => {
    delete state.overrides[product.code];
    renderEditor();
  });

  const tools = document.createElement("div");
  tools.className = "product-tools";
  tools.innerHTML = `
    <label class="field">
      <span>Titulo do produto</span>
      <input id="title-edit" type="text" value="${escapeHtml(productOverride.title || "")}" placeholder="${escapeHtml(product.title)}" />
    </label>
    <label class="sold-toggle">
      <input id="sold-edit" type="checkbox" ${productOverride.sold ? "checked" : ""} />
      <span>Produto vendido</span>
    </label>
    <label class="sold-toggle">
      <input id="hidden-edit" type="checkbox" ${productOverride.hidden ? "checked" : ""} />
      <span>Ocultar do catálogo</span>
    </label>
    <label class="upload">
      <span>Carregar foto ou video</span>
      <input id="media-upload" type="file" accept="image/jpeg,image/png,image/webp,video/mp4,video/quicktime,video/webm" />
    </label>
  `;
  els.editor.append(tools);
  tools.querySelector("#title-edit").addEventListener("input", (event) => {
    updateTitle(product.code, event.target.value);
  });
  tools.querySelector("#sold-edit").addEventListener("change", (event) => {
    updateSold(product.code, event.target.checked);
  });
  tools.querySelector("#hidden-edit").addEventListener("change", (event) => {
    updateHidden(product.code, event.target.checked);
  });
  tools.querySelector("#media-upload").addEventListener("change", (event) => {
    uploadMedia(product.code, event.target).catch((error) => alert(error.message));
  });

  if (!photos.length) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "Este produto ainda nao tem fotos associadas no relatorio local.";
    els.editor.append(empty);
    return;
  }

  const grid = document.createElement("div");
  grid.className = "photos";
  for (const photo of photos) {
    const hidden = override.hidden.includes(photo.fileName);
    const card = document.createElement("article");
    card.className = `photo-card ${primary === photo.fileName && !hidden ? "primary" : ""} ${hidden ? "hidden-photo" : ""}`;
    card.innerHTML = `
      ${
        photo.mediaType === "video"
          ? `<video src="${photo.url}" controls muted preload="metadata"></video>`
          : `<img src="${photo.url}" alt="${escapeHtml(photo.fileName)}" />`
      }
      <div class="photo-actions">
        <strong>${photo.manual ? "Manual | " : ""}${primary === photo.fileName && !hidden ? "Principal" : hidden ? "Oculta" : "Disponivel"}</strong>
        <span class="filename">${escapeHtml(photo.fileName)}</span>
        <div class="row">
          <button data-action="primary">Principal</button>
          <button data-action="up">Subir</button>
          <button data-action="down">Descer</button>
        </div>
        <button class="danger" data-action="hidden">${hidden ? "Mostrar" : "Ocultar"}</button>
      </div>
    `;
    card.querySelector('[data-action="primary"]').addEventListener("click", () => setPrimary(product.code, photo.fileName));
    card.querySelector('[data-action="up"]').addEventListener("click", () => movePhoto(product.code, photo.fileName, -1));
    card.querySelector('[data-action="down"]').addEventListener("click", () => movePhoto(product.code, photo.fileName, 1));
    card.querySelector('[data-action="hidden"]').addEventListener("click", () => toggleHidden(product.code, photo.fileName));
    grid.append(card);
  }
  els.editor.append(grid);
}

function render() {
  renderList();
  renderEditor();
}

async function save() {
  const cleaned = {};
  for (const [code, override] of Object.entries(state.overrides)) {
    if (override.primary || override.order.length || override.hidden.length) cleaned[code] = override;
  }
  const productCleaned = {};
  for (const [code, override] of Object.entries(state.productOverrides)) {
    const cleanedOverride = {};
    if (override.title) cleanedOverride.title = override.title;
    if (override.sold) cleanedOverride.sold = true;
    if (override.hidden) cleanedOverride.hidden = true;
    if (Object.keys(cleanedOverride).length) productCleaned[code] = cleanedOverride;
  }
  const [response, productResponse] = await Promise.all([
    fetch("/api/overrides", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(cleaned),
    }),
    fetch("/api/product-overrides", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(productCleaned),
    }),
  ]);
  if (!response.ok || !productResponse.ok) {
    const failed = !response.ok ? response : productResponse;
    const details = await failed.text().catch(() => "");
    throw new Error(`Falha ao salvar (${failed.status}). ${details}`.trim());
  }
  state.overrides = cleaned;
  state.productOverrides = productCleaned;
  els.save.textContent = "Salvo";
  setTimeout(() => {
    els.save.textContent = "Salvar escolhas";
  }, 1200);
}

async function publishCatalog() {
  els.publish.disabled = true;
  els.save.disabled = true;
  els.publishStatus.textContent = "Salvando...";
  await save();
  els.publishStatus.textContent = "Sincronizando planilha e publicando...";
  const response = await fetch("/api/publish", { method: "POST" });
  const result = await response.json().catch(() => ({}));
  if (!response.ok || !result.ok) {
    const detail = result.step ? ` Etapa: ${result.step}.` : "";
    throw new Error(`${result.message || "Falha ao publicar."}${detail}`);
  }
  els.publishStatus.textContent = result.message || "Publicado.";
  setTimeout(() => {
    els.publishStatus.textContent = "";
  }, 6000);
}

async function loadData(selected = state.selected) {
  const response = await fetch("/api/photos");
  const data = await response.json();
  state.products = data.products;
  state.overrides = data.overrides || {};
  state.productOverrides = data.productOverrides || {};
  state.selected = selected || state.products[0]?.code || "";
  render();
}

els.search.addEventListener("input", (event) => {
  state.search = event.target.value;
  renderList();
});
els.missing.addEventListener("change", (event) => {
  state.missingOnly = event.target.checked;
  renderList();
});
els.save.addEventListener("click", () => save().catch((error) => alert(error.message)));
els.publish.addEventListener("click", () => {
  publishCatalog()
    .catch((error) => alert(error.message))
    .finally(() => {
      els.publish.disabled = false;
      els.save.disabled = false;
    });
});

loadData();
