# Duda Salvados - Hermes/Codex Context

## Objetivo

O projeto Duda Salvados usa um agente operacional chamado Hermes/Emis para administrar produtos de logistica reversa: cadastro, pesquisa de preco, estoque, catalogo, reservas, vendas e acompanhamento financeiro.

O fluxo agora e local-first: a planilha `.xlsx` no PC e a fonte de trabalho diaria; a subida para o Google Sheets acontece depois que a rodada estiver fechada. O Codex deve atuar como camada de engenharia e automacao: criar helpers, fluxos seguros, validacoes, pesquisa de preco e, depois, sincronizacao/publicacao.

## Planilha Oficial

- Nome: Duda Salvados
- Google Sheets ID: `1kqLutUpgQwwnJgHmR7wrJ97zvQR8QZGRB6QyymM4GPU`
- URL: `https://docs.google.com/spreadsheets/d/1kqLutUpgQwwnJgHmR7wrJ97zvQR8QZGRB6QyymM4GPU/edit`
- Origem restaurada: backup local/importado do arquivo `Duda_Salvados_Hermes_GoogleSheets_v2_dashboard_executivo.xlsx`
- ID antigo bloqueado/inacessivel pela conexao atual: `12hkBY8_gDjy0wM7e301uZFcLqrA6_gZ79NZ8v5ZlHp4`
- Aba principal: `Produtos`
- Aba de custos: `Custos Operacionais`
- Linhas template: `DS001` a `DS300`
- Codigo livre: primeira linha em que `A` contem `DSxxx` e `B:AE` estao vazios.

## Arquivos Locais Confirmados

- Workspace: `C:\Users\User\duda`
- Modelo historico/local: `C:\Users\User\duda\Duda_Salvados_Hermes_GoogleSheets_v2.xlsx`
- Client secret copiado no workspace: `C:\Users\User\duda\client_secret.json`
- Instalacao Hermes: `C:\Users\User\AppData\Local\hermes`
- Credencial OAuth Hermes: `C:\Users\User\AppData\Local\hermes\google_client_secret.json`
- Token OAuth Hermes: `C:\Users\User\AppData\Local\hermes\google_token.json`
- Wrapper Google: `C:\Users\User\AppData\Local\hermes\skills\productivity\google-workspace\scripts\google_api.py`
- Helper local: `C:\Users\User\duda\local_sheets_helper.py`
- Sincronizador local->Google: `C:\Users\User\duda\sync_local_workbook_to_google.py`
- Memorias Hermes:
  - `C:\Users\User\AppData\Local\hermes\memories\MEMORY.md`
  - `C:\Users\User\AppData\Local\hermes\memories\USER.md`

## Colunas da Aba Produtos

| Letra | Campo |
| --- | --- |
| A | Codigo |
| B | Data cadastro |
| C | Categoria |
| D | Produto / descricao |
| E | Marca |
| F | Modelo |
| G | Condicao |
| H | Testado? |
| I | Funcionamento |
| J | Status interno |
| K | Localizacao fisica |
| L | Foto principal (URL) |
| M | Pasta / fotos (URL) |
| N | Preco baixo IA (R$) |
| O | Preco medio IA (R$) |
| P | Preco alto IA (R$) |
| Q | Fonte precos / URL |
| R | Custo estimado ref. (R$) |
| S | Preco sugerido IA (R$) |
| T | Preco definido (R$) |
| U | Vantagem ref. mercado (R$) |
| V | Vantagem ref. mercado (%) |
| W | Publicar no WhatsApp? |
| X | Status catalogo |
| Y | Descricao para anuncio |
| Z | Data venda |
| AA | Preco venda real (R$) |
| AB | Lucro real ref. (R$) |
| AC | Cliente (opcional) |
| AD | Observacoes |
| AE | Ultima atualizacao |

## Regras de Ouro

- Consultar a planilha antes de responder sobre estoque, status, preco ou financeiro.
- A primeira escrita deve acontecer na planilha local do PC. A planilha Google e atualizada via `sync_local_workbook_to_google.py` quando a rodada estiver pronta ou pelo botao `Publicar catalogo` da curadoria.
- Investimento do pallet fica na aba `Lote`; despesas recorrentes/operacionais ficam na aba `Custos Operacionais`.
- Nunca inventar codigo; sempre localizar o primeiro `DSxxx` livre.
- Antes de gravar, reler a linha.
- Depois de gravar, reler e confirmar.
- Nunca alterar multiplas linhas para um unico produto.
- Nunca excluir ou limpar linha sem autorizacao explicita.
- Preservar formulas nas colunas `R`, `U`, `V`, `AB`.
- As colunas `U/V` nao representam lucro do produto. Elas representam apenas a vantagem/desconto do preco Duda em relacao a referencia media/alta de mercado: `U = R - T` e `V = (R - T) / R`.
- Sempre atualizar `AE` quando modificar uma linha.
- Preco definido (`T`) deve ser preenchido automaticamente em novos cadastros com o preco sugerido arredondado comercialmente pelo Codex, salvo quando o usuario informar outro valor no pedido. Se o usuario pedir alteracao depois, atualizar `T` e manter a decisao do usuario como prevalente.
- Condicao/teste/funcionamento nao devem ser presumidos.
- Fotos devem ser confirmadas no Drive antes de afirmar que foram salvas.
- Para este pallet de logistica reversa da Shopee, a pesquisa de preco deve priorizar a Shopee como base principal. Mercado Livre, Amazon e outras fontes podem entrar como apoio/comparativo, mas o preco baixo e a sugestao devem considerar primeiro anuncios Shopee equivalentes, inclusive promocao/cupom quando claramente indicado.
- Como sao produtos salvados, o preco sugerido nunca deve ser maior que a referencia equivalente da Shopee. A sugestao deve ficar entre 50% abaixo e 10% abaixo da referencia Shopee escolhida, ajustando pela condicao, teste, avarias, completude e urgencia de giro.
- A referencia de menor preco deve corresponder ao produto da foto. Classificar cada achado como `mesmo produto`, `equivalente forte`, `parecido` ou `descartar`. Usar `N` apenas com `mesmo produto`; se usar equivalente forte por falta de igual, registrar baixa/media confianca em `AD`.
- Anuncios internacionais ou com indicacao de importacao/impostos nao devem ser usados como base de preco em `N/O/P`, pois podem ter encargos adicionais e prazo diferente. Usar apenas anuncios de venda nacional como base. Anuncios internacionais podem ficar apenas em observacao quando ajudarem a identificar modelo/imagem.

