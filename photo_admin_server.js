import { createReadStream, existsSync } from "node:fs";
import { readFile, writeFile } from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(root, "public");
const reportPath = path.join(root, "photo_rename_report.csv");
const overridesPath = path.join(root, "catalog_photo_overrides.json");
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
};

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
  const photoRoot = path.resolve(root, "Fotos_Organizadas");
  if (!resolved.startsWith(photoRoot)) return null;
  return resolved;
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

async function handleApi(req, res, url) {
  if (url.pathname === "/api/photos") {
    const [catalog, rows, overrides] = await Promise.all([
      readJson(path.join(publicDir, "catalog.json"), { products: [] }),
      readPhotoReport(),
      readJson(overridesPath, {}),
    ]);
    const products = catalog.products.map((product) => ({
      code: product.code,
      title: product.title,
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
        })),
      override: overrides[product.code] || { primary: "", order: [], hidden: [] },
    }));
    sendJson(res, { products, overrides });
    return;
  }

  if (url.pathname === "/api/overrides" && req.method === "POST") {
    const body = JSON.parse(await readBody(req));
    await writeFile(overridesPath, `${JSON.stringify(body, null, 2)}\n`, "utf8");
    sendJson(res, { ok: true });
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
