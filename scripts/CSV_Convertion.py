import pandas as pd
import json

def is_nan(value):
    return value.lower() == 'nan'

def csv_to_json(input_csv, output_json):
    # Read CSV file into a DataFrame with semicolon as the delimiter
    df = pd.read_csv(input_csv, delimiter=';')

    # Create a nested dictionary for the JSON structure
    json_data = {
        "name": "DEMAND",
        "children": []
    }

    # Iterate through unique topics in the DataFrame
    for topic in df['Topic'].unique():
        topic_data = {
            "name": f"{str(topic)}",
            "children": []
        }

        # Filter rows for the current topic
        topic_rows = df[df['Topic'] == topic]

        # Create a dictionary to keep track of Word entries and their corresponding data
        word_dict = {}

        # Iterate through rows for the current topic
        for _, row in topic_rows.iterrows():
            word = row['Word']

            # Identify the last non-blank column for the current row (excluding "Weight")
            last_non_blank_column = row.iloc[2:-1].last_valid_index()
            last_non_blank_column_name = str(row[last_non_blank_column]) if last_non_blank_column is not None else ""

            weight = str(row['Weight'])

            # Exclude entries with blank values
            if any(is_nan(val) for val in [word, last_non_blank_column_name, weight]):
                continue

            # Check if the Word entry already exists in the dictionary
            if word in word_dict:
                current_dict = word_dict[word]
            else:
                # If Word entry does not exist, create a new entry in the dictionary
                current_dict = {
                    "name": word,
                    "children": []
                }
                word_dict[word] = current_dict

            # Create nested children structure until the last non-blank column
            current_children = current_dict["children"]
            # Create nested children structure until the last non-blank column
            if last_non_blank_column is not None:
                for col in df.columns[2:df.columns.get_loc(last_non_blank_column)]:
                    col_value = str(row[col])
                    if not is_nan(col_value):
                        nested_dict = next((child for child in current_children if child["name"] == col_value), None)
                        if nested_dict:
                            current_children = nested_dict.get("children", [])
                        else:
                            new_dict = {"name": col_value, "children": []}
                            current_children.append(new_dict)
                            current_children = new_dict["children"]

            # Add the last entry with its Weight
            current_children.append({
                "name": last_non_blank_column_name,
                "value": weight
            })

        # Add the Word entries to the main JSON structure
        if word_dict:
            topic_data["children"].extend(word_dict.values())
            json_data["children"].append(topic_data)

    # Convert the dictionary to JSON and write to a file
    with open(output_json, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

# Example usage:
csv_input_file = r'C:\Users\PABLO\OneDrive - UCL\ECOS 2024\Radial tree diagram\January_25_01.csv'
json_output_file = r'C:\Users\PABLO\OneDrive - UCL\ECOS 2024\Radial tree diagram\output.json'
csv_to_json(csv_input_file, json_output_file)