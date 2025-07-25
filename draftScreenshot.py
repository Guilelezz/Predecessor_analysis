import cv2
import pytesseract
import os
import imagehash
from PIL import Image
from difflib import get_close_matches
from pprint import pprint
from collections import defaultdict
import csv
import numpy as np

# Set path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

standard_size = (64, 64)  # Standard image size for hero matching
TEAM_LIST = ["TI", "Immune", "SIN", "Primal", "Mythic"]  # List of known team names

def get_combined_hash(image):
    return (
        imagehash.phash(image),
        imagehash.average_hash(image),
        imagehash.dhash(image)
    )

def hash_distance(hash_tuple1, hash_tuple2):
    return sum(h1 - h2 for h1, h2 in zip(hash_tuple1, hash_tuple2))

def preprocess_text_crop(crop):
    # Convert PIL image to grayscale OpenCV format
    gray = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    # Convert back to PIL image
    return Image.fromarray(thresh)


def load_hero_library(path='hero_library'):
    library = {}
    for file in os.listdir(path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            hero_name = os.path.splitext(file)[0]
            img = Image.open(os.path.join(path, file)).convert('RGB').resize(standard_size)
            library[hero_name] = get_combined_hash(img)
    return library

def identify_hero(cropped_img, hero_hashes, confidence_threshold=70):
    cropped_img = cropped_img.resize(standard_size)
    cropped_hash = get_combined_hash(cropped_img)
    best_match = None
    min_dist = float('inf')

    for hero_name, h_hash in hero_hashes.items():
        dist = hash_distance(cropped_hash, h_hash)
        if dist < min_dist:
            min_dist = dist
            best_match = hero_name

    # print(f"Matched {best_match} with distance {min_dist}")
    return best_match if min_dist <= confidence_threshold else "XXXXXXXXXXX"


def define_draft_regions():
    left_x, right_x = 415, 1490
    custom_y_offsets = [220, 300, 405, 505, 595, 700, 805, 900]
    box_w, box_h = 72, 72

    def make_boxes_custom(x_center, y_offsets):
        return [
            (x_center - box_w//2, y,
            x_center + box_w//2, y + box_h)
            for y in y_offsets
        ]

    left_boxes = make_boxes_custom(left_x,custom_y_offsets)
    right_boxes = make_boxes_custom(right_x,custom_y_offsets)

    left_draft = {
        "bans": [left_boxes[i] for i in [0, 1, 5]],
        "picks": [left_boxes[i] for i in [2, 3, 4, 6, 7]]
    }

    right_draft = {
        "bans": [right_boxes[i] for i in [0, 1, 5]],
        "picks": [right_boxes[i] for i in [2, 3, 4, 6, 7]]
    }

    return left_draft, right_draft

def match_team_name(raw_name):
    matches = get_close_matches(raw_name, TEAM_LIST, n=1, cutoff=0.3)
    return matches[0] if matches else raw_name

def get_team_names_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    coords = {
        "left": (340, 160, 500, 200),
        "right": (1400, 160, 1520, 200)
    }

    names = {}
    for side, (x1, y1, x2, y2) in coords.items():
        cropped = image[y1:y2, x1:x2]
        pil_crop = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
        processed = preprocess_text_crop(pil_crop)
        text = pytesseract.image_to_string(processed, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz').strip()
        # print(f"OCR raw result for {side}: '{text}'") 
        matched_name = match_team_name(text)
        if len(matched_name) < 1:
            matched_name = "Unknown"
        if matched_name == "TI": #Fuck you Primal
            matched_name = "Immune"
        # print(f"Matched team name: {matched_name}") 
        names[side] = matched_name

    return names["left"], names["right"]

def parse_draft(image_path, hero_library_path='hero_library'):
    image = cv2.imread(image_path)
    left_name, right_name = get_team_names_from_image(image)
    hero_hashes = load_hero_library(hero_library_path)
    left_draft_coords, right_draft_coords = define_draft_regions()

    draft = {}

    for team_name, team_coords in zip([left_name, right_name], [left_draft_coords, right_draft_coords]):
        draft[team_name] = {"bans": [], "picks": []}
        for role in ["bans", "picks"]:
            for (x1, y1, x2, y2) in team_coords[role]:
                crop = image[y1:y2, x1:x2]
                pil_crop = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                hero = identify_hero(pil_crop, hero_hashes)
                draft[team_name][role].append(hero)
    
    filename = os.path.basename(image_path).lower()
    draft["Win"] = "_win" in filename

    return draft

def parse_draft_folder(folder_path, hero_library_path='hero_library'):
    drafts = []
    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, file)
            print(f"\nProcessing {file}...")
            draft = parse_draft(image_path, hero_library_path)
            drafts.append((file, draft))
    return drafts

def parse_all_draft_folders(base_folder, hero_library_folder):
    all_results = []

    for root, dirs, files in os.walk(base_folder):
        if not dirs:  # Only process folders containing files
            folder_results = parse_draft_folder(root, hero_library_folder)
            all_results.extend(folder_results)

    return all_results

def visualize_draft_regions(image_path):
    image = cv2.imread(image_path)
    
    # Team name boxes
    coords = {
        "left": (340, 160, 500, 200),
        "right": (1400, 160, 1550, 200)
    }

    # Draw team name boxes
    for label, (x1, y1, x2, y2) in coords.items():
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Draft hero boxes
    immune_coords, sin_coords = define_draft_regions()
    color_map = {'bans': (0, 0, 255), 'picks': (0, 255, 0)}

    for team_coords in [immune_coords, sin_coords]:
        for role in ['bans', 'picks']:
            for i, (x1, y1, x2, y2) in enumerate(team_coords[role]):
                cv2.rectangle(image, (x1, y1), (x2, y2), color_map[role], 2)
                cv2.putText(image, role[0].upper() + str(i + 1), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[role], 1)

    # Show the image
    cv2.imshow("Draft Region Debug", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Analyzes parsed draft data to compute hero stats per team and overall
from collections import defaultdict

def analyze_drafts(draft_results):
    # Stats containers
    stats = {
        "Immune": defaultdict(lambda: {"picked": 0, "banned": 0, "wins": 0, "losses": 0}),
        "Opponent": defaultdict(lambda: {"picked": 0, "banned": 0, "wins": 0, "losses": 0}),
        "Overall": defaultdict(lambda: {"picked": 0, "banned": 0, "presence": 0.0})
    }

    total_games = len(draft_results)

    for filename, draft in draft_results:
        win = draft.get("Win", False)
        team_names = [name for name in draft if name != "Win"]

        # Identify opponent name
        opponent = [team for team in team_names if team != "Immune"]
        if not opponent:
            continue  # Skip if no valid opponent
        opponent = opponent[0]

        # Track heroes picked or banned this game for presence calculation
        heroes_seen = set()

        for team in team_names:
            role = "Immune" if team == "Immune" else "Opponent"
            is_win = win if team == "Immune" else not win

            for hero in draft[team]["picks"]:
                stats[role][hero]["picked"] += 1
                stats[role][hero]["wins" if is_win else "losses"] += 1
                stats["Overall"][hero]["picked"] += 1
                heroes_seen.add(hero)

            for hero in draft[team]["bans"]:
                stats[role][hero]["banned"] += 1
                stats["Overall"][hero]["banned"] += 1
                heroes_seen.add(hero)

        # Update presence only once per hero per game (pick or ban)
        for hero in heroes_seen:
            stats["Overall"][hero]["presence"] += 1

    # Finalize presence as percentage and compute winrate
    for team in ["Immune", "Opponent"]:
        for hero, values in stats[team].items():
            total_games_played = values["wins"] + values["losses"]
            winrate = (values["wins"] / total_games_played) * 100 if total_games_played > 0 else 0.0
            values["winrate"] = round(winrate, 2)
            # Remove losses and reorder fields
            del values["losses"]

    for hero, values in stats["Overall"].items():
        if total_games > 0:
            values["presence"] = round((values["presence"] / total_games) * 100, 2)

    return stats

def analyze_first_three_picks(draft_results):
    stats = defaultdict(lambda: {"picked": 0, "presence": 0, "wins": 0, "losses": 0})
    total_games = len(draft_results)

    for filename, draft in draft_results:
        win = draft.get("Win", False)
        if "Immune" not in draft:
            continue

        first_three_picks = draft["Immune"]["picks"][:3]
        seen_in_this_game = set()

        for hero in first_three_picks:
            stats[hero]["picked"] += 1
            stats[hero]["wins" if win else "losses"] += 1
            seen_in_this_game.add(hero)

        for hero in seen_in_this_game:
            stats[hero]["presence"] += 1

    # Compute winrate and cleanup
    for hero, values in stats.items():
        total_games_played = values["wins"] + values["losses"]
        winrate = (values["wins"] / total_games_played) * 100 if total_games_played > 0 else 0.0
        values["winrate"] = round(winrate, 2)
        del values["losses"]

        # Reorder to Picks, Presence, Winrate, Wins
        reordered = {
            "picked": values["picked"],
            "presence": round((values["presence"] / total_games) * 100, 2) if total_games > 0 else 0.0,
            "winrate": values["winrate"],
            "wins": values["wins"]
        }
        stats[hero] = reordered

    return stats

def export_stats_to_csv(stats, filename):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Hero", "Picked", "Banned", "Winrate", "Wins", "Presence", "Team"])

        for team in ["Immune", "Opponent"]:
            for hero, data in stats[team].items():
                writer.writerow([
                    hero,
                    data.get("picked", 0),
                    data.get("banned", 0),
                    data.get("winrate", 0.0),
                    data.get("wins", 0),
                    "",
                    team
                ])

        for hero, data in stats["Overall"].items():
            writer.writerow([
                hero,
                data.get("picked", 0),
                data.get("banned", 0),
                "",
                "",
                data.get("presence", 0.0),
                "Overall"
            ])

def export_first_three_stats_to_csv(stats, filename):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Hero", "Picked", "Presence", "Winrate", "Wins"])
        for hero, data in stats.items():
            writer.writerow([
                hero,
                data.get("picked", 0),
                data.get("presence", 0.0),
                data.get("winrate", 0.0),
                data.get("wins", 0)
            ])

# Example usage:

results = parse_all_draft_folders('drafts', 'hero_library')
stats = analyze_drafts(results)
early_picks_stats = analyze_first_three_picks(results)

export_stats_to_csv(stats, "stats/full_stats.csv")
export_first_three_stats_to_csv(early_picks_stats, "stats/early_picks_stats.csv")

# def draftRecognition(draft_folder):
#     results = parse_draft_folder(draft_folder, "hero_library")
#     from pprint import pprint
#     pprint(results)

#     # visualize_draft_regions("drafts/Mythic/1907_1_win.PNG")
#     return results

# draftRecognition("drafts/Primal")



