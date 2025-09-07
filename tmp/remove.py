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

# ['it.zkai', 'pvtt__insaf', 'itz.kunikazu', 'natty_dheeraj', 'amitj_jatav_143', 'shourya_sajwan_', 'isuuu848', 'fc__assault', 'ay_ush0921', 'anurag__jatav_ji__09', 'itz.kevin._1', '_.priyanshu_rwt_', 'nkx.ansh', 'rose_galaxyy67', 'pa_yal_30', 'offical_suraj_0030', 'kingofthakur3456', 'aasthakumari1612', 'fuddimaster69', 'ay_xsh0972', 'aditya_____124999', 'nayanx919', 'para_sss01', 'kanishka___negii', 'itz.kunal_i']

# ['sakshi_m_27', 'it.zkai', 'nikhilrajput6009', '__gojo__6567', 'itz_kunal_jatav_ji', 'karanchaudharyy158', 'amitj_jatav_143', 'itz.kunikazu', 'natty_dheeraj', 'yvcyogeshvermaclasses', 'shourya_sajwan_', 'anurag__jatav_ji__09', 'itz.kevin._1', '_priiya18', '_.priyanshu_rwt_', 'aasthakumari1612', 'ay_xsh0972', 'kingofthakur3456', 'aditya_____124999', 'nkx.ansh', 'itz.kenkaneki', 'naman_singh6556', 'rose_galaxyy67', 'rupali._.1222', 'ileshh.22', 'ay_ush0921', 'parasss_7', 'cyborg_d_18', 'kalkigamesyt', 'fuddimaster69', 'somiljjain10', 'its.evanvale', 'aaravv_79', 'its___pandat___ji_', 'satyajeet_baraiya', 'mayank_soni150', 'ronak_aum', 'pvtt.palsahab.7434', 'its_.gopal20', 'existttenceeeee', 'kanishka___negii', '_.rituuuuuu_.08', 'rinavgangar']
