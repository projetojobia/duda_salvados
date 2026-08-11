import { createReadStream, existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(root, "public");
const reportPath = path.join(root, "photo_rename_report.csv");
const overridesPath = path.join(root, "catalog_photo_overrides.json");
const productOverridesPath = path.join(root, "catalog_product_overrides.json");
const manualMediaDir = path.join(root, "catalog_manual_media");
const port = Number(process.env.PORT || 8790);

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
};

const allowedMediaExtensions = new Set([".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm"]);

function parseCsvLine(line) {
  const values = [];
  let current = "";
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"' && line[i + 1] === '"') {
      current += '"';
      i += 1;
    } else if (ch === '"') {
      quoted = !quoted;
    } else if (ch === "," && !quoted) {
      values.push(current);
      current = "";
    } else {
      current += ch;
    }
  }
  values.push(current);
  return values;
}

async function readPhotoReport() {
  const text = await readFile(reportPath, "utf8");
  const lines = text.replace(/^\uFEFF/, "").trim().split(/\r?\n/);
  const headers = parseCsvLine(lines.shift() || "");
  const rows = [];
  for (const line of lines) {
    if (!line.trim()) continue;
    const values = parseCsvLine(line);
    const row = Object.fromEntries(headers.map((header, index) => [header, values[index] || ""]));
    if (row.Tipo === "PRODUTO" && row.Codigo && row.DestinoArquivo) rows.push(row);
  }
  return rows;
}

async function readManualMedia() {
  const rows = [];
  if (!existsSync(manualMediaDir)) return rows;
  const { readdir } = await import("node:fs/promises");
  for (const codeDir of await readdir(manualMediaDir, { withFileTypes: true })) {
    if (!codeDir.isDirectory()) continue;
    const code = codeDir.name;
    const folder = path.join(manualMediaDir, code);
    for (const file of await readdir(folder, { withFileTypes: true })) {
      if (!file.isFile()) continue;
      const filePath = path.join(folder, file.name);
      const ext = path.extname(file.name).toLowerCase();
      if (!allowedMediaExtensions.has(ext)) continue;
      rows.push({
        Codigo: code,
        DestinoArquivo: filePath,
        Manual: "1",
      });
    }
  }
  return rows;
}

async function readJson(file, fallback) {
  if (!existsSync(file)) return fallback;
  return JSON.parse(await readFile(file, "utf8"));
}

function sendJson(res, value) {
  res.writeHead(200, { "content-type": mime[".json"], "cache-control": "no-store" });
  res.end(JSON.stringify(value, null, 2));
}

function safeLocalPhotoPath(raw) {
  const resolved = path.resolve(raw);
  const allowedRoots = [path.resolve(root, "Fotos_Organizadas"), path.resolve(manualMediaDir)];
  if (!allowedRoots.some((allowedRoot) => resolved.startsWith(allowedRoot))) return null;
  return resolved;
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

function sanitizeCode(code) {
  return String(code || "").trim().toUpperCase().replace(/[^A-Z0-9_-]/g, "");
}

function sanitizeBaseName(name) {
  return String(name || "midia")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9._-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 80) || "midia";
}

function parseMultipart(buffer, contentType) {
  const boundaryMatch = contentType.match(/boundary=(?:"([^"]+)"|([^;]+))/);
  const boundary = boundaryMatch?.[1] || boundaryMatch?.[2];
  if (!boundary) throw new Error("Upload sem boundary");
  const marker = Buffer.from(`--${boundary}`);
  const parts = [];
  let start = buffer.indexOf(marker);
  while (start >= 0) {
    start += marker.length;
    if (buffer[start] === 45 && buffer[start + 1] === 45) break;
    if (buffer[start] === 13 && buffer[start + 1] === 10) start += 2;
    const headerEnd = buffer.indexOf(Buffer.from("\r\n\r\n"), start);
    if (headerEnd < 0) break;
    const headers = buffer.slice(start, headerEnd).toString("utf8");
    const next = buffer.indexOf(marker, headerEnd + 4);
    if (next < 0) break;
    let body = buffer.slice(headerEnd + 4, next);
    if (body.at(-2) === 13 && body.at(-1) === 10) body = body.slice(0, -2);
    const disposition = headers.match(/content-disposition:\s*form-data;([^\r\n]+)/i)?.[1] || "";
    const name = disposition.match(/name="([^"]+)"/)?.[1] || "";
    const filename = disposition.match(/filename="([^"]*)"/)?.[1] || "";
    parts.push({ name, filename, body });
    start = next;
  }
  return parts;
}

