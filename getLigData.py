import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time



# турнирная таблица

# df_fbref_goals = pd.read_html('https://fbref.com/en/stathead/player_comparison.cgi?request=1&sum=0&comp_type=spec&dom_lg=1&spec_comps=26&player_id1=414b2ce4&p1yrfrom=2025-2026&player_id2=fc4ab056&p2yrfrom=2025-2026&player_id3=26b3d752&p3yrfrom=2025-2026&player_id4=51af19f7&p4yrfrom=2025-2026&player_id5=6460189b&p5yrfrom=2025-2026&player_id6=88e9f529&p6yrfrom=2025-2026&player_id7=8c5f4501&p7yrfrom=2025-2026', attrs={'id': 'shooting_stats'})[0]
# print(df_fbref_goals)
#следующий матч
# df_future_matches = pd.read_html('https://fbref.com/en/squads/ecd11ca2/Galatasaray-Stats', attrs={'id': 'stats_standard_26'})[0]
# print(df_future_matches.columns)


# def fetch_player_photos():
#     players = {}
#     url = "https://www.transfermarkt.com/galatasaray/kader/verein/141"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     resp = requests.get(url, headers=headers)
#     soup = BeautifulSoup(resp.text, "html.parser")
#     players = {}
#     table = soup.find_all("td", class_="posrela")

#     for row in table:
#         name = row.find("img")["alt"]
#         img = row.find_all("img")
#         if len(img)==3:
#             name = img[-1]["alt"]
#             players[name] = img[-1]["data-src"]
#         else:
#             if img[0]:
#                 players[name] = img[0]["data-src"]
#             else:
#                 players[name] = row.find("img").get("src")
#     return json.dumps(players, indent=4, ensure_ascii=False)




# def fetch_club_logos():
#     url = "https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     resp = requests.get(url, headers=headers)
#     soup = BeautifulSoup(resp.text, "html.parser")
#     logos = {}
#     for team in soup.find_all("tr", class_="odd") + soup.find_all("tr", class_="even"):
#         name = team.find("img")["alt"]
#         logo = team.find("img")["src"]
#         logos[name] = logo
#     return json.dumps(logos, indent=4, ensure_ascii=False)

# # photos = fetch_player_photos()
# # with open("playersPhotos.json", "w") as f:
# #     f.write(photos)
# logos = fetch_club_logos()
# with open("logos.json", "w") as f:
#     f.write(logos)
    
    