## Divergencia A Resolver

Existe conflito entre o relatorio transferido e a memoria atual do Hermes:

- Relatorio: `R = 50% x N`, descrito como custo estimado.
- Memoria Hermes: protocolo v3 diz que `R = (O + P) / 2`, como referencia media/alta de propaganda; `N` orienta o preco Duda e `T` manual prevalece.

Antes de automatizar precificacao e catalogo, decidir qual regra deve valer na planilha atual.

## Politica de Preco Sugerido

Base principal: menor referencia Shopee equivalente e confiavel, priorizando item igual ou muito parecido.

Somente anuncios nacionais podem alimentar `N/O/P`. Se a unica correspondencia visual forte for internacional, nao preencher preco como base final; registrar a imagem/modelo em observacoes e buscar equivalente nacional antes de sugerir `S/T`.

Faixa permitida:

- Alta saida: `S = N * 0,90` (10% abaixo do menor preco Shopee)
- Media saida: `S = N * 0,75` (25% abaixo do menor preco Shopee)
- Baixa saida: `S = N * 0,50` (50% abaixo do menor preco Shopee)

Orientacao dentro da faixa:

- Alta saida: produto comum, facil de vender, procura ampla, utilidade clara, preco popular.
- Media saida: produto util e vendavel, mas com publico mais especifico, teste parcial, marca incerta ou ticket medio.
- Baixa saida: produto muito especifico/nichado, baixa procura, eletronico incerto, avaria, incompleto ou maior risco.
- Com defeito, incompleto ou funcionamento incerto relevante: pedir confirmacao humana; pode ficar abaixo de 50% se o usuario autorizar.

Referencia para anuncio:

- `R = (O + P) / 2`
- Vantagem em reais: `U = R - T`
- Percentual de vantagem no anuncio: `V = (R - T) / R`
- Texto recomendado: `Referencia media/alta de mercado: R$ X / Preco Duda: R$ T / Y% abaixo da referencia de mercado`

O campo `Preco definido (T)` deve ser preenchido automaticamente nos novos cadastros com a sugestao arredondada comercialmente. Exemplos de arredondamento: R$19,79 vira R$20,00; R$21,74 pode virar R$22,00 ou R$20,00 conforme atratividade do anuncio; valores maiores devem buscar numeros comerciais simples. Se o usuario decidir explicitamente outro valor, a decisao dele prevalece.

## Resultado Financeiro Real

Como o pallet foi comprado por lote fechado, nao existe custo unitario confiavel por produto. Portanto, nao calcular lucro estimado por produto com base em referencia de mercado.

Resultado real do pallet deve ser acompanhado no painel por:

- Receita real de vendas: soma de `Produtos!AA`
- Investimento do pallet: `Lote!B9`
- Despesas operacionais: aba `Custos Operacionais`
- Resultado real do pallet: receita real de vendas - investimento do pallet - despesas operacionais

## Proximas Implementacoes

1. Criar helper seguro para Google Sheets.
2. Testar leitura da aba `Produtos`.
3. Testar preservacao de formulas em `R`, `U`, `V`, `AB` sem editar valores reais desnecessariamente.
4. Implementar operacoes: localizar codigo livre, ler linha, atualizar campo, definir preco, reservar, vender.
5. Implementar pesquisa de preco com fontes atuais e comparaveis.
6. Gerar descricao curta para anuncio.
7. Criar catalogo a partir da planilha.

## Custos Operacionais

A aba `Custos Operacionais` registra despesas separadas do investimento do pallet. Campos:

- Data
- Categoria
- Descricao
- Valor (R$)
- Forma pagamento
- Relacionado ao DS
- Comprovante/URL
- Observacoes

Categorias iniciais sugeridas:

- Embalagem
- Frete/Transporte
- Anuncio/Marketing
- Taxa/Marketplace
- Limpeza/Manutencao
- Outros

Resumo atual:

- Total de despesas operacionais: soma `D6:D1000`
- Investimento pallet: referencia `Lote!B9`
- Total geral considerado: investimento do pallet + despesas operacionais
