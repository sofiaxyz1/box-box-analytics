import fastf1
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns

fastf1.Cache.enable_cache('../data/cache')

def processar_quali(ano, gp):
    session = fastf1.get_session(ano, gp, 'Q')
    session.load()

    registros = []

    for piloto in session.drivers:
        volta = session.laps.pick_drivers(piloto).pick_fastest()
        if volta is None:
            continue  # piloto sem volta cronometrada nessa sessão
        registros.append({
            'Piloto': volta['Driver'],
            'Equipe': volta['Team'],
            'S1': volta['Sector1Time'].total_seconds(),
            'S2': volta['Sector2Time'].total_seconds(),
            'S3': volta['Sector3Time'].total_seconds(),
            'Tempo de Volta': volta['LapTime'].total_seconds(),
        })

    df_quali = pd.DataFrame(registros)

    grid = session.results[['Abbreviation', 'Position']]

    df_final = df_quali.merge(grid, left_on='Piloto', right_on='Abbreviation')

    df_final = df_final.drop(columns=['Abbreviation'])
    df_final['Position'] = df_final['Position'].astype(int)

    df_final['Ano'] = ano
    df_final['GP'] = session.event['EventName']

    return df_final

def processar_corrida(ano, gp):
    session = fastf1.get_session(ano, gp, 'R')
    session.load()

    session.laps['LapTimeSeconds'] = session.laps['LapTime'].dt.total_seconds()
    session.laps['VoltaNoStint'] = session.laps.groupby(['Driver', 'Stint']).cumcount() + 1

    session.laps['Ano'] = ano
    session.laps['GP'] = session.event['EventName']

    return session.laps

def plotar_estrategia(laps):
    resumo_stints = laps.groupby(['Driver', 'Stint', 'Compound']).size().reset_index(name='Voltas')
    resumo_stints['Inicio'] = resumo_stints.groupby('Driver')['Voltas'].cumsum() - resumo_stints['Voltas']
    cores = {'SOFT': 'red', 'MEDIUM': 'gold', 'HARD': 'lightgray', 'INTERMEDIATE': 'green', 'WET': 'blue'}
    resumo_stints['Cor'] = resumo_stints['Compound'].map(cores)

    plt.figure(figsize=(12, 8))
    plt.barh(y=resumo_stints['Driver'], width=resumo_stints['Voltas'], left=resumo_stints['Inicio'], color=resumo_stints['Cor'])
    plt.xlabel('Volta')
    plt.ylabel('Piloto')

    gp = laps['GP'].iloc[0]
    ano = laps['Ano'].iloc[0]
    plt.title(f'Estratégia de pneus — {gp} {ano}')

    legenda = []
    for composto, cor in cores.items():
        legenda.append(Patch(color=cor, label=composto))
    plt.legend(handles=legenda, title='Composto')
    plt.show()

def plotar_degradacao(laps):
    grade = sns.relplot(
        data=laps,
        x='VoltaNoStint', y='LapTimeSeconds',
        hue='Compound', units='Stint', estimator=None,
        col='Driver', col_wrap=5,
        kind='line', height=2.5
    )
    grade.set(ylim=(90, 115))

    gp = laps['GP'].iloc[0]
    ano = laps['Ano'].iloc[0]
    grade.fig.suptitle(f'Degradação por composto — {gp} {ano}', y=1.02)
    plt.show()

def ultrapassagens_estrategia(laps):
    laps = laps.sort_values(['GP', 'Driver', 'LapNumber'])
    laps['MudancaPosicao'] = laps.groupby(['GP', 'Driver'])['Position'].diff()
    laps['VoltaDePit'] = laps['PitInTime'].notna() | laps['PitOutTime'].notna()

    ultrapassagens_reais = laps[~laps['VoltaDePit']].groupby(['GP', 'Driver'])['MudancaPosicao'].sum()
    mudanca_pits = laps[laps['VoltaDePit']].groupby(['GP', 'Driver'])['MudancaPosicao'].sum()
    ultrapassagens_liquidas = laps.groupby(['GP', 'Driver'])['MudancaPosicao'].sum()

    pd_ultrapassagens = pd.DataFrame({'Ultrapassagens reais': ultrapassagens_reais, 'Mudancas de posicao (pitstop)': mudanca_pits, 'Ultrapassagens liquidas': ultrapassagens_liquidas})

    return pd_ultrapassagens