async function handleApi(req, res, url) {
  if (url.pathname === "/api/photos") {
    const [catalog, reportRows, manualRows, overrides, productOverrides] = await Promise.all([
      readJson(path.join(publicDir, "catalog.json"), { products: [] }),
      readPhotoReport(),
      readManualMedia(),
      readJson(overridesPath, {}),
      readJson(productOverridesPath, {}),
    ]);
    const rows = [...reportRows, ...manualRows];
    const products = catalog.products.map((product) => ({
      code: product.code,
      title: product.title,
      customTitle: productOverrides[product.code]?.title || "",
      category: product.category,
      price: product.price,
      status: product.status,
      currentImages: product.images,
      sourcePhotos: rows
        .filter((row) => row.Codigo === product.code)
        .map((row) => ({
          fileName: path.basename(row.DestinoArquivo),
          path: row.DestinoArquivo,
          url: `/local-photo?path=${encodeURIComponent(row.DestinoArquivo)}`,
          mediaType: [".mp4", ".mov", ".webm"].includes(path.extname(row.DestinoArquivo).toLowerCase()) ? "video" : "image",
          manual: row.Manual === "1",
        })),
      override: overrides[product.code] || { primary: "", order: [], hidden: [] },
    }));
    sendJson(res, { products, overrides, productOverrides });
    return;
  }

  if (url.pathname === "/api/overrides" && req.method === "POST") {
    const body = JSON.parse(await readBody(req));
    await writeFile(overridesPath, `${JSON.stringify(body, null, 2)}\n`, "utf8");
    sendJson(res, { ok: true });
    return;
  }

  if (url.pathname === "/api/product-overrides" && req.method === "POST") {
    const body = JSON.parse(await readBody(req));
    await writeFile(productOverridesPath, `${JSON.stringify(body, null, 2)}\n`, "utf8");
    sendJson(res, { ok: true });
    return;
  }

  if (url.pathname === "/api/upload" && req.method === "POST") {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const parts = parseMultipart(Buffer.concat(chunks), req.headers["content-type"] || "");
    const code = sanitizeCode(parts.find((part) => part.name === "code")?.body.toString("utf8") || "");
    const filePart = parts.find((part) => part.name === "media" && part.filename);
    if (!code || !filePart) throw new Error("Produto ou arquivo ausente");
    const ext = path.extname(filePart.filename).toLowerCase();
    if (!allowedMediaExtensions.has(ext)) throw new Error("Formato nao permitido");
    const folder = path.join(manualMediaDir, code);
    await mkdir(folder, { recursive: true });
    const base = sanitizeBaseName(path.basename(filePart.filename, ext));
    const target = path.join(folder, `${code}_${Date.now()}_${randomUUID().slice(0, 8)}_${base}${ext}`);
    await writeFile(target, filePart.body);
    sendJson(res, { ok: true, fileName: path.basename(target), path: target });
    return;
  }

  res.writeHead(404);
  res.end("Not found");
}

function serveFile(res, file) {
  if (!existsSync(file)) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }
  const ext = path.extname(file).toLowerCase();
  res.writeHead(200, { "content-type": mime[ext] || "application/octet-stream", "cache-control": "no-store" });
  createReadStream(file).pipe(res);
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url || "/", `http://localhost:${port}`);
    if (url.pathname.startsWith("/api/")) {
      await handleApi(req, res, url);
    } else if (url.pathname === "/local-photo") {
      const file = safeLocalPhotoPath(url.searchParams.get("path") || "");
      if (!file) {
        res.writeHead(403);
        res.end("Forbidden");
      } else {
        serveFile(res, file);
      }
    } else if (url.pathname === "/admin/photos") {
      serveFile(res, path.join(publicDir, "admin", "photos.html"));
    } else {
      const relative = url.pathname === "/" ? "index.html" : url.pathname.slice(1);
      serveFile(res, path.join(publicDir, relative));
    }
  } catch (error) {
    res.writeHead(500, { "content-type": "text/plain; charset=utf-8" });
    res.end(error instanceof Error ? error.stack : String(error));
  }
});

server.listen(port, () => {
  console.log(`Photo admin: http://127.0.0.1:${port}/admin/photos`);
});
