<<<<<<< HEAD
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
# df_file = pd.read_excel("excel/Fang Prio.xlsx")

def objectivePrio(df):
    # Convert Yes/No/N/A to 1/0/None
    objective_cols = ['1st Fang', '2nd Fang', '3rd Fang', '1st Orb', '2nd Orb', '1st Tower']
    fang_cols = ['1st Fang', '2nd Fang', '3rd Fang']
    orb_cols = ['1st Orb', '2nd Orb']
    first_fang = ["1st Fang"]
    first_orb = ["1st Orb"]
    tower_cols = ['1st Tower']
    conversion = {'Yes': 1, 'No': 0, 'N/A': None}
    df[objective_cols] = df[objective_cols].replace(conversion)

    # Add Win column
    df['Win'] = df['Game outcome'].apply(lambda x: 1 if x == 'Win' else 0)

    # Extract Enemy Team
    df['Enemy Team'] = df['Games'].apply(lambda x: x.split("vs")[-1].strip())

    # # === 1. Win rate when 3rd Fang is taken ===
    # print("\n=== Win Rate by 3rd Fang ===")
    fang3_data = df[df['3rd Fang'].notnull()]
    # print(fang3_data.groupby('3rd Fang')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'}))

    # # === 2. Correlation between 1st Orb and 1st Tower ===
    # print("\n=== Correlation between 1st Orb and 1st Tower ===")
    correlation = df[['1st Orb', '1st Tower']].corr()
    # print(correlation)

    # # === 3. Objective count and Win correlation ===
    df['Enemy Team'] = df['Games'].apply(lambda x: x.split("vs")[-1].strip() if isinstance(x, str) and "vs" in x else "Unknown")
    # print("\n=== Win Rate by Total Objectives Taken ===")
    # # Ensure all objective-related columns are numeric before aggregation
    df[objective_cols + ['Win']] = df[objective_cols + ['Win']].apply(pd.to_numeric, errors='coerce')

    # # === 4. Enemy team behavior ===
    # print("\n=== Objectives Taken vs Enemy Team ===")
    enemy_agg = df.groupby('Enemy Team')[objective_cols + ['Win']].mean()
    # print(enemy_agg)

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
    df['First Tower % Taken'] = 100*df[tower_cols].sum(axis=1) / df[tower_cols].notna().sum(axis=1)
    df['Obj WR Diff'] = 100*df['Objective % Taken'].sub(df['Win'])

    # Group by enemy team to compute average control and win rate
    team_summary = df.groupby('Enemy Team').agg(
        Games_Played=('Win', 'count'),
        Fang_control=('Fang % Taken', 'mean'),
        Orb_Control=('Orb % Taken', 'mean'),
        First_Tower_Control=('First Tower % Taken', 'mean'),
        Avg_Objective_Control=('Objective % Taken', 'mean'),
        Win_Rate=('Win', 'mean'),
        Obj_WR_Diff=('Obj WR Diff', 'mean')
    ).sort_values('Games_Played', ascending=False)

    # Format nicely
    team_summary['Avg_Objective_Control'] = (team_summary['Avg_Objective_Control'] * 100).round(1)
    team_summary['Win_Rate'] = (team_summary['Win_Rate'] * 100).round(1)

    print(team_summary)


        #4 === First objectives
    print("=== First Fang & Orb taken win rate ===")

    # Filter matches only vs Immune and Sin
    vs_immune_sin = df[df['Enemy Team'].isin(['Immune', 'Sin'])]

    # Filter for rows where both 1st Fang and 1st Orb are defined
    combo_data = vs_immune_sin[
        vs_immune_sin['1st Fang'].notnull() & vs_immune_sin['1st Orb'].notnull()
    ]

    # Group by both 1st Fang and 1st Orb values
    combo_stats = combo_data.groupby(['1st Fang', '1st Orb'])['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})

    # Convert win rate to percentage string
    combo_stats['Win Rate'] = (combo_stats['Win Rate'] * 100).round(2).astype(str) + '%'

    # Print original individual stats (optional)
    print("\n=== Win Rate vs Immune & Sin When Taking 1st Fang ===")
    fang1_data = vs_immune_sin[vs_immune_sin['1st Fang'].notnull()]
    fang1_stats = fang1_data.groupby('1st Fang')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})
    fang1_stats['Win Rate'] = (fang1_stats['Win Rate'] * 100).round(2).astype(str) + '%'
    print(fang1_stats)

    print("\n=== Win Rate vs Immune & Sin When Taking 1st Orb ===")
    orb1_data = vs_immune_sin[vs_immune_sin['1st Orb'].notnull()]
    orb1_stats = orb1_data.groupby('1st Orb')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})
    orb1_stats['Win Rate'] = (orb1_stats['Win Rate'] * 100).round(2).astype(str) + '%'
    print(orb1_stats)

    # Print combined result
    print("\n=== Combined Win Rates Based on 1st Fang and 1st Orb ===")
    print(combo_stats)



    # print(fang1_data.groupby('1st Fang')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'}))
    # print(orb1_data.groupby('1st Orb')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'}))

    # Count total available Fangs per game (exclude N/A)
    # df['Fangs Available'] = df[fang_cols].notna().sum(axis=1)

    # # Count how many Fangs were taken (Yes = 1)
    # df['Fangs Taken'] = df[fang_cols].sum(axis=1)

    # # Count total avaliable Orbs per game (exclude N/A)
    # df['Orbs Avaliable'] = df[orb_cols].notna().sum(axis=1)

    # # Count How many Orbs were taken (Yes = 1)
    # df['Orbs Taken'] = df[orb_cols].sum(axis=1)

    # print("\n=== Correlation Between Objective % Taken and Win Rate per Enemy Team ===")

    # correlation_results = []

    # for team, group in df.groupby('Enemy Team'):
    #     if len(group) >= 2:
    #         corr = group['Objective % Taken'].corr(group['Win'])
    #         correlation_results.append({
    #             'Enemy Team': team,
    #             'Games Played': len(group),
    #             'Correlation': round(corr, 3) if pd.notna(corr) else None
    #         })
    #     else:
    #         correlation_results.append({
    #             'Enemy Team': team,
    #             'Games Played': len(group),
    #             'Correlation': None  # not enough data
    #         })

    # correlation_df = pd.DataFrame(correlation_results)
    # correlation_df = correlation_df.sort_values('Correlation', ascending=False)

    # print(correlation_df.to_string(index=False))



    # # === Optional: Visualizations ===
    # sns.heatmap(correlation, annot=True, cmap="coolwarm")
    # plt.title("Correlation Between Early Objectives")
    # plt.show()

    # print(df)

