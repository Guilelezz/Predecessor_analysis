import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Return playerId from player name
def get_player_id(playerName):
    url = "https://omeda.city/players.json?filter[name]="+str(playerName)
    response = requests.get(url)
    try:
        return response.json()[0]['id']
    except:
        print("Could not find:" +str(playerName))
        return "404"

def get_player_name(playerId):
    response = requests.get("https://omeda.city/players/"+str(playerId)+str(".json"))
    try:
        return response.json()["display_name"]
    except:
        print("Could not find player with ID "+str(playerId))
        return "404"

#Returns stats for specific heroes
def get_hero_stats(hero):
    response = requests.get("https://omeda.city/dashboard/hero_statistics.json")

    heroes = response.json()['hero_statistics']

    for i in range( len(heroes)):
        if heroes[i]['display_name'] == hero:
            print(heroes[i])
            break

def get_list_of_hero_ids():
    response = requests.get("https://omeda.city/dashboard/hero_statistics.json")

    heroes = response.json()['hero_statistics']
    overview = {}

    for hero in heroes:
        overview[hero['hero_id']] = hero['display_name']

    return overview

#Returns Json of basic player info such as rank and MMR
def get_player_basic(playerName):
    playerId = get_player_id(playerName)

    url = "https://omeda.city/players/" +str(playerId) +str(".json")
    response = requests.get(url)
    player = response.json()

    wantedStats = [ "region", "leaderboard_rank", "rank_title", "vp_total"]
    temp = [0]*len(wantedStats)

    for i in player:
        for j in range(len(wantedStats)):
            if i == wantedStats[j]:
                    temp[j] = player[wantedStats[j]]

    return {
        "region": temp[0],
        "leaderboard": temp[1],
        "rank": temp[2],
        "VP": temp[3]
    }

#Not used
def get_player_info(playerName):
    playerId = get_player_id(playerName)

    url = "https://omeda.city/players/" +str(playerId) +str("/matches.json")
    response = requests.get(url)
    player = response.json()

    with open('playerInfo.json','w') as f:
        json.dump(player,f)

#Returns basic overall stats
def get_player_stats(playerName):
    playerId = get_player_id(playerName)

    url = "https://omeda.city/players/"+str(playerId)+str("/statistics.json")
    response = requests.get(url)
    player = response.json()


    wantedStats = ["matches_played","avg_kda","avg_kdar","favorite_role","winrate"]
    temp = [0]*len(wantedStats)

    for i in player:
        for j in range(len(wantedStats)):
            if i == wantedStats[j]:
                    temp[j] = player[wantedStats[j]]

    return {
        "matches_played": temp[0],
        "avg_kda": temp[1],
        "avg_kdar": temp[2],
        "favorite_role": temp[3],
        "winrate": temp[4]
    }

#Returns list of most played heroes
def get_player_hero_stats(playerName):
    playerId = get_player_id(playerName)
    
    url = "https://omeda.city/players/"+str(playerId)+str("/hero_statistics.json?time_frame=1M")
    response = requests.get(url)
    try:
        player = response.json()["hero_statistics"]
    except:
        return 1
    return most_played(player)

def get_player_hero_stats_custom(playerName):
    playerId = get_player_id(playerName)
    
    url = "https://omeda.city/players/"+str(playerId)+str("/hero_statistics.json?filter[game_mode]=custom&time_frame=1M&filter[game_mode]=custom&per_page=100")
    response = requests.get(url)
    try:
        player = response.json()["hero_statistics"]
    except:
        return 1
    return most_played(player)

#Helper function for get_player_hero_stats to find most played heroes
def most_played(player):
    matchcount = []
    displayname = []

    for i in range(len(player)):
        matchcount.append(player[i]["match_count"])
        displayname.append(player[i]["display_name"])

    k = [0]*5
    l = 0

    hold = [0]*5

    for j in range (5):
        for i in range(len(matchcount)):
            if matchcount[i] > k[j]:
                k[j] = matchcount[i]
                l = i
        hold[j] = displayname[l]
        matchcount.pop(l)
        displayname.pop(l)
    
    return {"Favorite heroes": hold }

#Returns a json of basic player stats, including, rank, overall stats, and hero stats
def get_data(PlayerName):
    
    return {
        #"Basic_info": get_player_basic(PlayerName),
        #"Player_stats": get_player_stats(PlayerName),
        #"Hero stats": get_player_hero_stats(PlayerName,5)
        "Custom games": get_player_matches_custom(PlayerName)
    } 

