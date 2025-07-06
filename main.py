import OC

def main():

    saggu_bad = '\ud83c\udfae SAGGUx'  # smile emoji as surrogate pair

    # Fix using surrogatepass
    saggu = saggu_bad.encode('utf-16', 'surrogatepass').decode('utf-16')

        
    Immune = ["Morose", "ConteEiacula", "ManQ", "Penguin", "Neft"]
    Sin = ["M", "import", "Brandonite", "Shynn", "TwoHands"]
    VennyVens = ["Bondrewd", "Ven", "meyer1612", "$ecret", saggu]
    RnR = ["Dreckiger Dan", "Proper Clean", "kimbo", "SloneZZ", "Ezpzmaglll"]
    Obscure = ["ACM", "Ragnarok", "onfof", "SSScie", "Night"]

    Roles = ["offlane", "jungle", "midlane", "support", "carry"]

    Enemies = ["import", "Neft"]

    # OC.team_gold_by_role(VennyVens,Roles,Enemies)
    OC.team_gold_leads(VennyVens,Roles,Enemies)
    # OC.Fangbooth_stats(Obscure)

    # for player in Obscure:
    #     print(player + str(": ") +str(OC.get_player_hero_stats(player)))
main()