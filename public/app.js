const state = {
  catalog: null,
  search: "",
  category: "",
  status: "",
};

const money = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

const els = {
  summary: document.querySelector("#summary"),
  products: document.querySelector("#products"),
  template: document.querySelector("#product-template"),
  search: document.querySelector("#search"),
  category: document.querySelector("#category"),
  status: document.querySelector("#status"),
};

const normalize = (value) =>
  String(value || "")
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();

function parsePrice(value) {
  const number = Number(String(value).replace("R$", "").replace(/\./g, "").replace(",", "."));
  return Number.isFinite(number) ? number : 0;
}

function renderFilters() {
  els.category.replaceChildren(new Option("Todas", ""));
  for (const category of state.catalog.categories) {
    els.category.append(new Option(category, category));
  }
}

function productMatches(product) {
  const haystack = normalize(
    `${product.code} ${product.title} ${product.description} ${product.category} ${product.brand} ${product.model}`,
  );
  return (
    (!state.search || haystack.includes(normalize(state.search))) &&
    (!state.category || product.category === state.category) &&
    (!state.status || product.status === state.status)
  );
}

function renderProducts() {
  const products = state.catalog.products.filter(productMatches);
  els.products.replaceChildren();

  if (!products.length) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "Nenhum produto encontrado com estes filtros.";
    els.products.append(empty);
    return;
  }

  for (const product of products) {
    const node = els.template.content.firstElementChild.cloneNode(true);
    const img = node.querySelector(".photo");
    const title = node.querySelector("h2");
    const priceValue = parsePrice(product.price);

    img.alt = product.title;
    if (product.images.length) {
      img.src = product.images[0];
    } else {
      img.hidden = true;
    }

    node.querySelector(".code").textContent = product.code;
    node.querySelector(".status").textContent = product.status;
    title.textContent = product.title;
    node.querySelector(".desc").textContent = product.description;
    node.querySelector(".price").textContent = priceValue ? money.format(priceValue) : product.price;
    node.querySelector(".condition").textContent = product.condition || "A conferir";
    node.querySelector(".quantity").textContent = product.quantity;
    node.querySelector(".whatsapp").href = `https://wa.me/?text=${encodeURIComponent(product.whatsAppText)}`;
    els.products.append(node);
  }
}

function renderSummary() {
  const { products, categories, totalPotential, missingPhotos } = state.catalog.summary;
  els.summary.textContent = `${products} produtos • ${categories} categorias • ${money.format(totalPotential)} em potencial • ${missingPhotos.length} sem foto`;
}

async function boot() {
  const response = await fetch("/catalog.json");
  state.catalog = await response.json();
  renderSummary();
  renderFilters();
  renderProducts();
}

els.search.addEventListener("input", (event) => {
  state.search = event.target.value;
  renderProducts();
});

els.category.addEventListener("change", (event) => {
  state.category = event.target.value;
  renderProducts();
});

els.status.addEventListener("change", (event) => {
  state.status = event.target.value;
  renderProducts();
});

boot();
