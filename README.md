# Predecessor_analysis
Tools for analyzing Predecessor games

**Shit created by Guileless to analyse pred games.**

## Current functions that exist
### OC.py 
*Generally these functions gather data from Omeda.city through their API and formats it and gathers more specific pieces of information faster.*
**Fangboot_stats**
  Gathers the data from a team and the individual players custom games played for the last month, up to 100 games. Then finds the average amount of kills/deaths/assists pr. game, gold pr. game and total damage to heroes, while keeping it seperated in wins and losses. And afterwards plots the data.
** team_gold_by_role **\n
  Takes the input of a Team, their roles in the same order, eg. *Team=["Guileless", "Ven"]* *Role=["offlane", "jungle"]*, and then takes enemy as an optional argument, if the enemy argument is given, it will only look at matches where that player / list of players are present, on either team. The function will then look at your gold at a certain point in the game, and compare it to the other person in that game with the same role. This will then return the percentage of times the individual player on the team wins, when they have a gold lead at different points throughout the game.
**team_gold_leads**
  Like *team_gold_by_role* this function compares the gold between the targeted player and their opposing role, and gives in a percentage how often the targeted player is ahead in gold at certain points throughout the game.

  ### objectivePrio.py
  **This script uses a local excel spreadsheet, which contains manually gathered information about which team got which objectve, and then attempts to find trends**
  *Currently no functions exist in here*