# objectivePrio(df_file)
=======
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("excel/Fang Prio.xlsx")

# Convert Yes/No/N/A to 1/0/None
objective_cols = ['1st Fang', '2nd Fang', '3rd Fang', '1st Orb', '2nd Orb', '1st Tower']
fang_cols = ['1st Fang', '2nd Fang', '3rd Fang']
orb_cols = ['1st Orb', '2nd Orb']
first_fang = ["1st Fang"]
first_orb = ["1st Orb"]
tower_cols = ['1st Tower']
conversion = {'Yes': 1, 'No': 0, 'N/A': None}
df[objective_cols] = df[objective_cols].replace(conversion)

# Add Win column
df['Win'] = df['Game outcome'].apply(lambda x: 1 if x == 'Win' else 0)

# Extract Enemy Team
df['Enemy Team'] = df['Games'].apply(lambda x: x.split("vs")[-1].strip())

# # === 1. Win rate when 3rd Fang is taken ===
# print("\n=== Win Rate by 3rd Fang ===")
fang3_data = df[df['3rd Fang'].notnull()]
# print(fang3_data.groupby('3rd Fang')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'}))

# # === 2. Correlation between 1st Orb and 1st Tower ===
# print("\n=== Correlation between 1st Orb and 1st Tower ===")
correlation = df[['1st Orb', '1st Tower']].corr()
# print(correlation)

# # === 3. Objective count and Win correlation ===
df['Enemy Team'] = df['Games'].apply(lambda x: x.split("vs")[-1].strip() if isinstance(x, str) and "vs" in x else "Unknown")
# print("\n=== Win Rate by Total Objectives Taken ===")
# # Ensure all objective-related columns are numeric before aggregation
df[objective_cols + ['Win']] = df[objective_cols + ['Win']].apply(pd.to_numeric, errors='coerce')

