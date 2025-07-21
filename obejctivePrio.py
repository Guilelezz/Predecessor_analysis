import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def BigBoy(df):
    # Convert Yes/No/N/A to 1/0/None
    objective_cols = ['1st Fang', '2nd Fang', '3rd Fang', '1st Orb', '2nd Orb']
    fang_cols = ['1st Fang', '2nd Fang', '3rd Fang']
    orb_cols = ['1st Orb', '2nd Orb']
    first_fang = ['1st Fang']
    first_orb = ['1st Orb']
    conversion = {'Yes': 1, 'No': 0, 'N/A': None}
    df[objective_cols] = df[objective_cols].replace(conversion)

    # Extract Enemy Team
    df['Enemy Team'] = df['Games']

    print("\n=== Objective Control % and Win Rate vs Each Enemy Team ===")

    # Count total available objectives per game (exclude N/A)
    df['Objectives Available'] = df[objective_cols].notna().sum(axis=1)

    # Count how many objectives were taken (Yes = 1)
    df['Objectives Taken'] = df[objective_cols].sum(axis=1)

    # Count total available Fangs per game (exclude N/A)
    df['Fangs Available'] = df[fang_cols].notna().sum(axis=1)

    # Count how many Fangs were taken (Yes = 1)
    df['Fangs Taken'] = df[fang_cols].sum(axis=1)

    # Count total avaliable Orbs per game (exclude N/A)
    df['Orbs Avaliable'] = df[orb_cols].notna().sum(axis=1)

    # Count How many Orbs were taken (Yes = 1)
    df['Orbs Taken'] = df[orb_cols].sum(axis=1)


    # Calculate percentage of objectives taken
    df['Objective % Taken'] = df['Objectives Taken'] / df['Objectives Available']
    df['Fang % Taken'] = 100*df['Fangs Taken'] / df['Fangs Available']
    df['Orb % Taken'] = 100*df['Orbs Taken'] / df['Orbs Avaliable']
    df['Obj WR Diff'] = 100*df['Objective % Taken'].sub(df['Game outcome'])

    # Group by enemy team to compute average control and win rate
    team_summary = df.groupby('Enemy Team').agg(
        Games_Played=('Game outcome', 'count'),
        Fang_control=('Fang % Taken', 'mean'),
        Orb_Control=('Orb % Taken', 'mean'),
        Avg_Objective_Control=('Objective % Taken', 'mean'),
        Win_Rate=('Game outcome', 'mean'),
        Obj_WR_Diff=('Obj WR Diff', 'mean')
    ).sort_values('Games_Played', ascending=False)

    # Format nicely
    team_summary['Avg_Objective_Control'] = (team_summary['Avg_Objective_Control'] * 100).round(1)
    team_summary['Win_Rate'] = (team_summary['Win_Rate'] * 100).round(1)

    print(team_summary)


    #4 ======= First objectives ==============

    # ==== This can be used if you are only interested in looking at specific teams ======
    # vs_immune_sin = df[df['Enemy Team'].isin(['Immune', 'Sin'])]

    # fang1_data = vs_immune_sin[vs_immune_sin['1st Fang'].notnull()]
    # orb1_data = vs_immune_sin[vs_immune_sin['1st Orb'].notnull()]


    # Calculate win stats
    fang1_stats = df.groupby('1st Fang')['Game outcome'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})
    orb1_stats = df.groupby('1st Orb')['Game outcome'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})

    # Convert win rate to percentage
    fang1_stats['Win Rate'] = (fang1_stats['Win Rate'] * 100).round(2).astype(str) + '%'
    orb1_stats['Win Rate'] = (orb1_stats['Win Rate'] * 100).round(2).astype(str) + '%'

    # Print
    print("\n=== Win Rate vs When Taking 1st Fang ===")
    print(fang1_stats)

    print("\n=== Win Rate vs When Taking 1st Orb ===")
    print(orb1_stats)


    # ========= Combine Fang and prime stats ========

    # Group by both 1st Fang and 1st Orb values
    combo_stats = df.groupby(['1st Fang', '1st Orb'])['Game outcome'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})

    # Convert win rate to percentage string
    combo_stats['Win Rate'] = (combo_stats['Win Rate'] * 100).round(2).astype(str) + '%'

    # Print combined result
    print("\n=== Combined Win Rates Based on 1st Fang and 1st Orb ===")
    print(combo_stats)


# When I fuck around
df = pd.read_excel("excel/Immune_early_obj.xlsx")
BigBoy(df)