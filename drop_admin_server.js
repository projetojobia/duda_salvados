import { existsSync } from "node:fs";
import { readFile, writeFile } from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(root, "public");
const catalogPath = path.join(publicDir, "catalog.json");
const dropPath = path.join(publicDir, "drop.json");
const port = Number(process.env.DROP_ADMIN_PORT || 8791);
const execFileAsync = promisify(execFile);

const mime = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".webp": "image/webp",
  ".mp4": "video/mp4",
  ".mov": "video/quicktime",
  ".webm": "video/webm",
  ".svg": "image/svg+xml",
};

async function readJson(file, fallback) {
  if (!existsSync(file)) return fallback;
  return JSON.parse((await readFile(file, "utf8")).replace(/^\uFEFF/, ""));
}

function sendJson(res, status, value) {
  res.writeHead(status, {
    "content-type": mime[".json"],
    "cache-control": "no-store",
  });
  res.end(JSON.stringify(value, null, 2));
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

function sanitizeCode(value) {
  return String(value || "").trim().toUpperCase().replace(/[^A-Z0-9_-]/g, "");
}

function normalizeDrop(input, current = {}) {
  const productCodes = Array.from(
    new Set((Array.isArray(input.productCodes) ? input.productCodes : []).map(sanitizeCode).filter(Boolean)),
  );

  let expiresAt = String(input.expiresAt || "").trim();
  if (!expiresAt) expiresAt = current.expiresAt || new Date(Date.now() + 60 * 60 * 1000).toISOString();
  const parsedExpiry = new Date(expiresAt);
  if (!Number.isFinite(parsedExpiry.getTime())) throw new Error("Data de expiracao invalida.");

  return {
    active: Boolean(input.active),
    title: String(input.title || "Drop relampago").trim().slice(0, 120),
    subtitle: String(input.subtitle || "Produtos liberados por tempo limitado.").trim().slice(0, 400),
    expiresAt: parsedExpiry.toISOString(),
    expiredTitle: String(input.expiredTitle || "Link expirado").trim().slice(0, 120),
    expiredMessage: String(input.expiredMessage || "Esse drop foi encerrado. Aguarde o proximo link no grupo.")
      .trim()
      .slice(0, 400),
    productCodes,
  };
}

async function run(command, args) {
  try {
    const { stdout, stderr } = await execFileAsync(command, args, {
      cwd: root,
      windowsHide: true,
      maxBuffer: 1024 * 1024 * 8,
    });
    return { ok: true, stdout, stderr };
  } catch (error) {
    return {
      ok: false,
      stdout: error.stdout || "",
      stderr: error.stderr || "",
      message: error.message || String(error),
    };
  }
}

async function saveDrop(body) {
  const current = await readJson(dropPath, {});
  const drop = normalizeDrop(body, current);
  await writeFile(dropPath, `${JSON.stringify(drop, null, 2)}\n`, "utf8");
  return drop;
}

async function publishDrop(drop) {
  const steps = [];
  const add = await run("git", ["add", "public/drop.json"]);
  steps.push({ name: "git add", ...add });
  if (!add.ok) return { ok: false, step: "git add", steps };

  const diff = await run("git", ["diff", "--cached", "--quiet"]);
  if (diff.ok) {
    return { ok: true, published: false, message: "Drop salvo. Nenhuma alteracao nova para publicar.", drop, steps };
  }

  const commit = await run("git", ["commit", "-m", `Publish drop: ${drop.title}`]);
  steps.push({ name: "git commit", ...commit });
  if (!commit.ok) return { ok: false, step: "git commit", steps };

  const push = await run("git", ["push", "origin", "HEAD:main"]);
  steps.push({ name: "git push", ...push });
  if (!push.ok) return { ok: false, step: "git push", steps };

  return { ok: true, published: true, message: "Drop publicado no GitHub. O site sera atualizado pelo fluxo de deploy configurado.", drop, steps };
}

async function handleApi(req, res, url) {
  if (url.pathname === "/api/drop" && req.method === "GET") {
    sendJson(res, 200, await readJson(dropPath, {}));
    return true;
  }

  if (url.pathname === "/api/drop-products" && req.method === "GET") {
    const catalog = await readJson(catalogPath, { products: [] });
    const products = (catalog.products || []).map((product) => ({
      code: product.code,
      title: product.title,
      category: product.category,
      price: product.price,
      referencePrice: product.referencePrice,
      sold: Boolean(product.sold),
      reserved: Boolean(product.reserved),
      hidden: Boolean(product.hidden),
      status: product.status,
      image: product.media?.[0]?.url || product.images?.[0] || "",
    }));
    sendJson(res, 200, { products });
    return true;
  }

  if (url.pathname === "/api/drop" && req.method === "POST") {
    try {
      const drop = await saveDrop(JSON.parse(await readBody(req) || "{}"));
      sendJson(res, 200, { ok: true, drop });
    } catch (error) {
      sendJson(res, 400, { ok: false, message: error.message || String(error) });
    }
    return true;
  }

  if (url.pathname === "/api/drop/publish" && req.method === "POST") {
    try {
      const drop = await saveDrop(JSON.parse(await readBody(req) || "{}"));
      const result = await publishDrop(drop);
      sendJson(res, result.ok ? 200 : 500, result);
    } catch (error) {
      sendJson(res, 500, { ok: false, message: error.message || String(error) });
    }
    return true;
  }

  return false;
}

function safePublicPath(pathname) {
  const requested = pathname === "/" ? "/admin/drop.html" : pathname;
  const resolved = path.resolve(publicDir, `.${decodeURIComponent(requested)}`);
  const publicRoot = path.resolve(publicDir);
  return resolved.startsWith(publicRoot) ? resolved : null;
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url || "/", `http://${req.headers.host || `127.0.0.1:${port}`}`);
    if (await handleApi(req, res, url)) return;

    const file = safePublicPath(url.pathname);
    if (!file || !existsSync(file)) {
      res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
      res.end("Nao encontrado");
      return;
    }

    const ext = path.extname(file).toLowerCase();
    res.writeHead(200, {
      "content-type": mime[ext] || "application/octet-stream",
      "cache-control": "no-store",
    });
    res.end(await readFile(file));
  } catch (error) {
    sendJson(res, 500, { ok: false, message: error.message || String(error) });
  }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`Duda Salvados - admin de drops: http://127.0.0.1:${port}/admin/drop.html`);
});
