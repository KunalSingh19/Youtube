import json

def extract_reels_links(json_file, excluded_users):
    reels_links = []

    with open(json_file, 'r') as file:
        try:
            # Load the entire JSON content
            data = json.load(file)

            # Check if 'likes_media_likes' is in the data
            if 'likes_media_likes' in data:
                for item in data['likes_media_likes']:
                    # Check if the user is in the excluded list
                    if item.get('title') in excluded_users:
                        continue

                    # Extract the Reels link from 'string_list_data'
                    for string_data in item.get('string_list_data', []):
                        if 'href' in string_data:
                            reels_links.append(string_data['href'])

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    return reels_links

def save_links_to_file(links, output_file):
    with open(output_file, 'w') as file:
        for link in links:
            file.write(link + '\n')

if __name__ == "__main__":
    # Specify the path to your JSON file and the users to exclude
    json_file_path = 'liked_posts.json'
    excluded_users = [
        'it.zkai', 'pvtt__insaf', 'itz.kunikazu', 'natty_dheeraj', 
        'amitj_jatav_143', 'shourya_sajwan_', 'isuuu848', 'fc__assault', 
        'ay_ush0921', 'anurag__jatav_ji__09', 'itz.kevin._1', 
        '_.priyanshu_rwt_', 'nkx.ansh', 'rose_galaxyy67', 
        'pa_yal_30', 'offical_suraj_0030', 'kingofthakur3456', 
        'aasthakumari1612', 'fuddimaster69', 'ay_xsh0972', 
        'aditya_____124999', 'nayanx919', 'para_sss01', 
        'kanishka___negii', 'itz.kunal_i', 'sakshi_m_27', 
        'nikhilrajput6009', '__gojo__6567', 'itz_kunal_jatav_ji', 
        'karanchaudharyy158', 'yvcyogeshvermaclasses', 
        'aditya_____124999', 'itz.kenkaneki', 'naman_singh6556', 
        'rupali._.1222', 'ileshh.22', 'parasss_7', 'cyborg_d_18', 
        'kalkigamesyt', 'somiljjain10', 'its.evanvale', 
        'aaravv_79', 'its___pandat___ji_', 'satyajeet_baraiya', 
        'mayank_soni150', 'ronak_aum', 'pvtt.palsahab.7434', 
        'its_.gopal20', 'existttenceeeee', '_.rituuuuuu_.08', 
        'rinavgangar'
    ]

    # Output file for links
    output_file_path = 'extracted_reels_links2.txt'

    # Extract the Reels links
    links = extract_reels_links(json_file_path, excluded_users)

    # Save the extracted links to a file
    save_links_to_file(links, output_file_path)

    # Print a message indicating completion
    print(f"Extracted links saved to {output_file_path}")
