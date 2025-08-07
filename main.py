import OC
# import obejctivePrio
import pandas as pd

# df_file = pd.read_excel("excel/Fang Prio.xlsx")

def main():

    saggu_bad = '\ud83c\udfae SAGGUx'  # smile emoji as surrogate pair
    bry_bad = 'Bry\u3006'
    profficiency_bad = "Proficiency \ud83d\udda4"
    smegatron_bad = "Smegatron\ud83e\udd16"
    peeck_bad = "\u01a5\u025b\u025b\u03c2\u049b"
    Maguli_bad = "\u028d\u0105\u0262\u028a\u029f\u0131"
    MrGooRoo_bad = "MrG\u00f6\u00f6R\u00f6\u00f6"

    # Fix using surrogatepass
    saggu = saggu_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    bry = bry_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    profficiency = profficiency_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    smegatron = smegatron_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    peeck = peeck_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    Maguli = Maguli_bad.encode('utf-16', 'surrogatepass').decode('utf-16')
    MrGooRoo = MrGooRoo_bad.encode('utf-16', 'surrogatepass').decode('utf-16')

    Flowstate = ["bkbgrnrjefek", "Mercyy", "simba", peeck, Maguli]
    Hive = [MrGooRoo, "Nugzlit", "Aho", "Shwimmityy", "KevKaioken"]
    Immune = ["Morose", "ConteEiacula", "ManQ", "Penguin", "Neft"]
    Mach10 = ["Bondrewd", "norf", bry, "Bardeldoo", "Lakenator" ]
    MTG = ["Nitro", "KingKofi", "PinzoDunzo", smegatron, "Chicken"]
    Mythic = ["TekkenKid12", "gratty", "Appie", "Toasty", "Cure"]
    # Primal = ["Sneakz", "Mav", "Sei", "xehe", "CoLdskis"] #Primal with CoLdskis
    Primal = ["Sneakz", "Mav", "Sei", "xehe", "Knapz"] #Primal with Knapz
    Profs = [profficiency, "Creed", "SoulRe4p3r", "Crazzyfool", "SURVIVORTV"]
    Sin = ["M", "import", "Shynn", "Rei", "TwoHands"]
    Rogue = ["STSButters", "Warpz", "Phox", "Wangle", "Haru"]

    # VennyVens = ["Bondrewd", "Ven", "meyer1612", "$ecret", saggu]

    # Roles = ["offlane", "jungle", "midlane", "support", "carry"]

    # OC.LAN_team_stats(Flowstate)
    # OC.LAN_team_stats(Hive)
    # OC.LAN_team_stats(Immune)
    OC.LAN_team_stats(Mach10)
    # OC.LAN_team_stats(MTG)
    # OC.LAN_team_stats(Mythic)
    # OC.LAN_team_stats(Primal)
    # OC.LAN_team_stats(Profs)
    # OC.LAN_team_stats(Rogue)
    # OC.LAN_team_stats(Sin)
    
main()