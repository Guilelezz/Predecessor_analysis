<<<<<<< HEAD
import requests
import json
import matplotlib.pyplot as plt
import numpy as np

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
    
    url = "https://omeda.city/players/"+str(playerId)+str("/hero_statistics.json?time_frame=3M")
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

    filename = f"wteam_stats.json"
    with open(filename, "w") as outfile:
        json.dump(wteam_stats, outfile, indent=4)

    filename = f"lteam_stats.json"
    with open(filename, "w") as outfile:
        json.dump(lteam_stats, outfile, indent=4)

    return wteam_stats, lteam_stats

def plot_team_stats(wteam_data,lteam_data):
    # === Extract player names and stat values ===
    players = list(wteam_data.keys())
    wkda_values = [wteam_data[player]["kda"] for player in players]
    wdamage_values = [wteam_data[player]["average_damage_to_heroes"] for player in players]
    wgold_values = [wteam_data[player]["average_gold_earned"] for player in players]

    lkda_values = [lteam_data[player]["kda"] for player in players]
    ldamage_values = [lteam_data[player]["average_damage_to_heroes"] for player in players]
    lgold_values = [lteam_data[player]["average_gold_earned"] for player in players]

    # === Generate the plots ===
    plot_stat(wkda_values, lkda_values, "KDA per Player", "KDA", players)
    plot_stat(wdamage_values, ldamage_values, "Average Damage to Heroes per minute", "Damage", players)
    plot_stat(wgold_values, lgold_values, "Average Gold Earned per minute", "Gold", players)

def plot_stat(wvalues, lvalues, title, ylabel, players):
    if not (len(players) == len(wvalues) == len(lvalues)):
        raise ValueError("All input lists must have the same length.")
    
    x = np.arange(len(players))  # numeric positions for each player
    bar_width = 0.4

    plt.figure(figsize=(10, 6))

    # Plot wins (shift left)
    wbars = plt.bar(x - bar_width/2, wvalues, width=bar_width, color='#90ee90', edgecolor='black', label='Wins')

    # Plot losses (shift right)
    lbars = plt.bar(x + bar_width/2, lvalues, width=bar_width, color='#f08080', edgecolor='black', label='Losses')

    # Titles and labels
    plt.title(title, fontsize=16)
    plt.xlabel("Players", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(x, players, rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

    # Add value labels
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


# Team = ["Bondrewd", "Ven", ]
# Role = ["offlane", "jungle"]
# Team = ["Brandonite"]
# Role = ["midlane"]
# # Enemy = ["import","Neft"]
# # team_gold_leads(Team,Role,Enemy)
# team_gold_by_role(Team,Role)
        



# data = get_data("Ven")
# i = 0
# for match in data["Custom games"]["matches"]:
#     winning_team = match["winning_team"]
#     for player in match["players"]:
#         if player["display_name"] == "Ven":
#             if winning_team == player["team"]:
#                 i += 1
# data = get_player_matches_custom("Ven")
# filename = f"test.json"
# with open(filename, "w") as outfile:
#     json.dump(data, outfile, indent=4)
=======
import requests
import json
import matplotlib.pyplot as plt
import numpy as np

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
    
    url = "https://omeda.city/players/"+str(playerId)+str("/hero_statistics.json?time_frame=3M")
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

    filename = f"wteam_stats.json"
    with open(filename, "w") as outfile:
        json.dump(wteam_stats, outfile, indent=4)

    filename = f"lteam_stats.json"
    with open(filename, "w") as outfile:
        json.dump(lteam_stats, outfile, indent=4)

    return wteam_stats, lteam_stats

def plot_team_stats(wteam_data,lteam_data):
    # === Extract player names and stat values ===
    players = list(wteam_data.keys())
    wkda_values = [wteam_data[player]["kda"] for player in players]
    wdamage_values = [wteam_data[player]["average_damage_to_heroes"] for player in players]
    wgold_values = [wteam_data[player]["average_gold_earned"] for player in players]

    lkda_values = [lteam_data[player]["kda"] for player in players]
    ldamage_values = [lteam_data[player]["average_damage_to_heroes"] for player in players]
    lgold_values = [lteam_data[player]["average_gold_earned"] for player in players]

    # === Generate the plots ===
    plot_stat(wkda_values, lkda_values, "KDA per Player", "KDA", players)
    plot_stat(wdamage_values, ldamage_values, "Average Damage to Heroes per minute", "Damage", players)
    plot_stat(wgold_values, lgold_values, "Average Gold Earned per minute", "Gold", players)

def plot_stat(wvalues, lvalues, title, ylabel, players):
    if not (len(players) == len(wvalues) == len(lvalues)):
        raise ValueError("All input lists must have the same length.")
    
    x = np.arange(len(players))  # numeric positions for each player
    bar_width = 0.4

    plt.figure(figsize=(10, 6))

    # Plot wins (shift left)
    wbars = plt.bar(x - bar_width/2, wvalues, width=bar_width, color='#90ee90', edgecolor='black', label='Wins')

    # Plot losses (shift right)
    lbars = plt.bar(x + bar_width/2, lvalues, width=bar_width, color='#f08080', edgecolor='black', label='Losses')

    # Titles and labels
    plt.title(title, fontsize=16)
    plt.xlabel("Players", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(x, players, rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()

    # Add value labels
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

def get_gold(playerName, role, enemies = None):
    data = get_data(playerName)

    winning_team  = ""
    player1 = []
    player2 = []

    gold = {}

    games = wins = 0

    print("My enemies are:"+str(enemies) +str("\n"))

    for match in data["Custom games"]["matches"]:
        gold5 = gold10 = gold15 = gold20 = goldEnd = 0
        win = True
        enemyexist = False
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
            print(" no enemy")
            enemyexist = True

        for player in match["players"]:
            if player["role"] == role:
                if player["display_name"] == playerName:
                    if player["team"] == winning_team:
                        wins += 1
                        win = True
                    else:
                        win = False
                    player1 = player["gold_earned_at_interval"]
                else:
                    player2 = player["gold_earned_at_interval"]

        if enemyexist:
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
def team_gold_leads(Team, role, enemy = None):
    player_list = {}

    for i in range(len(Team)):
        if enemy is not None:
            player_list[Team[i]] = get_gold(Team[i], role[i], enemy)
        else:
            player_list[Team[i]] = get_gold(Team[i], role[i])


    print(player_list)

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


# Team = ["Bondrewd", "Ven", ]
# Role = ["offlane", "jungle"]
# Team = ["meyer1612"]
# Role = ["midlane"]
# Enemy = ["import","Neft"]
# team_gold_leads(Team,Role,Enemy)
# team_gold_by_role(Team,Role)
        



# data = get_data("Ven")
# i = 0
# for match in data["Custom games"]["matches"]:
#     winning_team = match["winning_team"]
#     for player in match["players"]:
#         if player["display_name"] == "Ven":
#             if winning_team == player["team"]:
#                 i += 1
# data = get_player_matches_custom("Ven")
# filename = f"test.json"
# with open(filename, "w") as outfile:
#     json.dump(data, outfile, indent=4)
>>>>>>> bbf4ce703a2e1b88c427dbd3904061a0ecbe1c7a
