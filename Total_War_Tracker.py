import requests
from requests import api
from collections import defaultdict
import os
import webbrowser
from dotenv import load_dotenv

# Configuration

load_dotenv()
API_KEY = os.getenv('STEAM_API_KEY')
STEAM_ID = os.getenv('STEAM_ID')
APP_ID = os.getenv('APP_ID')

def get_unlocked_achievements():
    base_url = f"https://api.steampowered.com/"
    params = {
        'appid': APP_ID,
        'key': API_KEY,
        'steamid': STEAM_ID,
        'endpoint': {
            'Achivements': 'ISteamUserStats/GetPlayerAchievements/v0001/?', 
            'Schema': 'ISteamUserStats/GetSchemaForGame/v2/?',
            'Details': 'ISteamUser/GetPlayerSummaries/v0002/?'
            }
    }

    try:
        schema_url = f"{base_url}{params['endpoint']['Schema']}{'&'.join([f'{k}={v}' for k, v in params.items() if k != 'endpoint'])}"
        achievements_url = f"{base_url}{params['endpoint']['Achivements']}{'&'.join([f'{k}={v}' for k, v in params.items() if k != 'endpoint'])}"
        player_url = f"{base_url}{params['endpoint']['Details']}&key={API_KEY}&steamids={STEAM_ID}"
        
        schema_response = requests.get(schema_url).json()
        achievements_response = requests.get(achievements_url).json()
        player_response = requests.get(player_url).json()

        # Build Schema Lookup: Map internal 'name' to the full metadata object
        schema_list = schema_response.get('game', {}).get('availableGameStats', {}).get('achievements', [])
        schema_lookup = {item['name']: item for item in schema_list if "MULTIPLAYER" not in item.get('name', '')}

        game_name = achievements_response.get('playerstats', {}).get('gameName', 'Unknown Game')
        player_persona = player_response.get('response', {}).get('players', [{}])[0].get('personaname', 'Player')

        player_achievements = achievements_response.get('playerstats', {}).get('achievements', [])
        player_achievements_list = [a for a in player_achievements if "MULTIPLAYER" not in a.get('apiname', '')]

        total_sp_achievements = len(player_achievements_list)

        # Filter for unachieved (achieved == 0)
        locked = [a for a in player_achievements_list if a['achieved'] == 0]
        
        html_output = f"<h2>🔒 {player_persona if player_persona != 'Player' else 'Someone'}'s Locked Achievements for {game_name}</h2>"
        html_output += f"<p>Total Achievements: {total_sp_achievements} | Locked Achievements: {len(locked)}</p>"
        
        categories = defaultdict(list)

        for ach in locked:
            apiname = ach['apiname']

            metadata = schema_lookup.get(apiname, {})
            # display_name = metadata.get('displayName', apiname)
            # description = metadata.get('description', 'No description available.')
            # icon_url = metadata.get('icon', '')

            if "WINNING" in apiname:
                categories['🏆 Victory Achievements'].append(metadata)
            elif "PRO10_MOM_ACHIEVEMENT_TRIAL" in apiname:
                categories['⚔️ Trials of Fate'].append(metadata)
            elif "WH3_ACHIEVEMENT_" in apiname:
                # Extract faction name (e.g., WH3_ACHIEVEMENT_TZEENTCH -> TZEENTCH)
                faction = apiname.split('_')[2].title()
                categories[f"🚩 Faction: {faction}"].append(metadata)
            else:
                categories["Other Achievements"].append(metadata)

        html_output += "<style>.ach-card { border: 1px solid #444; border-radius: 5px; padding: 10px; margin: 5px 0; background: #1b2838; color: white; display: flex; align-items: center; justify-content: space-between; } summary { font-size: 1.3em; font-weight: bold; cursor: pointer; padding: 10px; background: #2a475e; color: #66c0f4; border-radius: 5px; margin-top: 10px; }</style>"
            
        for cat_name, items in sorted(categories.items()): 
            html_output += f"<details><summary>{cat_name} ({len(items)})</summary>"   
            # Create a styled HTML card for each achievement
            for meta in items:
                html_output += f"""
                <div class="ach-card">
                    <div>
                        <div style="font-weight: bold; color: #66c0f4;">{meta.get('displayName')}</div>
                        <div style="font-size: 0.9em; color: #acb2b8;">{meta.get('description', '')}</div>
                    </div>
                    <img src="{meta.get('icon')}" style="width: 50px; height: 50px; border-radius: 3px; border: 1px solid #555;">
                </div>"""
            html_output += "</details>"  
        

        output_file = os.path.abspath("achievements.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_output)
        webbrowser.open(f"file://{output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_unlocked_achievements()