# # === 4. Enemy team behavior ===
# print("\n=== Objectives Taken vs Enemy Team ===")
enemy_agg = df.groupby('Enemy Team')[objective_cols + ['Win']].mean()
# print(enemy_agg)

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
df['First Tower % Taken'] = 100*df[tower_cols].sum(axis=1) / df[tower_cols].notna().sum(axis=1)
df['Obj WR Diff'] = 100*df['Objective % Taken'].sub(df['Win'])

# Group by enemy team to compute average control and win rate
team_summary = df.groupby('Enemy Team').agg(
    Games_Played=('Win', 'count'),
    Fang_control=('Fang % Taken', 'mean'),
    Orb_Control=('Orb % Taken', 'mean'),
    First_Tower_Control=('First Tower % Taken', 'mean'),
    Avg_Objective_Control=('Objective % Taken', 'mean'),
    Win_Rate=('Win', 'mean'),
    Obj_WR_Diff=('Obj WR Diff', 'mean')
).sort_values('Games_Played', ascending=False)

# Format nicely
team_summary['Avg_Objective_Control'] = (team_summary['Avg_Objective_Control'] * 100).round(1)
team_summary['Win_Rate'] = (team_summary['Win_Rate'] * 100).round(1)

print(team_summary)


    #4 === First objectives
print("=== First Fang & Orb taken win rate ===")

vs_immune_sin = df[df['Enemy Team'].isin(['Immune', 'Sin'])]

fang1_data = vs_immune_sin[vs_immune_sin['1st Fang'].notnull()]
orb1_data = vs_immune_sin[vs_immune_sin['1st Orb'].notnull()]

# Calculate win stats
fang1_stats = fang1_data.groupby('1st Fang')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})
orb1_stats = orb1_data.groupby('1st Orb')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'})

# Convert win rate to percentage
fang1_stats['Win Rate'] = (fang1_stats['Win Rate'] * 100).round(2).astype(str) + '%'
orb1_stats['Win Rate'] = (orb1_stats['Win Rate'] * 100).round(2).astype(str) + '%'

# Print
print("\n=== Win Rate vs Immune & Sin When Taking 1st Fang ===")
print(fang1_stats)

print("\n=== Win Rate vs Immune & Sin When Taking 1st Orb ===")
print(orb1_stats)


# print(fang1_data.groupby('1st Fang')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'}))
# print(orb1_data.groupby('1st Orb')['Win'].agg(['count', 'sum', 'mean']).rename(columns={'mean': 'Win Rate'}))

# Count total available Fangs per game (exclude N/A)
# df['Fangs Available'] = df[fang_cols].notna().sum(axis=1)

# # Count how many Fangs were taken (Yes = 1)
# df['Fangs Taken'] = df[fang_cols].sum(axis=1)

# # Count total avaliable Orbs per game (exclude N/A)
# df['Orbs Avaliable'] = df[orb_cols].notna().sum(axis=1)

# # Count How many Orbs were taken (Yes = 1)
# df['Orbs Taken'] = df[orb_cols].sum(axis=1)

# print("\n=== Correlation Between Objective % Taken and Win Rate per Enemy Team ===")

# correlation_results = []

# for team, group in df.groupby('Enemy Team'):
#     if len(group) >= 2:
#         corr = group['Objective % Taken'].corr(group['Win'])
#         correlation_results.append({
#             'Enemy Team': team,
#             'Games Played': len(group),
#             'Correlation': round(corr, 3) if pd.notna(corr) else None
#         })
#     else:
#         correlation_results.append({
#             'Enemy Team': team,
#             'Games Played': len(group),
#             'Correlation': None  # not enough data
#         })

# correlation_df = pd.DataFrame(correlation_results)
# correlation_df = correlation_df.sort_values('Correlation', ascending=False)

# print(correlation_df.to_string(index=False))



# # === Optional: Visualizations ===
# sns.heatmap(correlation, annot=True, cmap="coolwarm")
# plt.title("Correlation Between Early Objectives")
# plt.show()

# print(df)
>>>>>>> bbf4ce703a2e1b88c427dbd3904061a0ecbe1c7a
