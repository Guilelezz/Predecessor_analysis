import OC
# import obejctivePrio
import pandas as pd

def main():

    saggu_bad = '\ud83c\udfae SAGGUx'  # smile emoji as surrogate pair
    bry_bad = 'Bry\u3006'
    profficiency_bad = "Proficiency \ud83d\udda4"

    # Fix using surrogatepass
    saggu = saggu_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    bry = bry_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    profficiency = profficiency_bad.encode('utf-16', 'surrogatepass').decode('utf-16')

    # df_file = pd.read_excel("excel/Fang Prio.xlsx")
        
    Immune = ["Morose", "ConteEiacula", "ManQ", "Penguin", "Neft"]
    Sin = ["M", "import", "Shynn", "Rei", "TwoHands"]
    Mach10 = ["Bondrewd", "norf", bry, "Bardeldoo" "Lakenator" ]
    Profs = [profficiency, "Creed", "SoulRe4p3r", "Crazzyfool", "SURVIVORTV"]

    # VennyVens = ["Bondrewd", "Ven", "meyer1612", "$ecret", saggu]


    # Roles = ["offlane", "jungle", "midlane", "support", "carry"]

    OC.LAN_team_stats(Profs)
    # OC.LAN_team_stats(Immune)
    # OC.LAN_team_stats(Sin)
    # OC.LAN_team_stats(Mach10)
    
main()