#Creates Json of the stats of an entire team, with the first in list being team name and 
#And all following being player names
def get_team_stats(teams):
    for team in teams:
        f = open(str(team[0])+str(".json"),'w')
        print(team[0]+str("\n"))
        json_dump = {}
        for k in range(len(team)-1):
            print(team[k+1])
            json_dump[team[k+1]] = get_data(team[k+1])
        f.write(json.dumps(json_dump,indent=4))
        f.close()
        print("\n")

#Returns json of matches in time frame, such as 1M, 3M or ALL
def get_player_matches(PlayerName, TimeFrame):
    PlayerId = get_player_id(PlayerName)
    
    response = requests.get("https://omeda.city/players/"+str(PlayerId)+str("/matches.json?filter[game_mode]=custom&time_frame="+str(TimeFrame)))
    matches = response.json()

    return matches

#Returns json of custom matches played with 1 month
def get_player_matches_custom(PlayerName):
    PlayerId = get_player_id(PlayerName)

    response = requests.get("https://omeda.city/players/"+str(PlayerId)+str("/matches.json?filter[game_mode]=custom&time_frame=1M&filter[game_mode]=custom&per_page=100"))
    
    matches = response.json()

    return matches

#Returns json of matches where 2 players are facing each other in time frame such as 1M, 3M or ALL
def get_player_matches_enemy(PlayerName, Enemy, TimeFrame):
    PlayerId = get_player_id(PlayerName)

    response = requests.get("https://omeda.city/players/"+str(PlayerId)+str("/matches.json?filter[game_mode]=custom&time_frame=")+str(TimeFrame)+str("&filter[player_name]=")+str(Enemy)+str("&per_page=100"))
    matches = response.json()

    return matches

#Takes key and value, and returns json
def return_json(key, value):
    json_dump = {}
    if (len(key) != len(value)):
        print("Key and value are not same size")
        return 1
    
    for i in range(len(key)):
        json_dump[key[i]] = value[i]

    return json_dump

#Returns Json of wantedstats from a json of stats
def extract_stats(stats, wantedStats):
    value = [0]*len(wantedStats)

    for stat in stats:
         for i in range(len(wantedStats)):
             if stat == wantedStats[i]:
                 value[i] = stats[wantedStats[i]]

    return return_json(wantedStats,value)

#Compares 2 players, in a given time frame, such as 1M, 3M or ALL
def compare_players(Player1, Player2, TimeFrame):
    matches = get_player_matches_enemy(Player1, Player2, TimeFrame)["matches"]
    numberOfGames = len(matches)

    wantedStats = ["display_name","hero_id","role","minions_killed","kills","deaths","assists","total_damage_dealt_to_heroes","gold_earned","performance_score"]

    enemies = []
    teammates = []

    for i in range(numberOfGames):
        team1 = "none"
        team2 = "none"
        for j in range(10):
            if matches[i]["players"][j]["display_name"] == Player1:
                team1 = matches[i]["players"][j]["team"]
            if matches[i]["players"][j]["display_name"] == Player2:
                team2 = matches[i]["players"][j]["team"]
        if team1 != team2 and team2 != "none":
            enemies.append(i)
        else:
            teammates.append(i)

    Player1Stats = [0]*len(enemies)
    Player2Stats = [0]*len(enemies)

    for i in range(len(enemies)):
        for j in range(10):
            if matches[enemies[i]]["players"][j]["display_name"] == Player2:
                Player2Stats[i] = extract_stats(matches[enemies[i]]["players"][j],wantedStats)
            if matches[enemies[i]]["players"][j]["display_name"] == Player1:
                Player1Stats[i] = extract_stats(matches[enemies[i]]["players"][j],wantedStats)

    return Player1Stats,Player2Stats

#Helper function for ComparePlayers, returns 2 jsons of wantedstats averages.
def Head2Head(stats):
    wantedStats = ["minions_killed","kills","deaths","assists","total_damage_dealt_to_heroes","gold_earned","performance_score"]

    numberStats = [[0]*len(stats[0]) for i in range(len(stats))]

    for i in range(len(stats)):
        for j in range(len(stats[i])):
            numberStats[i][j] = extract_stats(stats[i][j],wantedStats)

    Averages = [[0]*len(wantedStats) for i in range(len(stats))]
    for i in range(len(stats)):
        for j in range(len(stats[i])):
            count = 0
            for k in numberStats[i][j]:
                Averages[i][count] += numberStats[i][j][k]
                count += 1

    for i in range(len(Averages)):
        for j in range(len(Averages[i])):
            Averages[i][j] /= len(stats[i]) 

    return return_json(wantedStats,Averages[0]), return_json(wantedStats,Averages[1])

