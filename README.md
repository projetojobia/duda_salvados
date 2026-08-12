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
npm run drop:admin
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

## Drops relampago

Rode:

```bash
npm run drop:admin
```

Abra `http://127.0.0.1:8791/admin/drop.html`. O painel permite selecionar os produtos do catalogo, definir titulo e mensagem, escolher a duracao, ajustar a expiracao e ativar ou desativar o drop.

`Salvar rascunho` atualiza somente `public/drop.json` no computador. `Publicar drop` salva o arquivo, cria commit e envia a alteracao para a branch `main`, usando o fluxo de deploy ja configurado para o site.

A pagina publica do drop continua em `/drop.html`. Produtos vendidos, reservados ou ocultos aparecem como indisponiveis para novas selecoes no painel.

## Fluxo oficial

1. Enviar foto do produto no Codex/Hermes.
2. O agente identifica o produto, pesquisa referencias e sugere preco.
3. O produto e cadastrado primeiro na planilha local oficial.
4. Fotos sao organizadas e associadas ao codigo DS.
5. A curadoria permite revisar foto principal, titulo visual, vendido e oculto.
6. `Publicar catalogo` fecha a rodada: sincroniza Google Sheets quando possivel, gera catalogo, envia GitHub e atualiza Cloudflare.
7. Quando houver campanha, `drop:admin` seleciona poucos produtos e publica um link temporario para o grupo.
