import { createReadStream, existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { randomUUID } from "node:crypto";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(root, "public");
const reportPath = path.join(root, "photo_rename_report.csv");
const overridesPath = path.join(root, "catalog_photo_overrides.json");
const productOverridesPath = path.join(root, "catalog_product_overrides.json");
const manualMediaDir = path.join(root, "catalog_manual_media");
const workbookPath = path.join(root, "Duda_Salvados_Hermes_GoogleSheets_v2_dashboard_executivo.xlsx");
const port = Number(process.env.PORT || 8790);
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
  const text = await readFile(file, "utf8");
  return JSON.parse(text.replace(/^\uFEFF/, ""));
}

function extractFirstUrl(text) {
  const match = String(text || "").match(/https?:\/\/[^\s)"'<]+/i);
  return match?.[0] || "";
}

async function readPricingSources() {
  if (!existsSync(workbookPath)) return {};
  const script = [
    "import json, openpyxl, sys",
    "wb=openpyxl.load_workbook(sys.argv[1], data_only=True)",
    "ws=wb['Produtos']",
    "items={}",
    "for row in ws.iter_rows(min_row=2, max_row=301, values_only=True):",
    "    code=str(row[0] or '').strip()",
    "    if code:",
    "        items[code]=str(row[16] or '').strip()",
    "print(json.dumps(items, ensure_ascii=False))",
  ].join("\n");
  try {
    const { stdout } = await execFileAsync("python", ["-c", script, workbookPath], {
      cwd: root,
      windowsHide: true,
      maxBuffer: 1024 * 1024 * 4,
    });
    return JSON.parse(stdout || "{}");
  } catch {
    return {};
  }
}

async function readDashboard() {
  if (!existsSync(workbookPath)) return { finance: [], operation: [], charts: {} };
  const script = [
    "import json, openpyxl, sys",
    "wb=openpyxl.load_workbook(sys.argv[1], data_only=True)",
    "overrides=json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 and sys.argv[2] else {}",
    "ws=wb['Painel']",
    "products=wb['Produtos']",
    "def value(cell):",
    "    v=ws[cell].value",
    "    return v if v is not None else ''",
    "def num(v):",
    "    try:",
    "        if v in (None, ''):",
    "            return 0.0",
    "        return float(str(v).replace('R$', '').replace('.', '').replace(',', '.'))",
    "    except Exception:",
    "        return 0.0",
    "investment=num(value('B4'))",
    "revenue=0.0",
    "potential_total=0.0",
    "potential_available=0.0",
    "counts={'Produtos cadastrados': 0, 'Aguardando análise': 0, 'Aguardando preço': 0, 'Prontos para publicar': 0, 'Disponíveis': 0, 'Reservados': 0, 'Vendidos': 0, 'Defeito / descartado': 0, 'Publicados no catálogo': 0, 'A atualizar no catálogo': 0, 'Produtos testados': 0}",
    "for row in products.iter_rows(min_row=2, max_row=301, values_only=True):",
    "    code=str(row[0] or '').strip()",
    "    if not code.startswith('DS'):",
    "        continue",
    "    if not any(v not in (None, '') for v in row[1:]):",
    "        continue",
    "    override=overrides.get(code, {})",
    "    status=str(row[9] or '').strip()",
    "    catalog_status=str(row[23] or '').strip()",
    "    price=num(override.get('price') if override.get('price') not in (None, '') else row[19])",
    "    quantity=max(1, int(num(row[31]) or 1))",
    "    sale=num(row[26]) or price",
    "    if override.get('sold'):",
    "        status='Vendido'",
    "        catalog_status='Vendido'",
    "    elif override.get('reserved'):",
    "        status='Reservado'",
    "        catalog_status='Reservado'",
    "    elif override.get('hidden'):",
    "        catalog_status='Oculto'",
    "    counts['Produtos cadastrados'] += 1",
    "    if status in counts:",
    "        counts[status] += 1",
    "    if status == 'Disponível':",
    "        counts['Disponíveis'] += 1",
    "    elif status == 'Pronto para publicar':",
    "        counts['Prontos para publicar'] += 1",
    "    elif status == 'Aguardando análise':",
    "        counts['Aguardando análise'] += 1",
    "    elif status == 'Aguardando preço':",
    "        counts['Aguardando preço'] += 1",
    "    if status == 'Vendido' or catalog_status == 'Vendido':",
    "        counts['Vendidos'] += 1",
    "        revenue += sale * quantity",
    "    elif status == 'Reservado' or catalog_status == 'Reservado':",
    "        counts['Reservados'] += 0 if status == 'Reservado' else 1",
    "        potential_total += price * quantity",
    "    elif catalog_status != 'Oculto':",
    "        potential_total += price * quantity",
    "        if status in ('Disponível', 'Pronto para publicar', 'Publicado'):",
    "            potential_available += price * quantity",
    "    if str(row[7] or '').strip().lower() in ('sim', 'testado', 'ok'):",
    "        counts['Produtos testados'] += 1",
    "remaining=max(0, investment-revenue)",
    "projected=potential_total-investment",
    "recovered=(revenue/investment) if investment else 0",
    "finance=[]",
    "operation=[]",
    "for row in range(4, 18):",
    "    if value(f'A{row}') != '':",
    "        label=value(f'A{row}')",
    "        val=value(f'B{row}')",
    "        if label == 'Receita já realizada': val=revenue",
    "        elif label == 'Saldo para recuperar investimento': val=remaining",
    "        elif label == '% investimento recuperado': val=recovered",
    "        elif label == 'Valor potencial disponível': val=potential_available",
    "        elif label == 'Valor potencial total (preço definido)': val=potential_total",
    "        elif label == 'Projeção resultado do lote': val=projected",
    "        elif label == 'Retorno projetado sobre investimento': val=(projected/investment) if investment else 0",
    "        finance.append({'label': label, 'value': val})",
    "    if value(f'D{row}') != '':",
    "        label=value(f'D{row}')",
    "        operation.append({'label': label, 'value': counts.get(label, value(f'E{row}'))})",
    "charts={",
    "    'costCoverage': {'recovered': revenue, 'remaining': remaining, 'percent': recovered},",
    "    'profit': {'investment': investment, 'potential': potential_total, 'projectedResult': projected},",
    "}",
    "print(json.dumps({'finance': finance, 'operation': operation, 'charts': charts}, ensure_ascii=False))",
  ].join("\n");
  try {
    const { stdout } = await execFileAsync("python", ["-c", script, workbookPath, productOverridesPath], {
      cwd: root,
      windowsHide: true,
      maxBuffer: 1024 * 1024 * 4,
    });
    return JSON.parse(stdout || "{}");
  } catch {
    return { finance: [], operation: [], charts: {} };
  }
}

async function writeProductPrices(priceUpdates) {
  const safeUpdates = {};
  for (const [rawCode, rawPrice] of Object.entries(priceUpdates || {})) {
    const code = sanitizeCode(rawCode);
    const price = Number(String(rawPrice || "").replace(",", "."));
    if (code && Number.isFinite(price) && price >= 0) {
      safeUpdates[code] = Math.round(price);
    }
  }
  if (!Object.keys(safeUpdates).length) return { ok: true, updated: [] };

  const tempFile = path.join(root, `.price-updates-${Date.now()}-${randomUUID().slice(0, 8)}.json`);
  await writeFile(tempFile, JSON.stringify(safeUpdates), "utf8");
  const script = [
    "import json, sys, openpyxl",
    "workbook_path=sys.argv[1]",
    "updates=json.load(open(sys.argv[2], encoding='utf-8'))",
    "wb=openpyxl.load_workbook(workbook_path)",
    "ws=wb['Produtos']",
    "updated=[]",
    "for row in range(2, 302):",
    "    code=str(ws.cell(row, 1).value or '').strip()",
    "    if code in updates:",
    "        ws.cell(row, 20).value=float(updates[code])",
    "        updated.append(code)",
    "wb.save(workbook_path)",
    "print(json.dumps({'updated': updated}, ensure_ascii=False))",
  ].join("\n");

  try {
    const { stdout } = await execFileAsync("python", ["-c", script, workbookPath, tempFile], {
      cwd: root,
      windowsHide: true,
      maxBuffer: 1024 * 1024 * 4,
    });
    const result = JSON.parse(stdout || "{}");
    return { ok: true, updated: result.updated || [] };
  } catch (error) {
    const details = `${error.message || ""}\n${error.stderr || ""}`;
    if (details.includes("Permission denied")) {
      return {
        ok: true,
        updated: [],
        workbookUpdated: false,
        warning: "Planilha local aberta ou travada; preco salvo para o catalogo.",
      };
    }
    return {
      ok: false,
      message: error.message || String(error),
      stdout: error.stdout || "",
      stderr: error.stderr || "",
    };
  } finally {
    const { rm } = await import("node:fs/promises");
    await rm(tempFile, { force: true }).catch(() => {});
  }
}

async function writeProductOperations(productUpdates) {
  const safeUpdates = {};
  for (const [rawCode, rawUpdate] of Object.entries(productUpdates || {})) {
    const code = sanitizeCode(rawCode);
    if (!code || !rawUpdate || typeof rawUpdate !== "object") continue;
    safeUpdates[code] = {
      title: String(rawUpdate.title || "").trim(),
      price: rawUpdate.price === undefined || rawUpdate.price === "" ? "" : Math.round(Number(rawUpdate.price)),
      referencePrice:
        rawUpdate.referencePrice === undefined || rawUpdate.referencePrice === ""
          ? ""
          : Math.round(Number(rawUpdate.referencePrice)),
      sold: Boolean(rawUpdate.sold),
      reserved: Boolean(rawUpdate.reserved),
      hidden: Boolean(rawUpdate.hidden),
    };
    if (!Number.isFinite(safeUpdates[code].price)) safeUpdates[code].price = "";
    if (!Number.isFinite(safeUpdates[code].referencePrice)) safeUpdates[code].referencePrice = "";
  }
  if (!Object.keys(safeUpdates).length) return { ok: true, updated: [] };

  const tempFile = path.join(root, `.product-updates-${Date.now()}-${randomUUID().slice(0, 8)}.json`);
  await writeFile(tempFile, JSON.stringify(safeUpdates), "utf8");
  const script = [
    "import json, sys, openpyxl",
    "from datetime import datetime",
    "workbook_path=sys.argv[1]",
    "updates=json.load(open(sys.argv[2], encoding='utf-8'))",
    "wb=openpyxl.load_workbook(workbook_path)",
    "ws=wb['Produtos']",
    "now=datetime.now().strftime('%d/%m/%Y %H:%M:%S')",
    "updated=[]",
    "for row in range(2, 302):",
    "    code=str(ws.cell(row, 1).value or '').strip()",
    "    item=updates.get(code)",
    "    if not item:",
    "        continue",
    "    if item.get('title'):",
    "        ws.cell(row, 6).value=item['title']",
    "    if item.get('price') != '':",
    "        ws.cell(row, 20).value=float(item['price'])",
    "    if item.get('referencePrice') != '':",
    "        ws.cell(row, 15).value=float(item['referencePrice'])",
    "        ws.cell(row, 16).value=float(item['referencePrice'])",
    "    if item.get('sold'):",
    "        ws.cell(row, 10).value='Vendido'",
    "        ws.cell(row, 24).value='Vendido'",
    "        if not ws.cell(row, 26).value:",
    "            ws.cell(row, 26).value=now",
    "    elif item.get('reserved'):",
    "        ws.cell(row, 10).value='Reservado'",
    "        ws.cell(row, 24).value='Reservado'",
    "    elif item.get('hidden'):",
    "        ws.cell(row, 24).value='Oculto'",
    "    ws.cell(row, 31).value=now",
    "    updated.append(code)",
    "wb.save(workbook_path)",
    "print(json.dumps({'updated': updated}, ensure_ascii=False))",
  ].join("\n");

  try {
    const { stdout } = await execFileAsync("python", ["-c", script, workbookPath, tempFile], {
      cwd: root,
      windowsHide: true,
      maxBuffer: 1024 * 1024 * 4,
    });
    const result = JSON.parse(stdout || "{}");
    return { ok: true, updated: result.updated || [], workbookUpdated: true };
  } catch (error) {
    const details = `${error.message || ""}\n${error.stderr || ""}`;
    if (details.includes("Permission denied")) {
      return {
        ok: true,
        updated: [],
        workbookUpdated: false,
        warning: "Planilha local aberta ou travada; alteracoes serao aplicadas ao Google Sheets na publicacao.",
      };
    }
    return {
      ok: false,
      message: error.message || String(error),
      stdout: error.stdout || "",
      stderr: error.stderr || "",
    };
  } finally {
    const { rm } = await import("node:fs/promises");
    await rm(tempFile, { force: true }).catch(() => {});
  }
}

function sendJson(res, value) {
  res.writeHead(200, { "content-type": mime[".json"], "cache-control": "no-store" });
  res.end(JSON.stringify(value, null, 2));
}

async function runCommand(command, args) {
  try {
    const isCmd = command.toLowerCase().endsWith(".cmd") || command.toLowerCase().endsWith(".bat");
    const finalCommand = isCmd ? process.env.ComSpec || "cmd.exe" : command;
    const finalArgs = isCmd ? ["/d", "/s", "/c", command, ...args] : args;
    const { stdout, stderr } = await execFileAsync(finalCommand, finalArgs, {
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
  if (url.pathname === "/api/dashboard") {
    sendJson(res, await readDashboard());
    return;
  }

  if (url.pathname === "/api/photos") {
    const [catalog, reportRows, manualRows, overrides, productOverrides, pricingSources] = await Promise.all([
      readJson(path.join(publicDir, "catalog.json"), { products: [] }),
      readPhotoReport(),
      readManualMedia(),
      readJson(overridesPath, {}),
      readJson(productOverridesPath, {}),
      readPricingSources(),
    ]);
    const rows = [...reportRows, ...manualRows];
    const products = catalog.products.map((product) => ({
      code: product.code,
      title: product.title,
      customTitle: productOverrides[product.code]?.title || "",
      category: product.category,
      price: productOverrides[product.code]?.price || product.price,
      referencePrice: productOverrides[product.code]?.referencePrice || product.referencePrice || "",
      status: product.status,
      pricingSource: pricingSources[product.code] || "",
      pricingSourceUrl: extractFirstUrl(pricingSources[product.code]),
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
    const result = await writeProductOperations(body);
    if (!result.ok) {
      res.writeHead(500, { "content-type": mime[".json"], "cache-control": "no-store" });
      res.end(JSON.stringify(result, null, 2));
      return;
    }
    sendJson(res, result);
    return;
  }

  if (url.pathname === "/api/product-prices" && req.method === "POST") {
    const body = JSON.parse(await readBody(req));
    const result = await writeProductPrices(body);
    if (!result.ok) {
      res.writeHead(500, { "content-type": mime[".json"], "cache-control": "no-store" });
      res.end(JSON.stringify(result, null, 2));
      return;
    }
    sendJson(res, result);
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

  if (url.pathname === "/api/publish" && req.method === "POST") {
    const steps = [];
    const skipGoogleSync = url.searchParams.get("skipGoogleSync") === "1";
    const sync = skipGoogleSync
      ? { ok: true, stdout: "Sincronizacao Google ignorada por parametro.", stderr: "" }
      : await runCommand("npm.cmd", ["run", "sheets:sync"]);
    steps.push({ name: "sheets:sync", ...sync });
    const googleSynced = sync.ok && !skipGoogleSync;

    const build = await runCommand("npm.cmd", ["run", "catalog:build"]);
    steps.push({ name: "catalog:build", ...build });
    if (!build.ok) {
      res.writeHead(500, { "content-type": mime[".json"], "cache-control": "no-store" });
      res.end(JSON.stringify({ ok: false, step: "catalog:build", steps }, null, 2));
      return;
    }

    const add = await runCommand("git", [
      "add",
      "catalog_photo_overrides.json",
      "catalog_product_overrides.json",
      ...(existsSync(manualMediaDir) ? ["catalog_manual_media"] : []),
      "public/catalog.json",
      "public/assets/products",
    ]);
    steps.push({ name: "git add", ...add });
    if (!add.ok) {
      res.writeHead(500, { "content-type": mime[".json"], "cache-control": "no-store" });
      res.end(JSON.stringify({ ok: false, step: "git add", steps }, null, 2));
      return;
    }

    const diff = await runCommand("git", ["diff", "--cached", "--quiet"]);
    if (diff.ok) {
      sendJson(res, { ok: true, published: false, message: "Nada novo para publicar.", steps });
      return;
    }

    const commit = await runCommand("git", ["commit", "-m", "Publish catalog updates"]);
    steps.push({ name: "git commit", ...commit });
    if (!commit.ok) {
      res.writeHead(500, { "content-type": mime[".json"], "cache-control": "no-store" });
      res.end(JSON.stringify({ ok: false, step: "git commit", steps }, null, 2));
      return;
    }

    const push = await runCommand("git", ["push", "origin", "main"]);
    steps.push({ name: "git push", ...push });
    if (!push.ok) {
      res.writeHead(500, { "content-type": mime[".json"], "cache-control": "no-store" });
      res.end(JSON.stringify({ ok: false, step: "git push", steps }, null, 2));
      return;
    }

    sendJson(res, {
      ok: true,
      published: true,
      googleSynced,
      googleSyncWarning: sync.ok ? "" : "Google Sheets nao sincronizou; catalogo publicado a partir da planilha local.",
      message: sync.ok
        ? "Catalogo publicado. O Cloudflare pode levar alguns segundos para atualizar."
        : "Catalogo publicado, mas a planilha Google nao sincronizou.",
      steps,
    });
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
