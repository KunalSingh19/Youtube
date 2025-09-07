import os
import json

# Function to extract usernames from JSON files
def extract_usernames_from_json(folder_path):
    usernames = []

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Extract usernames from the string_list_data
                for item in data:
                    if 'string_list_data' in item:
                        for user in item['string_list_data']:
                            usernames.append(user['value'])

    return usernames

# Specify the folder containing the JSON files
folder_path = 'followers_and_following-20250827T141408Z-1-001/followers_and_following1'

# Call the function and print the result
usernames_array = extract_usernames_from_json(folder_path)
print(usernames_array)