def customgames_data_extractor(Team):

    team_players = [Team[0], Team[1], Team[2],Team[3],Team[4]]

    # Initialize the team stats dictionary
    wteam_stats = {}
    lteam_stats = {}

    for target_player in team_players:
        data = get_data(target_player)

        wtotal_kills = wtotal_deaths = wtotal_assists = 0
        wtotal_damage_to_heroes = wtotal_gold = 0
        ltotal_kills = ltotal_deaths = ltotal_assists = 0
        ltotal_damage_to_heroes = ltotal_gold = 0
        games_won = games_lost = wgame_length = lgame_length = 0
        winning_team = ""

        for match in data["Custom games"]["matches"]:
            winning_team = match["winning_team"]
            duration = match["game_duration"]
            for player in match["players"]:
                if player["display_name"] == target_player:
                    if winning_team == player["team"]:
                        wgame_length += duration
                        games_won += 1
                        wtotal_kills += player["kills"]
                        wtotal_deaths += player["deaths"]
                        wtotal_assists += player["assists"]
                        wtotal_damage_to_heroes += player["total_damage_dealt_to_heroes"]
                        wtotal_gold += player["gold_earned"]  
                    else:
                        lgame_length += duration
                        games_lost += 1
                        ltotal_kills += player["kills"]
                        ltotal_deaths += player["deaths"]
                        ltotal_assists += player["assists"]
                        ltotal_damage_to_heroes += player["total_damage_dealt_to_heroes"]
                        ltotal_gold += player["gold_earned"] 

        if games_won > 0:
            wavg_data = {
                "kda": round((wtotal_kills + wtotal_assists) / wtotal_deaths, 2),
                "average_damage_to_heroes": round((wtotal_damage_to_heroes / games_won) / (wgame_length/(60*games_won)), 2),
                "average_gold_earned": round((wtotal_gold / games_won) / (wgame_length/(60*games_won)), 2)
            }
            wteam_stats[target_player] = wavg_data
        else:
            wteam_stats[target_player] = {"error": "No games found"}

        if games_lost > 0:
            lavg_data = {
                "kda": round((ltotal_kills + ltotal_assists) / ltotal_deaths, 2),
                "average_damage_to_heroes": round((ltotal_damage_to_heroes / games_lost) / (lgame_length/(60*games_lost)), 2),
                "average_gold_earned": round((ltotal_gold / games_lost) / (lgame_length/(60*games_lost)), 2)
            }
            lteam_stats[target_player] = lavg_data
        else:
            lteam_stats[target_player] = {"error": "No games found"}

    filename = f"temp_files/wteam_stats.json"
    with open(filename, "w") as outfile:
        json.dump(wteam_stats, outfile, indent=4)

    filename = f"temp_files/lteam_stats.json"
    with open(filename, "w") as outfile:
        json.dump(lteam_stats, outfile, indent=4)

    return wteam_stats, lteam_stats

def plot_team_stats(team_data, wteam_data,lteam_data):
    # === Extract player names and stat values ===
    players = list(wteam_data.keys())

    kda_values = [team_data[player]["kda"] for player in players]
    damage_values = [team_data[player]["average_damage_to_heroes"] for player in players]
    gold_values = [team_data[player]["average_gold_earned"] for player in players]
    kp_values = [team_data[player]["Kill participation"] for player in players]

    wkda_values = [wteam_data[player]["kda"] for player in players]
    wdamage_values = [wteam_data[player]["average_damage_to_heroes"] for player in players]
    wgold_values = [wteam_data[player]["average_gold_earned"] for player in players]
    wkp_values = [wteam_data[player]["Kill participation"] for player in players]

    lkda_values = [lteam_data[player]["kda"] for player in players]
    ldamage_values = [lteam_data[player]["average_damage_to_heroes"] for player in players]
    lgold_values = [lteam_data[player]["average_gold_earned"] for player in players]
    lkp_values = [lteam_data[player]["Kill participation"] for player in players]

    # === Generate the plots ===
    plot_stat(kda_values, wkda_values, lkda_values, "KDA per Player", "KDA", players)
    plot_stat(damage_values, wdamage_values, ldamage_values, "Average Damage to Heroes per minute", "Damage", players)
    plot_stat(gold_values, wgold_values, lgold_values, "Average Gold Earned per minute", "Gold", players)
    plot_stat(kp_values, wkp_values, lkp_values, "Kill Participation per Player", "Kill Participation (%)", players)

