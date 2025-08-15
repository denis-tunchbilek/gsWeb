from flask import Flask, jsonify, render_template, request
import pandas as pd
import threading
import time
from datetime import datetime
import locale
import json
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

app = Flask(__name__)

# Глобальные переменные
table_data = []
df_matches = None
next_date = None
next_opponent = None
galatasaray_form = None
players_stats = None


def update_table():
    global table_data, df_matches, next_date, next_opponent, galatasaray_form, players_stats
    while True:
        try:
            # Загружаем турнирную таблицу
            df = pd.read_html(
                'https://fbref.com/en/comps/26/Super-Lig-Stats',
                attrs={'id': 'results2025-2026261_overall'}
            )[0]
            with open("../gsWeb/logos.json", "r") as f:
                logos = json.load(f)
            df["Logo"] = df["Squad"].map(logos)
            table_data = df.to_dict(orient="records")

            # Запоминаем форму Галатасарая
            galatasaray_row = next((row for row in table_data if row['Squad'] == "Galatasaray"), None)
            if galatasaray_row:
                galatasaray_form = galatasaray_row['Last 5']

            # Загружаем список матчей
            tables = pd.read_html(
                'https://fbref.com/en/squads/ecd11ca2/Galatasaray-Stats#all_matchlogs',
                attrs={'id': 'matchlogs_for'}
            )


            players_stats = pd.read_html('https://fbref.com/en/squads/ecd11ca2/Galatasaray-Stats', attrs={'id': 'stats_standard_26'})[0]
            if tables:
                df_matches = tables[0]
                df_matches = df_matches[df_matches['Date'].notna()]  # убираем пустые строки

                # Находим ближайший матч
                future_matches = df_matches[df_matches['Result'].isna()]
                if not future_matches.empty:
                    next_match_row = future_matches.iloc[0]
                    next_date = next_match_row['Date']
                    next_date = datetime.strptime(next_date, "%Y-%m-%d").strftime("%d %B")
                    next_opponent = next_match_row['Opponent']
                else:
                    next_date = None
                    next_opponent = None
            else:
                print("Таблица матчей не найдена")
                df_matches = None

            print("Data updated")

        except Exception as e:
            print("Error updating data:", e)

        time.sleep(300)  # обновляем каждые 5 минут

# Запускаем обновление данных в отдельном потоке
threading.Thread(target=update_table, daemon=True).start()

@app.route("/")
def index():
    stat = request.args.get('stat', 'goals')
    # Отбираем 7 команд вокруг Галатасарая
    galatasaray_index = next(
        (i for i, row in enumerate(table_data) if row['Squad'] == "Galatasaray"),
        None
    )
    if galatasaray_index is not None:
        start = max(0, galatasaray_index - 5)
        end = galatasaray_index + 6
        filtered_table = table_data[start:end]
        galatasaray_place = int(table_data[galatasaray_index]['Rk'])
    else:
        filtered_table = table_data
        galatasaray_place = None
        
    squad_total = players_stats.iloc[-2]
    gls_column = ('Performance', 'Gls')
    squad_goals = int(squad_total[gls_column])

    return render_template(
        "index.html",
        table=filtered_table,
        galatasaray_place=galatasaray_place,
        next_date=next_date,
        next_opponent=next_opponent,
        galatasaray_form=galatasaray_form,
        players_stats=players_stats,
        stat=stat,
        squad_goals=squad_goals
    )
    
@app.route("/players")
def get_players():
    stat = request.args.get("stat", "goals")    
    if stat == "goals":
        df_simple = players_stats[[('Unnamed: 0_level_0', 'Player'), ('Performance', 'Gls')]]
    else:
        df_simple = players_stats[[('Unnamed: 0_level_0', 'Player'), ('Performance', 'Ast')]]
    df_simple.columns = ['Player', 'Value']
    df_simple = df_simple.sort_values('Value', ascending=False)
    df_simple = df_simple[df_simple['Player'] != 'Squad Total']
    players_list = df_simple.to_dict(orient="records")
    with open("../gsWeb/playersPhotos.json", "r") as f:
        photos = json.load(f)
        for p in players_list:
            p["Photo"] = photos.get(p["Player"])
    players_list = players_list[:5]
    return jsonify(players_list)

if __name__ == "__main__":
    app.run(debug=True)