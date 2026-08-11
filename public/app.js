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

function discountLabel(product) {
  const discount = Number(product.discountPercent || 0);
  if (!Number.isFinite(discount) || discount < 5) return "";
  return `${Math.round(discount)}% OFF`;
}

function renderPrice(product, priceEl) {
  const priceValue = parsePrice(product.price);
  const referenceValue = parsePrice(product.referencePrice);
  priceEl.replaceChildren();

  if (referenceValue > priceValue && priceValue > 0) {
    const oldPrice = document.createElement("span");
    oldPrice.className = "old-price";
    oldPrice.textContent = `De ${money.format(referenceValue)}`;

    const currentPrice = document.createElement("span");
    currentPrice.className = "current-price";
    currentPrice.textContent = `Por ${money.format(priceValue)}`;

    priceEl.append(oldPrice, currentPrice);
    return;
  }

  priceEl.textContent = priceValue ? money.format(priceValue) : product.price;
}

function stockLabel(value) {
  const quantity = Number(String(value || "1").replace(",", "."));
  if (!Number.isFinite(quantity) || quantity <= 1) return "Última unidade";
  return `${Math.trunc(quantity)} em estoque`;
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
  const displayStatus = product.sold ? "Vendido" : "Disponivel";
  return (
    (!state.search || haystack.includes(normalize(state.search))) &&
    (!state.category || product.category === state.category) &&
    (!state.status || displayStatus === state.status)
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
    const photoWrap = node.querySelector(".photo-wrap");
    const fallback = node.querySelector(".photo-fallback");
    const title = node.querySelector("h2");
    const media = product.media?.[0] || (product.images?.[0] ? { type: "image", url: product.images[0] } : null);
    const isSold = Boolean(product.sold);
    const badge = discountLabel(product);

    if (isSold) {
      node.classList.add("sold");
      const soldStamp = document.createElement("div");
      soldStamp.className = "sold-stamp";
      soldStamp.textContent = "Vendido";
      photoWrap.append(soldStamp);
    }

    if (media?.type === "video") {
      const video = document.createElement("video");
      video.className = "photo";
      video.src = media.url;
      video.controls = true;
      video.muted = true;
      video.preload = "metadata";
      photoWrap.prepend(video);
      fallback.hidden = true;
    } else if (media?.url) {
      const img = document.createElement("img");
      img.className = "photo";
      img.alt = product.title;
      img.loading = "lazy";
      img.src = media.url;
      photoWrap.prepend(img);
      fallback.hidden = true;
    }

    node.querySelector(".code").textContent = product.code;
    node.querySelector(".status").textContent = isSold ? "Vendido" : badge;
    node.querySelector(".status").hidden = !isSold && !badge;
    title.textContent = product.title;
    node.querySelector(".desc").textContent = product.description;
    renderPrice(product, node.querySelector(".price"));
    node.querySelector(".condition").textContent = product.condition || "A conferir";
    node.querySelector(".quantity").textContent = stockLabel(product.quantity);
    const whatsapp = node.querySelector(".whatsapp");
    if (isSold) {
      whatsapp.textContent = "Produto vendido";
      whatsapp.removeAttribute("href");
      whatsapp.setAttribute("aria-disabled", "true");
    } else {
      whatsapp.href = `https://wa.me/?text=${encodeURIComponent(product.whatsAppText)}`;
    }
    els.products.append(node);
  }
}

function renderSummary() {
  const { products, categories, missingPhotos } = state.catalog.summary;
  els.summary.textContent = `${products} produtos • ${categories} categorias • ${missingPhotos.length} sem foto`;
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
