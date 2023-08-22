"""
Uploads a series of videos to TikTok
"""
from sys import argv
import toml

import pandas as pd
import time

from src.tiktok_uploader.upload import upload_video
from src.tiktok_uploader import logger
from src.tiktok_uploader.utils import green
from src.tiktok_uploader import config

# NOTE: A TOML file with the following information also works
# Good for when you have multiple accounts
INFO = "asset/data.xlsx"
KEY = "Max_upload"
class Account:
        def __init__(self, max_upload, account_ck, start_time):
            self.max_upload = max_upload
            self.account_ck = account_ck
            self.start_time = start_time

def fcl():
    print (green("folow and like"))
    time.sleep(20)

def main():
    """
    Posts a video to TikTok from INFO, a spreadsheet containing: file_path, description, and uploaded
    """
    # set_config() # Sets global variables based on arguments parsed from the command line

    # Load the Excel file into a pandas DataFrame, skipping the first row
    frame = pd.read_excel(INFO)
    
    # Create an account object and set its values

    account = Account(frame[KEY][0], frame['Account'][0], frame['Start_time'][0])
    f_tmp = pd.read_excel(INFO).iloc[1:]
    i=1
    # print("Starting to upload videos")
#6
#1
    while True:
        frame = f_tmp[i-1:]
        i=1
        it = 1
        for index, video_info in frame.iterrows() :
            # print (max_upload)
            print (f"Uploading {video_info['Video_path']} in {account.account_ck} {i}th video")
            i+=1
            if (video_info['Uploaded'] == 1):
                continue
            if it > account.max_upload:
                break

            failed = upload_video(video_info['Video_path'], video_info['Description'], cookies=account.account_ck)
            if len(failed) > 0 :
                if i >= 1:
                    i -= 1
                    break
                else:
                    break
            else:
                it += 1
                fcl()
            # # Update the DataFrame
            frame.at[index, 'Uploaded'] = 1 # Update the uploaded column with the number of videos that were uploaded
            frame.to_excel(INFO, index=False) # Saves the DataFrame to the Excel file
            # time.sleep(20) # Sleeps for 10 seconds between each account
        if it > account.max_upload:
            break

if __name__ == '__main__':
    main()
