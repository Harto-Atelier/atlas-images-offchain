import json
import argparse
import re
import sys

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

def update_image_url(url):
    """
    Updates the image URL by:
    1. Replacing 'atlas-offchain-images' with 'atlas-images-offchain'.
    2. Inserting a hyphen between 'Atlas' and the seed number in the image filename.
    
    Example:
    'https://harto-atelier.github.io/atlas-offchain-images/images/Atlas0.png'
    → 'https://harto-atelier.github.io/atlas-images-offchain/images/Atlas-0.png'
    """
    # Step 1: Replace 'atlas-offchain-images' with 'atlas-images-offchain'
    updated_url = url.replace('atlas-offchain-images', 'atlas-images-offchain')
    
    # Step 2: Insert a hyphen between 'Atlas' and the seed number in the image filename
    # Regex Pattern Explanation:
    # (Atlas) - Captures 'Atlas'
    # (\d+) - Captures one or more digits (seed number)
    # (\.png)$ - Ensures the string ends with '.png'
    pattern = r'(Atlas)(\d+)(\.png)$'
    replacement = r'\1-\2\3'
    updated_url, count = re.subn(pattern, replacement, updated_url)
    
    if count == 0:
        print(f"Warning: URL '{url}' does not match the expected pattern for filename modification.")
    
    return updated_url

def replace_image_urls(json_data):
    """
    Replaces the 'image' URLs in the JSON data by updating folder name and inserting hyphens.
    Returns the updated JSON data and the count of updated URLs.
    """
    updated_count = 0
    for index, entry in enumerate(json_data, start=1):
        meta = entry.get('meta', {})
        image_url = meta.get('image', '')
        if image_url:
            new_image_url = update_image_url(image_url)
            if new_image_url != image_url:
                json_data[index - 1]['meta']['image'] = new_image_url
                updated_count += 1
        else:
            print(f"Warning: Entry #{index} does not have an 'image' field.")
    return json_data, updated_count

def main():
    parser = argparse.ArgumentParser(description="Update 'image' URLs in a JSON file by replacing folder name and inserting hyphens in filenames.")
    parser.add_argument('json_file', help='Path to the input JSON file (e.g., updated_atlas_collection.json).')
    parser.add_argument('-o', '--output', default='updated_atlas_collection_urls.json', help='Path to the output JSON file. Defaults to "updated_atlas_collection_urls.json".')
    
    args = parser.parse_args()
    
    # Read JSON data
    json_data = read_json(args.json_file)
    print(f"Number of JSON entries read: {len(json_data)}")
    
    # Replace image URLs
    updated_json, updated_count = replace_image_urls(json_data)
    print(f"Number of image URLs updated: {updated_count}")
    
    # Write updated JSON
    write_json(updated_json, args.output)

if __name__ == "__main__":
    main()