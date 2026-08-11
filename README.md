# Duda Salvados

Catalogo web e automacoes operacionais do projeto Duda Salvados.

## Base oficial restaurada

Google Sheets: https://docs.google.com/spreadsheets/d/1kqLutUpgQwwnJgHmR7wrJ97zvQR8QZGRB6QyymM4GPU/edit

O catalogo e gerado a partir do backup local `Duda_Salvados_Hermes_GoogleSheets_v2_dashboard_executivo.xlsx` e das fotos organizadas em `Fotos_Organizadas`.

## Comandos

```bash
npm run catalog:build
npm run cf:dev
npm run cf:dry-run
npm run cf:deploy
```

## Publicacao

O Worker serve os arquivos estaticos de `public/` via Cloudflare Workers Assets e mantem `/health` como endpoint de diagnostico.
