import argparse
import requests
import logging
import time
import sys
import csv
import os


API = "https://api.scryfall.com"
# REMINDER : Here the key is the parameter for the Scryfall API and the value is the name you want for the column where that data will be stored in your csv.
DATA_TO_IMPORT = {
    "colors": "Colors"
}

ACCEPTED_PARAMETERS = [
 'object', 'id', 'oracle_id', 'multiverse_ids', 'mtgo_id', 'mtgo_foil_id', 
 'tcgplayer_id', 'cardmarket_id', 'name', 'lang', 'released_at', 'uri', 
 'scryfall_uri', 'layout', 'highres_image', 'image_status', 'image_uris', 
 'small', 'normal', 'large', 'png', 'art_crop', 'border_crop', 'mana_cost', 
 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 'colors', 
 'color_identity', 'keywords', 'legalities', 'standard', 'future', 
 'historic', 'timeless', 'gladiator', 'pioneer', 'explorer', 'modern', 
 'legacy', 'pauper', 'vintage', 'penny', 'commander', 'oathbreaker', 
 'standardbrawl', 'brawl', 'alchemy', 'paupercommander', 'duel', 'oldschool', 
 'premodern', 'predh', 'games', 'reserved', 'foil', 'nonfoil', 'finishes', 
 'oversized', 'promo', 'reprint', 'variation', 'set_id', 'set', 'set_name', 
 'set_type', 'set_uri', 'set_search_uri', 'scryfall_set_uri', 'rulings_uri', 
 'prints_search_uri', 'collector_number', 'digital', 'rarity', 'card_back_id', 
 'artist', 'artist_ids', 'illustration_id', 'border_color', 'frame', 
 'full_art', 'textless', 'booster', 'story_spotlight', 'edhrec_rank', 
 'penny_rank', 'prices', 'usd', 'usd_foil', 'usd_etched', 'eur', 'eur_foil', 
 'tix', 'related_uris', 'gatherer', 'tcgplayer_infinite_articles', 
 'tcgplayer_infinite_decks', 'edhrec', 'purchase_uris', 'tcgplayer', 
 'cardmarket', 'cardhoarder'
]
for parameter in DATA_TO_IMPORT.keys():
    if parameter not in ACCEPTED_PARAMETERS:
        print(f"Error: {parameter} is not an accepted parameter! Please refer to the accepted parameters list.")
        sys.exit(1)


logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.INFO,  
    datefmt="%H:%M:%S"
)


def verify_csv(arg:str):
    if not arg.endswith(".csv"):
        logging.error("The file must be a csv file!")
        sys.exit(1)

    if not os.path.isfile(arg):
        logging.error(f"{arg} does not exist!")
        sys.exit(1)

    if os.path.getsize(arg) == 0:
        logging.error("the file is empty!")
        sys.exit(1)


def process_card_data(card:dict, data_to_import:dict, verbose:bool):
    if "Scryfall ID" not in card:
        logging.error(f"Card {card['Name']} does not have a Scryfall ID! Skipping...")
        return False

    headers = {
    "User-Agent": "Small script to update my csv file with my collection in it with information. Name of the python file : csv_converter.py",
    "Accept": "application/json"
    }
    if verbose:
        logging.info(f"Reaching {API}/cards/{card['Scryfall ID']} ...")

    retries = 3
    success = False
    for attempt in range(1, retries+1):
        try:
            response = requests.get(f"{API}/cards/{card['Scryfall ID']}", headers=headers, timeout=5)
            response.raise_for_status()
            scryfall_card_info = response.json()
            success = True
            break
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error: {errh} , card : {card['Name']} / Scryfall ID : {card['Scryfall ID']}. Skipping...")
            break
        except requests.exceptions.ConnectionError as errc:
            if attempt < retries:
                if verbose:
                    logging.error(f"Connection Error: {errc} , card : {card['Name']} / Scryfall ID : {card['Scryfall ID']}. Retrying...")
                time.sleep(1 * attempt) # DO NOT REMOVE !! Delay requested by Scryfall, removing it could result in a temporary or permanent ban of your IP.
            elif attempt == retries:
                logging.error(f"Connection Error: {errc} , card : {card['Name']} / Scryfall ID : {card['Scryfall ID']}. Skipping after {retries}...")
        except requests.exceptions.Timeout as errt:
            if attempt < retries:
                if verbose:
                    logging.error(f"Timeout Error: {errt}, card : {card['Name']} / Scryfall ID : {card['Scryfall ID']}. Retrying...")
                time.sleep(1 * attempt) # DO NOT REMOVE !! Delay requested by Scryfall, removing it could result in a temporary or permanent ban of your IP.
            if attempt == retries:
                logging.error(f"Timeout Error: {errt}, card : {card['Name']} / Scryfall ID : {card['Scryfall ID']}. Skipping...")
        except requests.exceptions.RequestException as err:
            logging.error(f"Request Error: {err}, card : {card['Name']} / Scryfall ID : {card['Scryfall ID']}. Skipping...")
            break

    if not success:
        if verbose:
            logging.error(f"Failed to fetch data for {card['Name']}")
        return False

    card_data = scryfall_card_info
    if "card_faces" in scryfall_card_info:  
        card_data = scryfall_card_info["card_faces"][0]
    
    if verbose:
        logging.info(f"Adding the data to '{card['Name']}'.")
    for data in data_to_import.keys():
        card[data_to_import[data]] = scryfall_card_info.get(data, '')

    return True


def main():
    parser = argparse.ArgumentParser(description="Process a csv file from manabox to add card information based on the Scryfall API!")
    parser.add_argument("csv_files", metavar="File", type=str, nargs='+', help="Path to the csv file(s)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()

    for file in args.csv_files:
        if args.verbose:
            logging.info(f"Verifying {file} ...")
        verify_csv(file)
        if args.verbose:
            logging.info("All good!\n")
   
    for file in args.csv_files:
        logging.info(f"Processing {file} ...")
        with open(file, mode='r', newline='') as opened_file:
            reader = csv.DictReader(opened_file)
            column_names = reader.fieldnames
            if "Scryfall ID" not in column_names:
                logging.error("You don't have a 'Scryfall ID' column in your csv file! Exiting.")
                sys.exit(1)
            for data in DATA_TO_IMPORT.values():
                if data not in column_names:
                    if args.verbose:
                        logging.warning(f"'{data}' column not found, adding it.")
                    column_names.append(data)
            if args.verbose:
                print()
            if args.verbose:
                logging.info("Reading and importing rows...\n")
            rows = list(reader)

            if args.verbose:
                print("=============== Fetching Card Data from API ==================\n")
            cards_not_processed = []
            for row in rows:
                success = process_card_data(row, DATA_TO_IMPORT, args.verbose)
                if args.verbose:
                    print()
                if not success:
                    cards_not_processed.append(row["Name"])
                time.sleep(0.075) # DO NOT REMOVE !! Delay requested by Scryfall, removing it could result in a temporary or permanent ban of your IP.
            if args.verbose:
                print("==============================================================\n")

            with open(file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=column_names)
                writer.writeheader()
                for row in rows:
                    for new_column in DATA_TO_IMPORT.values():
                        if new_column not in row:
                            row[new_column] = ''  
                    writer.writerow(row)

        logging.info(f"Done!")
        if len(cards_not_processed) > 0:
            logging.info(f"Counted {len(cards_not_processed)} cards not processed! Here they are :")
            print()
            for card in cards_not_processed:
                print(card)
        print()
        print()


if __name__ == "__main__":
    main()
