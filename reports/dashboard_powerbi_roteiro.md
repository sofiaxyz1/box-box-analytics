# Roteiro — Dashboard Power BI (box-box-analytics)

Dados prontos pra importar em `data/powerbi/` (4 CSVs, derivados dos mesmos CSVs em `data/processed/` que os notebooks já usam — nenhum número novo, só reorganizado/persistido pra ficar fácil de consumir no Power BI):

- `setores_vs_grid.csv` — GP, rho_s1, rho_s2, rho_s3 (24 linhas, 1 por corrida)
- `quali_piloto_corrida.csv` — Piloto, Equipe, S1, S2, S3, Tempo de Volta, Position, Ano, GP (475 linhas)
- `ultrapassagens_piloto_corrida.csv` — GP, Driver, Equipe, UltrapassagensReais, MudancaPits, UltrapassagensLiquidas, Paradas (476 linhas)
- `ultrapassagens_por_pista.csv` — GP, MovimentacaoTotal, Voltas, MovimentacaoPorVolta (24 linhas)

No Power BI: **Get Data > Folder** apontando pra `data/powerbi/` (ou um CSV de cada vez), e criar relacionamento entre as duas tabelas por `GP` (uma relação 1-pra-muitos, já que `setores_vs_grid` e `ultrapassagens_por_pista` têm 1 linha por corrida, e as outras duas têm várias).

## Página 1 — Setores de quali vs. grid

**Visuais:**
1. **3 cartões de KPI** — correlação média de cada setor na temporada: `AVERAGE(setores_vs_grid[rho_s1])`, idem para `rho_s2` e `rho_s3`. Destaca o achado principal (S2 = 0.89, o mais forte).
2. **Gráfico de barras (clustered column)** — eixo X = `GP`, valores = `rho_s1`/`rho_s2`/`rho_s3` lado a lado. Ordenar pelo `rho_s2` pra ver o padrão geral, ou deixar alfabético e usar cor pra destacar Azerbaijão/Bélgica (os outliers).
3. **Tabela/Matrix com formatação condicional** — linhas = `GP`, colunas = os 3 rhos, com escala de cor (vermelho→azul) imitando o heatmap que já existe em `reports/figures/heatmap_setores_grid.png`. No Power BI: botão direito na tabela → *Conditional formatting > Background color > Color scale*.
4. **Scatter** — `S1` (ou setor escolhido num slicer) no eixo X, `Position` no eixo Y, usando `quali_piloto_corrida`. Com um slicer de `GP`, dá pra recriar interativamente o contraste Bahrain (pontos quase numa diagonal) vs. Azerbaijão (espalhados) que está no notebook.

**Slicer:** `GP` (dropdown ou lista).

## Página 2 — Estratégia e ultrapassagens

**Visuais:**
1. **Cartão de KPI** — mediana de `UltrapassagensLiquidas` segmentada por `Paradas` (usa a agregação "Median" do próprio campo no visual, não precisa de DAX customizado) — mostra que 1 e 2 paradas empatam em 0.0.
2. **Gráfico de barras empilhadas (stacked bar)** — eixo Y = `Driver`, valores = `UltrapassagensReais` e `MudancaPits` lado a lado (cores diferentes), filtrado por um `GP` no slicer (ex: Bahrain) — reproduz visualmente a história do VER (+22 real, -20 pit) sem precisar abrir o notebook.
3. **Gráfico de barras horizontal** — eixo Y = `GP` (de `ultrapassagens_por_pista`), valor = `MovimentacaoPorVolta`, ordenado decrescente — mesma conclusão do notebook (Monaco no fim, Bahrain/São Paulo no topo), mas navegável.
4. **Slicers:** `GP`, `Driver` (ou `Equipe`), e um slicer numérico/dropdown de `Paradas`.

**Medida DAX útil (opcional, pra ir além do básico):**
```dax
Media Movimentacao por Volta Geral =
AVERAGE(ultrapassagens_por_pista[MovimentacaoPorVolta])
```
Serve de linha de referência (constant line) no gráfico de barras da pista, pra visualizar quais corridas ficam acima/abaixo da média da temporada.

## Observação

Os números desse dashboard precisam bater exatamente com os dos notebooks (ex: VER Bahrain = -2 líquido) — isso já foi conferido ao gerar os CSVs. Se algum visual no Power BI mostrar algo diferente, o problema está na configuração do visual (agregação errada, filtro faltando), não no dado.
