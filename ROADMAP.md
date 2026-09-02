# F1 Analytics — Roteiro do Projeto (FastF1)

Portfólio de análise de dados com telemetria de F1 (temporada 2025 completa).
Formato: notebooks Jupyter para a narrativa + módulos Python reutilizáveis em `src/`.

Análises:
1. **Setores de Quali vs. Grid** — correlação estatística entre tempo de cada setor e posição final do grid.
2. **Estratégia de corrida e ultrapassagens** — stints, compostos, pit stops e trocas de posição.

---

## Etapa 0 — Fundação do repositório
- [x] Criar repositório no GitHub 
- [x] Criar ambiente virtual 
- [x] Instalar: `fastf1`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `jupyter`
- [x] Gerar `requirements.txt`
- [x] Estrutura de pastas:
  ```
  box-box-analytics/
  ├── notebooks/
  ├── src/
  ├── data/cache/        # cache do FastF1 (vai no .gitignore!)
  ├── reports/figures/   # gráficos exportados
  ├── README.md
  └── requirements.txt
  ```
- [ ] README inicial: título, objetivo, as duas perguntas de análise

## Etapa 1 — Exploração da API FastF1
Notebook: `notebooks/01_exploracao_fastf1.ipynb`
- [x] Habilitar cache: `fastf1.Cache.enable_cache('data/cache')`
- [x] Carregar UMA sessão de quali (ex: Bahrein 2025) com `fastf1.get_session(2025, 'Bahrain', 'Q')` + `session.load()`
- [x] Explorar `session.laps`: colunas `Sector1Time`, `Sector2Time`, `Sector3Time`, `LapTime`, `Compound`, `Driver`, `Deleted`...
- [x] Explorar `session.results` (posição de grid) e o calendário via `fastf1.get_event_schedule(2025)`
- [x] Anotar no notebook o que cada estrutura contém (isso vira sua documentação mental)

## Etapa 2 — Pipeline de coleta (temporada 2025)
Módulo: `src/data_loader.py` | Notebook: `02_coleta_dados.ipynb`
- [x] Função que percorre o calendário 2025 e baixa todas as sessões de quali
- [ ] Para cada piloto: melhor volta válida + melhores tempos de setor + posição de grid
- [ ] Decidir e documentar: usar setores da *melhor volta real* ou os *melhores setores da sessão* ("volta ideal")? (vale comparar os dois)
- [ ] Tratar: voltas deletadas (`Deleted == True`), pilotos sem tempo, fins de semana sprint (quali de sprint ≠ quali da corrida)
- [ ] Salvar DataFrame consolidado em `data/processed/quali_2025.csv` (ou parquet)

## Etapa 3 — Análise 1: Setores vs. Grid
Notebook: `03_setores_vs_grid.ipynb` | Funções em `src/analysis.py`
- [ ] Normalizar tempos por corrida (Mônaco ~70s/volta, Monza ~80s — não dá pra comparar tempos brutos entre pistas). Opções: z-score por corrida ou delta % para o melhor setor
- [ ] Correlação: **Spearman** (posição de grid é ordinal — justifique isso no notebook, é ouro em entrevista) entre cada setor e a posição
- [ ] Por corrida E agregado da temporada: em quais pistas cada setor "decide" o grid?
- [ ] Visualizações: heatmap setor × corrida, scatter setor vs. posição, ranking de circuitos por setor mais decisivo
- [ ] Extra (opcional): regressão para prever posição a partir dos 3 setores; comparar importância

## Etapa 4 — Análise 2: Estratégia e ultrapassagens
Notebook: `04_estrategia_corrida.ipynb`
- [ ] Carregar sessões de corrida ('R') de 2025
- [ ] Stints: agrupar `laps` por `Driver` + `Stint`, com `Compound` e nº de voltas
- [ ] Gráfico de estratégia (barras horizontais estilo Gantt: piloto × voltas, cor = composto)
- [ ] Degradação: evolução do tempo de volta dentro do stint por composto
- [ ] Ultrapassagens: variação de `Position` volta a volta, filtrando trocas causadas por pit stop (senão você conta "ultrapassagens fantasmas")
- [ ] Perguntas: 1 vs. 2 paradas — o que rendeu mais posições? Undercut funcionou? Em quais pistas se ultrapassa mais?

## Etapa 5 — Refatoração e qualidade
- [ ] Mover funções repetidas dos notebooks para `src/` com docstrings
- [ ] Nomes claros, remover código morto, notebooks rodando do zero (Restart & Run All)
- [ ] `requirements.txt` final com versões

## Etapa 6 — README e apresentação
- [ ] README com: contexto, perguntas, principais achados COM gráficos (exportar para `reports/figures/`), como rodar, estrutura do repo, limitações e próximos passos
- [ ] Descrição e topics no GitHub (`python`, `data-analysis`, `formula1`, `fastf1`)

## Etapa 7 — Verificação final
- [ ] Clonar o repo do zero e rodar tudo seguindo só o README
- [ ] Revisar cada conclusão estatística: o dado sustenta a frase?
- [ ] Checar correlação ≠ causalidade nas interpretações
