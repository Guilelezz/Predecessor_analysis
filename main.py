import OC
# import obejctivePrio
import pandas as pd

def main():

    saggu_bad = '\ud83c\udfae SAGGUx'  # smile emoji as surrogate pair

    # Fix using surrogatepass
    saggu = saggu_bad.encode('utf-16', 'surrogatepass').decode('utf-16')

    # df_file = pd.read_excel("excel/Fang Prio.xlsx")
        
    Immune = ["Morose", "ConteEiacula", "ManQ", "Penguin", "Neft"]
    Sin = ["M", "import", "Shynn", "Rei", "TwoHands"]

    VennyVens = ["Bondrewd", "Ven", "meyer1612", "$ecret", saggu]
    RnR = ["Dreckiger Dan", "Proper Clean", "kimbo", "SloneZZ", "Ezpzmaglll"]
    Obscure = ["ACM", "Ragnarok", "onfof", "SSScie", "Night"]

    Roles = ["offlane", "jungle", "midlane", "support", "carry"]

    EnemiesVen = ["import", "Neft"]
    EnemiesImmune = ["import", "Ven", "Toasty", "xehe", ]
    EnemiesSin = ["Neft", "Ven", "xehe"]

    OC.LAN_team_stats(Immune)

    # OC.team_gold_by_role(Immune,Roles,EnemiesImmune)
    # OC.team_gold_leads(Immune,Roles,EnemiesImmune)

    # OC.team_gold_by_role(Sin,Roles,EnemiesSin)
    # OC.team_gold_leads_tf(Sin,Roles,EnemiesSin)
    # OC.team_gold_leads(Sin, Roles, EnemiesSin)

    # OC.Fangbooth_stats(Obscure)
    # obejctivePrio.objectivePrio(df_file)

    # for player in Obscure:
        # print(player + str(": ") +str(OC.get_player_hero_stats(player)))
    
main()