def plot_stat(values, wvalues, lvalues, title, ylabel, players):
    if not (len(players) == len(wvalues) == len(lvalues)):
        raise ValueError("All input lists must have the same length.")
    
    x = np.arange(len(players))*1.5  # numeric positions for each player
    bar_width = 0.4

    plt.figure(figsize=(10, 6))

    # Plot overall game (middle?)
    bars = wbars = plt.bar(x , values, width=bar_width, color="#295bc7", edgecolor='black', label='All games')

    # Plot wins (shift left)
    wbars = plt.bar(x - bar_width, wvalues, width=bar_width, color='#90ee90', edgecolor='black', label='Wins')

    # Plot losses (shift right)
    lbars = plt.bar(x + bar_width, lvalues, width=bar_width, color='#f08080', edgecolor='black', label='Losses')

    # Titles and labels
    plt.title(title, fontsize=16)
    plt.xlabel("Players", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(x, players, rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

    # Add value labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

    for bar in wbars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

    for bar in lbars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()

def Fangbooth_stats(Team):
    data = customgames_data_extractor(Team)
    
    plot_team_stats(data[0],data[1])

def get_gold(playerName: str, role:str , enemies: str = None):
    data = get_data(playerName)
    print("name = "+str(playerName)+str(" role = ")+str(role))
    winning_team  = ""
    player1 = []
    player2 = []

    gold = {}

    games = wins = 0

    # print("My enemies are:"+str(enemies) +str("\n"))

    for match in data["Custom games"]["matches"]:
        gold5 = gold10 = gold15 = gold20 = goldEnd = 0
        win = True
        enemyexist = CorrectRole = False
        games += 1
        winning_team = match["winning_team"] 

        if enemies is not None:
            for player in match["players"]:
                for enemy in enemies:
                    # print("Looking for enemy: "+str(enemy) +str(" And current player is: "+str(player)))
                    if enemy == player["display_name"]:
                        # print("Found correct enemy:" +str(enemy))
                        enemyexist = True
                        break            
        else:
            enemyexist = True

        for player in match["players"]:
            # print(player["role"])
            # print(player["display_name"])
            if player["role"] == role:
                if player["display_name"] == playerName:
                    CorrectRole = True
                    if player["team"] == winning_team:
                        wins += 1
                        win = True
                    else:
                        win = False
                    player1 = player["gold_earned_at_interval"]
                else:
                    player2 = player["gold_earned_at_interval"]

        if enemyexist and CorrectRole :
            player1 = np.trim_zeros(player1)
            player2 = np.trim_zeros(player2)
            
            goldEnd = player1[len(player1)-1] - player2[len(player2)-1]

            if len(player1) > 5:
                gold5 = player1[5] - player2[5]
            else:
                gold15 = goldEnd
            if len(player1) > 10:
                gold10 = player1[10] - player2[10]
            else:
                gold15 = goldEnd
            if len(player1) > 15:
                gold15 = player1[15] - player2[15]
            else:
                gold15 = goldEnd
            if len(player1) > 20:
                gold20  = player1[20] - player2[20]
            else:
                gold20 = goldEnd

            gold[games] = [gold5,gold10,gold15,gold20,goldEnd,win]
        else:
            games -= 1
            if win:
                wins -= 1
            

    return gold
    
#Gold leads that end up in wins
def team_gold_by_role(Team, role, enemy = None):
    player_list = {}

    for i in range(len(Team)):
        if enemy is not None:
            player_list[Team[i]] = get_gold(Team[i],role[i], enemy)
        else:
            player_list[Team[i]] = get_gold(Team[i],role[i])


    games = [0]*len(Team)
    lead5 = [0]*len(Team)
    lead10 = [0]*len(Team)
    lead15 = [0]*len(Team)
    lead20 = [0]*len(Team)
    leadEnd = [0]*len(Team)
    wins = [0]*len(Team)

    for k in range(len(Team)):
        games[k] = len(player_list[Team[k]])
        for i in range(len(player_list[Team[k]])):
            if player_list[Team[k]][i+1][0] > 0 and player_list[Team[k]][i+1][5]:
                lead5[k] += 1
            if player_list[Team[k]][i+1][1] > 0 and player_list[Team[k]][i+1][5]:
                lead10[k] += 1
            if player_list[Team[k]][i+1][2] > 0 and player_list[Team[k]][i+1][5]:
                lead15[k] += 1
            if player_list[Team[k]][i+1][3] > 0 and player_list[Team[k]][i+1][5]:
                lead20[k] += 1
            if player_list[Team[k]][i+1][4] > 0 and player_list[Team[k]][i+1][5]:
                leadEnd[k] += 1
            if player_list[Team[k]][i+1][5]:
                wins[k] += 1
            
        print("Player: " +str(Team[k])+str(", played: ")+str(games[k])+str(", wins: ")+str(wins[k]))
        print("win % when lead at 5: " +str(100*lead5[k]/games[k]))
        print("win % when lead at 10: " +str(100*lead10[k]/games[k]))
        print("win % when lead at 15: " +str(100*lead15[k]/games[k]))
        print("win % when lead at 20: " +str(100*lead20[k]/games[k]))
        print("win % when lead at End: " +str(100*leadEnd[k]/games[k]))
        print("\n")

#Gold leads throughout certain points of a game
def team_gold_leads_tf(Team, role, enemy = None):
    player_list = {}
    print("team = " +str(Team) +str(" role = ") +str(role))
    for i in range(len(Team)):
        if enemy is not None:
            player_list[Team[i]] = get_gold(Team[i], role[i], enemy)
        else:
            player_list[Team[i]] = get_gold(Team[i], role[i])


    # print(player_list)

    games = [0]*len(Team)
    lead5 = [0]*len(Team)
    lead10 = [0]*len(Team)
    lead15 = [0]*len(Team)
    lead20 = [0]*len(Team)
    leadEnd = [0]*len(Team)
    wins = [0]*len(Team)

    for k in range(len(Team)):
        games[k] = len(player_list[Team[k]])
        for i in range(len(player_list[Team[k]])):
            if player_list[Team[k]][i+1][0] > 0 :
                lead5[k] += 1
            if player_list[Team[k]][i+1][1] > 0 :
                lead10[k] += 1
            if player_list[Team[k]][i+1][2] > 0 :
                lead15[k] += 1
            if player_list[Team[k]][i+1][3] > 0 :
                lead20[k] += 1
            if player_list[Team[k]][i+1][4] > 0:
                leadEnd[k] += 1
            if player_list[Team[k]][i+1][5]:
                wins[k] += 1
            
        print("Player: " +str(Team[k])+str(", played: ")+str(games[k])+str(", wins: ")+str(wins[k]))
        print("Lead at 5: " +str(100*lead5[k]/games[k]))
        print("Lead at 10: " +str(100*lead10[k]/games[k]))
        print("Lead at 15: " +str(100*lead15[k]/games[k]))
        print("Lead at 20: " +str(100*lead20[k]/games[k]))
        print("Lead at End: " +str(100*leadEnd[k]/games[k]))
        print("\n")

#Gold leads throughout certain points of a game
def team_gold_leads(Team, role, enemy = None):
    player_list = {}
    print("team = " +str(Team) +str(" role = ") +str(role))
    for i in range(len(Team)):
        if enemy is not None:
            player_list[Team[i]] = get_gold(Team[i], role[i], enemy)
        else:
            player_list[Team[i]] = get_gold(Team[i], role[i])


    # print(player_list)

    games = [0]*len(Team)
    lead5 = [0]*len(Team)
    lead10 = [0]*len(Team)
    lead15 = [0]*len(Team)
    lead20 = [0]*len(Team)
    leadEnd = [0]*len(Team)
    wins = [0]*len(Team)

    for k in range(len(Team)):
        games[k] = len(player_list[Team[k]])
        for i in range(len(player_list[Team[k]])):
            # if player_list[Team[k]][i+1][0] > 0 :
            lead5[k] += player_list[Team[k]][i+1][0]
            lead10[k] += player_list[Team[k]][i+1][1]
            lead15[k] += player_list[Team[k]][i+1][2]
            lead20[k] += player_list[Team[k]][i+1][3]
            leadEnd[k] += player_list[Team[k]][i+1][4]
            if player_list[Team[k]][i+1][5]:
                wins[k] += 1
            
        print("Player: " +str(Team[k])+str(", played: ")+str(games[k])+str(", wins: ")+str(wins[k]))
        print("Lead at 5: " +str(lead5[k]/games[k]))
        print("Lead at 10: " +str(lead10[k]/games[k]))
        print("Lead at 15: " +str(lead15[k]/games[k]))
        print("Lead at 20: " +str(lead20[k]/games[k]))
        print("Lead at End: " +str(leadEnd[k]/games[k]))
        print("\n")

def LAN_team_stats(Team):
    team_players = [Team[0], Team[1], Team[2],Team[3],Team[4]]

    # Initialize the team stats dictionary
    wteam_stats = {}
    lteam_stats = {}
    team_stats = {}
    hero_stats = {}
    wr_hero_stats = {}

    for target_player in team_players:
        data = get_data(target_player)

        wtotal_kills = wtotal_deaths = wtotal_assists = wteam_total_kills = 0
        wtotal_damage_to_heroes = wtotal_gold = 0
        ltotal_kills = ltotal_deaths = ltotal_assists = lteam_total_kills = 0
        ltotal_damage_to_heroes = ltotal_gold = 0
        games = games_won = games_lost = wgame_length = lgame_length = 0

        winning_team = ""
        hero = [0]*75
        wr_hero = [0]*75

        for match in data["Custom games"]["matches"]:
            winning_team = match["winning_team"]
            dusk_kills = dawn_kills = 0
            duration = match["game_duration"]
            player_team = "none"
            for player in match["players"]:

                if player["team"] == "dusk":
                    dusk_kills += player["kills"]
                    # print("Dusk kills: " +str(dusk_kills))
                else:
                    dawn_kills += player["kills"]
                    # print("Dawn kills: " +str(dawn_kills))

                if player["display_name"] == target_player:
                    # print("Found target player: " +str(target_player))
                    games += 1
                    if player["hero_id"] > 75:
                        hero_id = 74
                    else:
                        hero_id = player["hero_id"]
                    hero[hero_id] += 1

                    if winning_team == player["team"]:
                        # print("Player is on winning team")
                        player_team = player["team"]

                        wr_hero[hero_id] += 1
                        wgame_length += duration
                        games_won += 1
                        wtotal_kills += player["kills"]
                        wtotal_deaths += player["deaths"]
                        wtotal_assists += player["assists"]
                        wtotal_damage_to_heroes += player["total_damage_dealt_to_heroes"]
                        wtotal_gold += player["gold_earned"]  
                    else:
                        # print("Player is on losing team")
                        player_team = player["team"]

                        lgame_length += duration
                        games_lost += 1
                        ltotal_kills += player["kills"]
                        ltotal_deaths += player["deaths"]
                        ltotal_assists += player["assists"]
                        ltotal_damage_to_heroes += player["total_damage_dealt_to_heroes"]
                        ltotal_gold += player["gold_earned"] 
                # print("Player: " +str(target_player) +str(" Team: ")+str(player_team) +str(" Winning team: ")+str(winning_team))

            if player_team == winning_team:
                # print("Player team: " +str(player_team) +str(" Winning team: ")+str(winning_team))
                if winning_team == "dusk":
                    wteam_total_kills += dusk_kills
                else:
                    wteam_total_kills += dawn_kills
                # print("Winning team total kills: " +str(wteam_total_kills))
            elif player_team != "none":
                # print("Player team: " +str(player_team) +str(" Winning team: ")+str(winning_team))
                if player_team == "dawn":
                    lteam_total_kills += dawn_kills
                else:
                    lteam_total_kills += dusk_kills
                # print("Losing team total kills: " +str(lteam_total_kills))
            
            # print("Player: " +str(target_player) +str(" Current Kill participation: ")+str((100*(wtotal_kills + ltotal_kills + wtotal_assists + ltotal_assists)) / (wteam_total_kills + lteam_total_kills)))



        if games_won + games_lost > 0:
            avg_data = {
                "games": games,
                "win_rate" : (100*games_won)/games,
                "kda": round((wtotal_kills + ltotal_kills + wtotal_assists + ltotal_deaths) / (wtotal_deaths + ltotal_deaths), 2),
                "average_damage_to_heroes": round(((wtotal_damage_to_heroes + ltotal_damage_to_heroes) / games) / ((wgame_length + lgame_length)/(60*games)), 2),
                "average_gold_earned": round(((wtotal_gold + ltotal_gold) / games) / ((wgame_length+lgame_length)/(60*games)), 2),
                "Kill participation": round((100*(wtotal_kills + ltotal_kills + wtotal_assists + ltotal_assists)) / (wteam_total_kills + lteam_total_kills), 2)
            }
            team_stats[target_player] = avg_data
        else:
            team_stats[target_player] = {"error": "No games found"}

        if games_won > 0:
            wavg_data = {
                "wins": games_won,
                "kda": round((wtotal_kills + wtotal_assists) / wtotal_deaths, 2),
                "average_damage_to_heroes": round((wtotal_damage_to_heroes / games_won) / (wgame_length/(60*games_won)), 2),
                "average_gold_earned": round((wtotal_gold / games_won) / (wgame_length/(60*games_won)), 2),
                "Kill participation": round((100*(wtotal_kills + wtotal_assists)) / (wteam_total_kills), 2)
            }
            wteam_stats[target_player] = wavg_data
        else:
            wteam_stats[target_player] = {"error": "No wins found"}

        if games_lost > 0:
            lavg_data = {
                "losses": games_lost,
                "kda": round((ltotal_kills + ltotal_assists) / ltotal_deaths, 2),
                "average_damage_to_heroes": round((ltotal_damage_to_heroes / games_lost) / (lgame_length/(60*games_lost)), 2),
                "average_gold_earned": round((ltotal_gold / games_lost) / (lgame_length/(60*games_lost)), 2),
                "Kill participation": round((100*(ltotal_kills + ltotal_assists)) / (lteam_total_kills), 2)
            }
            lteam_stats[target_player] = lavg_data
        else:
            lteam_stats[target_player] = {"error": "No losses found"}

        #Note down most played heroes by number indency
        hero_stats[target_player] = hero
        wr_hero_stats[target_player] = wr_hero

    hero_list = get_list_of_hero_ids()
    most_played_heroes = {}

    for player in hero_stats:
        top_n = 5

        # Sort by value descending, keeping index
        sorted_indices = sorted(enumerate(hero_stats[player]), key=lambda x: x[1], reverse=True)

        # Extract the top N indices
        largest_indices = [index for index, value in sorted_indices[:top_n]]

        # if hero_list[largest_indices[0]] == 74:
        #     hero_list[largest_indices[0]] = 10000000001

        if player not in most_played_heroes:
            most_played_heroes[player] = {}

        for i in range(len(largest_indices)):
            key = largest_indices[i]
            if largest_indices[i] == 74:
                key = 10000000001
            most_played_heroes[player][hero_list[key]] = [hero_stats[player][largest_indices[i]]]
            win_rate_by_hero = (100*wr_hero_stats[player][largest_indices[i]])/hero_stats[player][largest_indices[i]]
            # most_played_heroes[player][hero_list[key]] = (100*wr_hero_stats[player][largest_indices])/hero_stats[player][largest_indices[i]] 
            most_played_heroes[player][hero_list[key]].append(win_rate_by_hero)

    # filename = f"temp_files/team_stats.json"
    # with open(filename, "w") as outfile:
    #     json.dump(team_stats, outfile, indent=4)

    # filename = f"temp_files/wteam_stats.json"
    # with open(filename, "w") as outfile:
    #     json.dump(wteam_stats, outfile, indent=4)

    # filename = f"temp_files/lteam_stats.json"
    # with open(filename, "w") as outfile:
    #     json.dump(lteam_stats, outfile, indent=4)

    combined_data = {
        "team_stats": team_stats,
        "wins_team_stats": wteam_stats,
        "losses_team_stats": lteam_stats,
        "most_played_heroes": most_played_heroes
    }
    filename = f"temp_files/combined_team_stats.json"
    with open(filename, "w") as outfile:
        json.dump(combined_data, outfile, indent=4)

    LAN_to_excel()

    plot_team_stats(team_stats,wteam_stats,lteam_stats)

def LAN_to_excel():
    # Load the JSON data
    with open("temp_files/combined_team_stats.json", "r") as f:
        data = json.load(f)

    # Extract and flatten main team stats
    team_stats_df = pd.DataFrame(data["team_stats"]).T.reset_index()
    team_stats_df.rename(columns={
        "index": "Player",
        "games": "Games",
        "win_rate": "Win Rate (%)",
        "kda": "KDA",
        "average_damage_to_heroes": "Avg. Damage to Heroes",
        "average_gold_earned": "Avg. Gold Earned",
        "Kill participation": "Kill Participation (%)"
    }, inplace=True)

    # Reorder columns and round values
    team_stats_df = team_stats_df[
        ["Player", "Games", "Win Rate (%)", "KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]
    ]
    team_stats_df[["Win Rate (%)", "KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]] = \
        team_stats_df[["Win Rate (%)", "KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]].round(2)

    # Copy to clipboard for team stats
    team_stats_df.to_clipboard(index=False)
    print("✅ Formatted team stats copied to clipboard. You can now paste directly into Excel.")

    input("Press Enter to continue to Heroes stats...")

    # --- HEROES STATS FORMATTING ---
    all_heroes_rows = []
    for player, hero_dict in data["most_played_heroes"].items():
        hero_names = list(hero_dict.keys())
        picks = [hero_dict[h][0] for h in hero_names]
        winrates = [round(hero_dict[h][1], 2) for h in hero_names]

        # Build the 3 rows for this player
        row_player = [player] + hero_names
        row_picks = ["Picks"] + picks
        row_winrate = ["Win Rate (%)"] + winrates

        # Add to the list
        all_heroes_rows.append(row_player)
        all_heroes_rows.append(row_picks)
        all_heroes_rows.append(row_winrate)

    # Convert to DataFrame for clipboard
    heroes_df = pd.DataFrame(all_heroes_rows)
    heroes_df.to_clipboard(index=False, header=False)
    print("✅ Formatted heroes stats copied to clipboard. You can now paste directly into Excel.")

    input("Press Enter to continue to WIN stats...")

    # === WINS TEAM STATS ===
    wins_stats_df = pd.DataFrame(data["wins_team_stats"]).T.reset_index()
    wins_stats_df.rename(columns={
        "index": "Player",
        "wins": "Wins",
        "kda": "KDA",
        "average_damage_to_heroes": "Avg. Damage to Heroes",
        "average_gold_earned": "Avg. Gold Earned",
        "Kill participation": "Kill Participation (%)"
    }, inplace=True)
    wins_stats_df = wins_stats_df[
        ["Player", "Wins", "KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]
    ]
    wins_stats_df[["KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]] = \
        wins_stats_df[["KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]].round(2)
    wins_stats_df.to_clipboard(index=False)
    print("✅ Formatted wins stats copied to clipboard. You can now paste directly into Excel.")
    input("Press Enter to continue to LOSS stats...")

    # === LOSSES TEAM STATS ===
    losses_stats_df = pd.DataFrame(data["losses_team_stats"]).T.reset_index()
    losses_stats_df.rename(columns={
        "index": "Player",
        "losses": "Losses",
        "kda": "KDA",
        "average_damage_to_heroes": "Avg. Damage to Heroes",
        "average_gold_earned": "Avg. Gold Earned",
        "Kill participation": "Kill Participation (%)"
    }, inplace=True)
    losses_stats_df = losses_stats_df[
        ["Player", "Losses", "KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]
    ]
    losses_stats_df[["KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]] = \
        losses_stats_df[["KDA", "Avg. Damage to Heroes", "Avg. Gold Earned", "Kill Participation (%)"]].round(2)
    losses_stats_df.to_clipboard(index=False)
    print("✅ Formatted losses stats copied to clipboard. You can now paste directly into Excel.")
    input("Press Enter to finish...")

def get_all_items():
    response = requests.get("https://omeda.city/items.json")
    fuckyou = response.json()
    return fuckyou

def find_item_values():
    data = get_all_items()

    item_list = {}

    #Value of 1 stat - Basic values
    stat_values = {
        "physical_power": 350/8,
        "magical_power": 350/12,
        "physical_penetration": 200/4,
        "magical_penetration": 180/5,
        "critical_chance": 450/10,
        "attack_speed": 350/10,
        "lifesteal": 143.75/5,
        "magical_lifesteal": 170.83/5,
        "omnivamp": 325/4,
        "physical_armor": 350/10,
        "magical_armor": 350/10,
        "tenacity": 200/15,
        "max_health": 350/100,
        "max_mana": 350/150,
        "health_regeneration": 350/40,
        "mana_regeneration": 350/50,
        "heal_shield_increase": 216.67/5,
        "ability_haste": 350/5,
        "movement_speed": 200
    }

    #  #   Value of 1 stat - Values only from basic components so no lifesteal and so on
    # stat_values = {
    #     "physical_power": 350/8,
    #     "magical_power": 350/12,
    #     "physical_penetration": 0,
    #     "magical_penetration": 0,
    #     "critical_chance": 450/10,
    #     "attack_speed": 350/10,
    #     "lifesteal": 0,
    #     "magical_lifesteal": 0,
    #     "omnivamp": 0,
    #     "physical_armor": 350/10,
    #     "magical_armor": 350/10,
    #     "tenacity": 0,
    #     "max_health": 350/100,
    #     "max_mana": 350/150,
    #     "health_regeneration": 350/40,
    #     "mana_regeneration": 350/50,
    #     "heal_shield_increase": 0,
    #     "ability_haste": 350/5,
    #     "movement_speed": 0
    # }
    for item in data:
        if item["slot_type"] == "Trinket" or  item["slot_type"] == "Active" or  item["slot_type"] == "Crest":
            pass
        else:
            theoretical_value = 0
            for stat in item["stats"]:
                for value in stat_values:
                    if stat == value:
                        theoretical_value += stat_values[stat] * item["stats"][stat]
            item_list[item["display_name"]] = {
                "Price": item["total_price"],
                "Value": theoretical_value,
                "Difference": theoretical_value - item["total_price"]
            }
    return item_list

# find_item_values()

# data = find_item_values()

# filename = f"temp_files/item_values.json"
# with open(filename, "w") as outfile:
#     json.dump(data, outfile, indent=4)

# Immune = ["Morose", "ConteEiacula", "ManQ", "Penguin", "Neft"]
# LAN_team_stats(Immune)

# Team = ["Bondrewd", "Ven", ]
# Role = ["offlane", "jungle"]
# Team = ["Brandonite"]
# Role = ["midlane"]
# # Enemy = ["import","Neft"]
# # team_gold_leads(Team,Role,Enemy)
# team_gold_by_role(Team,Role)
        

data = get_data("Bondrewd")
i = 0
for match in data["Custom games"]["matches"]:
    winning_team = match["winning_team"]
    for player in match["players"]:
        if player["display_name"] == "Bondrewd":
            if winning_team == player["team"]:
                i += 1
data = get_player_matches_custom("Bondrewd")
filename = f"temp_files/test.json"
with open(filename, "w") as outfile:
    json.dump(data, outfile, indent=4)