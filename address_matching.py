import re
from rapidfuzz import fuzz, process
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Ensure the punkt tokenizer and wordnet are downloaded (if not already)
try:
    word_tokenize("test")
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()

filename = "output_data.xlsx"
ignore_terms = ["PO-", "PO", "Marg", "Peeth", "Veedhi", "Rd", "Lane", "NR", "Beside", "Opposite", "OPP", "Behind", "near", "Enclave", "Township", "Society", "Soc", "Towers", "Block", "S/o", "C/o", "D/o", "W/o"]
synonyms = {"St": "Street", "Rd": "Road", "Ave": "Avenue", "Blvd": "Boulevard", "Ln": "Lane"}  # Expand as needed

def normalize_text(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    for term in ignore_terms:
        text = re.sub(r'\b' + re.escape(term) + r'\b', '', text, flags=re.IGNORECASE)
    for abbrev, full_form in synonyms.items():
        text = re.sub(r'\b' + re.escape(abbrev) + r'\b', full_form, text, flags=re.IGNORECASE)
    tokens = word_tokenize(text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    text = ' '.join(lemmatized_tokens)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_similarity(str1, str2):
    if not str1 or not str2:
        return 0.0
    return fuzz.partial_ratio(str1, str2)

def address_matching(input_fields, extracted_address):
    normalized_extracted_address = normalize_text(extracted_address)
    normalized_input_fields = {field: normalize_text(value) for field, value in input_fields.items()}

    input_pincode = input_fields.get('PINCODE', '').replace(' ', '')
    extracted_pincode = re.search(r'\d{6}', extracted_address)
    extracted_pincode = extracted_pincode.group(0) if extracted_pincode else ''
    pincode_score = 100 if input_pincode == extracted_pincode else 0

    field_scores = {}
    weights = {
        'House Flat Number': 1.0,
        'Street Road Name': 1.0,
        'City': 1.0,
        'Floor Number': 0.5,
        'PINCODE': 1.0,
        'Premise Building Name': 0.8,
        'Landmark': 0.5,
        'State': 1.0,
        'Town': 1.0 
    }

    for field, input_value in normalized_input_fields.items():
        if field not in weights:
            print(f"Warning: Field '{field}' not found in weights dictionary. Using default weight of 1.0.")
            weights[field] = 1.0
        if input_value:
             field_scores[field] = round(calculate_similarity(input_value, normalized_extracted_address) * weights[field], 2)
        else:
            field_scores[field] = 0

    included_field_scores = [score for score in field_scores.values() if score >= 70]
    average_score = sum(included_field_scores) / len(included_field_scores) if included_field_scores else 0
    final_match = average_score >= 70 and pincode_score == 100

    return field_scores, average_score, final_match


def process_and_match_addresses(input_file, output_file):
    df = pd.read_excel(input_file)
    selected_columns = df[["SrNo", "House Flat Number", "Street Road Name", "Town", "City", "Floor Number", "Country", "PINCODE", "Premise Building Name", "Landmark", "State", "Address Extracted From OVD"]]
    excel_data = {}
    for index, row in selected_columns.iterrows():
        input_fields_1 = {
            'House Flat Number': str(row['House Flat Number']).strip(),
            'Town': str(row['Town']).strip(),  # include Town
            'Street Road Name': str(row['Street Road Name']).strip(),
            'City': str(row['City']).strip(),
            'Floor Number': str(row['Floor Number']).strip(),
            'PINCODE': str(row['PINCODE']).strip(),
            'Premise Building Name': str(row['Premise Building Name']).strip(),
            'Landmark': str(row['Landmark']).strip(),
            'State': str(row['State']).strip()
        }
        excel_data[row["SrNo"]] = input_fields_1


    # ... (rest of your column creation and saving logic)
    house_flat_number_matches = []
    street_road_name_matches = []
    city_matches = []
    floor_number_matches = []
    pincode_matches = []
    premise_building_name_matches = []
    landmark_matches = []
    state_matches = []
    town_matches = [] #added town matches
    final_address_matches = []
    final_address_match_scores = []


    for sr_no, input_addr in excel_data.items():
        extracted_addr = selected_columns[selected_columns["SrNo"] == sr_no]["Address Extracted From OVD"].values[0]
        if isinstance(extracted_addr, str) and extracted_addr.strip(): # check if address exists and has value
            field_scores_1, average_score_1, final_match_1 = address_matching(input_addr, extracted_addr)
            house_flat_number_matches.append(field_scores_1.get('House Flat Number', 0))
            street_road_name_matches.append(field_scores_1.get('Street Road Name', 0))
            city_matches.append(field_scores_1.get('City', 0))
            floor_number_matches.append(field_scores_1.get('Floor Number', 0))
            pincode_matches.append(field_scores_1.get('PINCODE', 0))
            premise_building_name_matches.append(field_scores_1.get('Premise Building Name', 0))
            landmark_matches.append(field_scores_1.get('Landmark', 0))
            state_matches.append(field_scores_1.get('State', 0))
            town_matches.append(field_scores_1.get('Town', 0)) # added town to the output lists
            final_address_matches.append(final_match_1)
            final_address_match_scores.append(round(average_score_1, 2))
        else: # if extracted address is empty then fill these values with 0
            house_flat_number_matches.append('0')
            street_road_name_matches.append('0')
            city_matches.append('0')
            floor_number_matches.append('0')
            pincode_matches.append('0')
            premise_building_name_matches.append('0')
            landmark_matches.append('0')
            state_matches.append('0')
            town_matches.append('0') # added town to the else condition as well
            final_address_matches.append(False)
            final_address_match_scores.append('0')



    df['House Flat Number Match Score'] = house_flat_number_matches
    df['Street Road Name Match Score'] = street_road_name_matches
    df['City Match Score'] = city_matches
    df['Floor Number Match Score'] = floor_number_matches
    df['PINCODE Match Score'] = pincode_matches
    df['Premise Building Name Match Score'] = premise_building_name_matches
    df['Landmark Match Score'] = landmark_matches
    df['State Match Score'] = state_matches
    df['Town Match Score'] = town_matches #added town to the final output as well
    df['Final Address Match'] = final_address_matches
    df['Final Address Match Score'] = final_address_match_scores

    df.to_excel(output_file, index=False)

    print("Output saved to output_data.xlsx")


# if __name__ == "__main__":
#     process_and_match_addresses("test_data.xlsx", "output_data.xlsx")