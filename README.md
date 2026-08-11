# Duda Salvados

Catalogo web e automacoes operacionais do projeto Duda Salvados.

## Base oficial restaurada

Google Sheets: https://docs.google.com/spreadsheets/d/1kqLutUpgQwwnJgHmR7wrJ97zvQR8QZGRB6QyymM4GPU/edit

O catalogo e gerado a partir do backup local `Duda_Salvados_Hermes_GoogleSheets_v2_dashboard_executivo.xlsx` e das fotos organizadas em `Fotos_Organizadas`.

## Comandos

```bash
npm run catalog:build
npm run sheets:sync:dry-run
npm run sheets:sync
npm run photos:admin
npm run flow:publish
npm run flow:publish:local
npm run cf:dev
npm run cf:dry-run
npm run cf:deploy
```

## Publicacao

O Worker serve os arquivos estaticos de `public/` via Cloudflare Workers Assets e mantem `/health` como endpoint de diagnostico.

## Curadoria de fotos

Rode:

```bash
npm run photos:admin
```

Abra `http://127.0.0.1:8790/admin/photos` para escolher a foto principal, ocultar imagens ruins, reordenar fotos por produto, carregar fotos ou videos manuais, ajustar o titulo exibido no catalogo, marcar produtos como vendidos e ocultar produtos do catalogo publico.

As escolhas de fotos ficam em `catalog_photo_overrides.json`. Os titulos editados ficam em `catalog_product_overrides.json`. Arquivos enviados manualmente ficam em `catalog_manual_media/`.

Use `Salvar escolhas` para gravar somente no computador. Use `Publicar catalogo` para salvar, tentar sincronizar a planilha local com o Google Sheets restaurado, regenerar o catalogo, criar um commit e enviar para o GitHub/Cloudflare.

Se a credencial Google estiver indisponivel, o catalogo ainda pode ser publicado a partir da planilha local. Nesse caso, a planilha Google deve ser reconectada/sincronizada depois.

## Fluxo oficial

1. Enviar foto do produto no Codex.
2. Codex identifica o produto, pesquisa referencias e sugere preco.
3. Codex cadastra primeiro na planilha local oficial.
4. Fotos sao organizadas e associadas ao codigo DS.
5. A curadoria permite revisar foto principal, titulo visual, vendido e oculto.
6. `Publicar catalogo` fecha a rodada: sincroniza Google Sheets quando possivel, gera catalogo, envia GitHub e atualiza Cloudflare.
