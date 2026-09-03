import fastf1
import pandas as pd

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