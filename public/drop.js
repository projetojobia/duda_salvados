const state = {
  drop: null,
  catalog: null,
  timer: null,
};

const money = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
const whatsappNumber = "5541984860237";

const els = {
  hero: document.querySelector("#drop-hero"),
  title: document.querySelector("#drop-title"),
  subtitle: document.querySelector("#drop-subtitle"),
  countdown: document.querySelector("#countdown"),
  countdownValue: document.querySelector("#countdown-value"),
  products: document.querySelector("#drop-products"),
  template: document.querySelector("#drop-product-template"),
};

function parsePrice(value) {
  const number = Number(String(value || "").replace("R$", "").replace(/\./g, "").replace(",", "."));
  return Number.isFinite(number) ? number : 0;
}

function isExpired() {
  if (!state.drop?.active) return true;
  const expiresAt = new Date(state.drop.expiresAt).getTime();
  return !Number.isFinite(expiresAt) || Date.now() >= expiresAt;
}

function formatRemaining(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function renderPrice(product, target) {
  const price = parsePrice(product.price);
  const reference = parsePrice(product.referencePrice);
  target.replaceChildren();
  if (reference > price && price > 0) {
    target.innerHTML = `<span>De ${money.format(reference)}</span><strong>Por ${money.format(price)}</strong>`;
    return;
  }
  target.innerHTML = `<strong>${price ? money.format(price) : product.price}</strong>`;
}

function renderMedia(product, photoWrap, fallback) {
  const media = product.media?.[0] || (product.images?.[0] ? { type: "image", url: product.images[0] } : null);
  fallback.hidden = Boolean(media?.url);
  if (!media?.url) return;
  if (media.type === "video") {
    const video = document.createElement("video");
    video.className = "photo";
    video.src = media.url;
    video.muted = true;
    video.controls = true;
    video.preload = "metadata";
    photoWrap.prepend(video);
    return;
  }
  const img = document.createElement("img");
  img.className = "photo";
  img.alt = product.title;
  img.src = media.url;
  photoWrap.prepend(img);
}

function renderExpired() {
  clearInterval(state.timer);
  els.hero.classList.add("expired");
  els.title.textContent = state.drop?.expiredTitle || "Link expirado";
  els.subtitle.textContent = state.drop?.expiredMessage || "Aguarde o proximo link no grupo.";
  els.countdown.hidden = true;
  els.products.innerHTML = `<p class="expired-box">Esse drop foi encerrado. Quem viu, viu. O proximo link sera avisado no grupo.</p>`;
}

function renderProducts() {
  const codes = new Set(state.drop.productCodes || []);
  const products = (state.catalog.products || []).filter((product) => codes.has(product.code));
  els.products.replaceChildren();

  if (!products.length) {
    els.products.innerHTML = `<p class="expired-box">Nenhum produto selecionado para este drop.</p>`;
    return;
  }

  for (const product of products) {
    const node = els.template.content.firstElementChild.cloneNode(true);
    const isSold = Boolean(product.sold);
    const isReserved = Boolean(product.reserved);
    const badge = isSold ? "Vendido" : isReserved ? "Reservado" : `${Math.round(product.discountPercent || 0)}% OFF`;
    node.classList.toggle("blocked", isSold || isReserved);
    node.querySelector(".code").textContent = product.code;
    node.querySelector(".badge").textContent = badge;
    node.querySelector("h2").textContent = product.title;
    node.querySelector(".desc").textContent = product.description;
    renderPrice(product, node.querySelector(".price"));
    renderMedia(product, node.querySelector(".photo-wrap"), node.querySelector(".photo-fallback"));
    const whatsapp = node.querySelector(".whatsapp");
    if (isSold || isReserved) {
      whatsapp.textContent = isSold ? "Produto vendido" : "Produto reservado";
      whatsapp.removeAttribute("href");
      whatsapp.setAttribute("aria-disabled", "true");
    } else {
      whatsapp.href = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(product.whatsAppText)}`;
    }
    els.products.append(node);
  }
}

function tick() {
  const remaining = new Date(state.drop.expiresAt).getTime() - Date.now();
  if (remaining <= 0) {
    renderExpired();
    return;
  }
  els.countdownValue.textContent = formatRemaining(remaining);
}

function renderActive() {
  els.hero.classList.remove("expired");
  els.title.textContent = state.drop.title || "Drop liberado";
  els.subtitle.textContent = state.drop.subtitle || "Produtos por tempo limitado.";
  els.countdown.hidden = false;
  renderProducts();
  tick();
  state.timer = setInterval(tick, 1000);
}

async function boot() {
  const [dropResponse, catalogResponse] = await Promise.all([
    fetch(`/drop.json?ts=${Date.now()}`),
    fetch(`/catalog.json?ts=${Date.now()}`),
  ]);
  state.drop = await dropResponse.json();
  state.catalog = await catalogResponse.json();
  if (isExpired()) renderExpired();
  else renderActive();
}

boot().catch((error) => {
  els.title.textContent = "Nao foi possivel abrir o drop";
  els.subtitle.textContent = error.message;
});
