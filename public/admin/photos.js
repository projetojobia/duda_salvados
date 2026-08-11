const state = {
  products: [],
  overrides: {},
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
};

const normalize = (value) =>
  String(value || "")
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();

function ensureOverride(code) {
  if (!state.overrides[code]) state.overrides[code] = { primary: "", order: [], hidden: [] };
  const override = state.overrides[code];
  override.primary ||= "";
  override.order ||= [];
  override.hidden ||= [];
  return override;
}

function visibleProducts() {
  return state.products.filter((product) => {
    const text = normalize(`${product.code} ${product.title} ${product.category}`);
    const noPhotos = product.sourcePhotos.length === 0;
    return (!state.search || text.includes(normalize(state.search))) && (!state.missingOnly || noPhotos);
  });
}

function renderList() {
  els.list.replaceChildren();
  for (const product of visibleProducts()) {
    const button = document.createElement("button");
    button.className = `item ${state.selected === product.code ? "active" : ""}`;
    button.innerHTML = `<strong>${product.code}</strong><span>${product.title}</span><small>${product.sourcePhotos.length} foto(s)</small>`;
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

function renderEditor() {
  const product = state.products.find((item) => item.code === state.selected);
  if (!product) {
    els.editor.innerHTML = `<p class="empty">Selecione um produto.</p>`;
    return;
  }
  const override = ensureOverride(product.code);
  const photos = orderedPhotos(product);
  const primary = override.primary || photos.find((photo) => !override.hidden.includes(photo.fileName))?.fileName || "";

  els.editor.replaceChildren();
  const head = document.createElement("div");
  head.className = "editor-head";
  head.innerHTML = `
    <div>
      <h2>${product.code} - ${product.title}</h2>
      <p class="meta">${product.category} | ${product.status} | R$ ${product.price}</p>
    </div>
    <button id="clear-product">Limpar escolhas deste produto</button>
  `;
  els.editor.append(head);
  head.querySelector("#clear-product").addEventListener("click", () => {
    delete state.overrides[product.code];
    renderEditor();
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
      <img src="${photo.url}" alt="${photo.fileName}" />
      <div class="photo-actions">
        <strong>${primary === photo.fileName && !hidden ? "Principal" : hidden ? "Oculta" : "Disponivel"}</strong>
        <span class="filename">${photo.fileName}</span>
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
  const response = await fetch("/api/overrides", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(cleaned),
  });
  if (!response.ok) throw new Error("Falha ao salvar");
  state.overrides = cleaned;
  els.save.textContent = "Salvo";
  setTimeout(() => {
    els.save.textContent = "Salvar escolhas";
  }, 1200);
}

async function boot() {
  const response = await fetch("/api/photos");
  const data = await response.json();
  state.products = data.products;
  state.overrides = data.overrides || {};
  state.selected = state.products[0]?.code || "";
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

boot();
