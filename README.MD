# 📜 TotalWarTracker

**TotalWarTracker** is a specialized Steam API utility designed for *Total War: Warhammer III* completionists. It streamlines your path to 100% completion by extracting, filtering, and categorizing your remaining achievements into a clean, readable format.

The tool focuses specifically on the "Long Campaign"—automatically stripping away multiplayer achievements and organizing the rest by Faction, Trials, and Victory types.

---
## ✨ Features
*   **Smart Filtering**: Automatically excludes any achievement containing "multiplayer" in the display name or internal API ID.
*   **Dynamic Categorization**: Groups locked achievements into collapsible sections:
    *   🏆 **Victory Achievements**: Campaign wins for specific Legendary Lords.
    *   ⚔️ **Trials of Fate**: Challenges from the Mirror of Madness (PRO10).
    *   🚩 **Racial Factions**: Organized dynamically by race (e.g., Khorne, Kislev, Tzeentch).
*   **High-Quality Metadata**: Maps internal Steam `apiname` to the official Game Schema to retrieve full descriptions and high-resolution icons.
*   **Secure**: Uses environment variables to ensure your Steam API Key and SteamID never leave your local machine.

---
## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone github.com
cd TotalWarTracker
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Configure your credentials
This project uses a .env file for security.
1. Create a file named .env in the root directory.
   - Or copy/rename the example file as from .env.example to .env
2. Add your credentials:
```text
STEAM_API_KEY= [your_api_key_here]
STEAM_USER_ID= [your_64_bit_steam_id_here]
APP_ID - [your_game's_steam_app_id_here]
```
1. Get your API Key: [Steam Community Dev Page](https://steamcommunity.com/dev)
2. Find your SteamID64: Use your [Steam Account Details page](https://store.steampowered.com/account/).
3. Get your Game's App ID via one of these methods:
   1. URL in the Web Browser
        - Look at the URL of the game's store page. The AppID is the series of numbers following /app/. 
        - Format: store.steampowered.com/app/[appid]
        - Example: 
          - Total War: Warhammer III
          - URL: (https://store.steampowered.com/app/1142710/Total_War_WARHAMMER_III
          - AppID: 1142710.
   2. Third-Party
        - If the game has been removed from the store or you cannot find the page, search for the game title on [SteamDB](https://steamdb.info/). The AppID is clearly labeled at the top of the search results and individual game pages. 
    
### 4. Privacy Settings
For the Steam API to access your data, your **Game Details** must be set to **Public** in your Steam Profile Privacy Settings.

---
## 🛠 Usage

Run the script directly from the terminal:
```bash
python Total_War_Tracker.py
```
---
## 📁 Project Structure
- total_war_tracker.py: Main Python logic for API calls and filtering.
- .env: (User-created) Stores your private API keys.
- .gitignore: Pre-configured to ensure your .env is never committed to Git.
- README.md: Project documentation

---
## 🛡 License
Distributed under the MIT License. See LICENSE for more information.

Disclaimer: This tool is a fan project and is not affiliated with Creative Assembly, SEGA, or Games Workshop. All icons and achievement data are property of their respective owners via the Steam Web API.