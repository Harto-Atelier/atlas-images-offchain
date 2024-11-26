import json
import argparse
import sys

def read_ids(ids_file_path):
    """
    Reads IDs from a text file, one ID per line.
    Returns a list of IDs.
    """
    try:
        with open(ids_file_path, 'r', encoding='utf-8') as f:
            ids = [line.strip() for line in f if line.strip()]
        return ids
    except FileNotFoundError:
        print(f"Error: The file '{ids_file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{ids_file_path}': {str(e)}")
        sys.exit(1)

def read_json(json_file_path):
    """
    Reads a JSON file and returns its content as a Python list.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"Error: Expected the JSON file to contain a list of objects.")
            sys.exit(1)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON file '{json_file_path}': {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{json_file_path}': {str(e)}")
        sys.exit(1)

def write_json(data, output_file_path):
    """
    Writes the Python list of dictionaries to a JSON file with indentation.
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully wrote updated JSON to '{output_file_path}'.")
    except Exception as e:
        print(f"Error writing to '{output_file_path}': {str(e)}")
        sys.exit(1)

def replace_ids_in_json(json_data, new_ids):
    """
    Replaces the 'id' fields in the JSON data with new IDs from the list.
    """
    if len(json_data) != len(new_ids):
        print(f"Error: Number of IDs ({len(new_ids)}) does not match number of JSON entries ({len(json_data)}).")
        sys.exit(1)
    
    for index, (entry, new_id) in enumerate(zip(json_data, new_ids), start=1):
        old_id = entry.get('id', None)
        if old_id is not None:
            entry['id'] = new_id
        else:
            print(f"Warning: Entry #{index} does not have an 'id' field.")
    
    return json_data

def main():
    parser = argparse.ArgumentParser(description="Replace 'id' fields in a JSON file with new IDs from a text file.")
    parser.add_argument('json_file', help='Path to the input JSON file (e.g., atlas_collection.json).')
    parser.add_argument('ids_file', help='Path to the text file containing new IDs (one per line).')
    parser.add_argument('-o', '--output', default='atlas_collection_updated.json', help='Path to the output JSON file. Default is "atlas_collection_updated.json".')
    
    args = parser.parse_args()
    
    # Read new IDs
    new_ids = read_ids(args.ids_file)
    print(f"Number of new IDs read: {len(new_ids)}")
    
    # Read JSON data
    json_data = read_json(args.json_file)
    print(f"Number of JSON entries read: {len(json_data)}")
    
    # Replace IDs
    updated_json = replace_ids_in_json(json_data, new_ids)
    
    # Write updated JSON
    write_json(updated_json, args.output)

if __name__ == "__main__":
    main()