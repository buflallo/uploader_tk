"""
Uploads a series of videos to TikTok
"""
from sys import argv
import toml

import pandas as pd
import time

from tiktok_uploader.upload import upload_video

# NOTE: A TOML file with the following information also works
# Good for when you have multiple accounts
INFO = "./data.xlsx"
KEY = "uploaded"
PROXY = "./socks5_proxies.txt"

def main():
    """
    Posts a video to TikTok from INFO, a spreadsheet containing: file_path, description, and uploaded
    """
    set_config() # Sets global variables based on arguments parsed from the command line

    # read from the console and do an infinite loop that sleeps 10 seconds between each iteration
    frame = pd.read_excel(INFO)
    
    for index, video_info in frame[frame[KEY] == False].iterrows():
        failed = upload_video(video_info['file_path'], video_info['description'], cookies=video_info['cookies'], proxy=video_info['cookies'])
        if not failed:
            frame.at[index, KEY] = True # Registers the video has been uploaded
        time.sleep(10) # Sleeps for 10 seconds between each iteration

    frame.to_excel(INFO)


# checks if the user passed in a file path
def set_config() -> dict:
    """
    Gets the optional file path from the command line
    """
    if len(argv) < 2 or not argv[1].endswith('.toml'):
        print("No file path was provided")
        return

    try:
        dictionary = toml.load(argv[1])
    except toml.decoder.TomlDecodeError as e:
        print(f"Error loading TOML file: {e}")
        return
        
        
    INFO = dictionary['INFOAC']
    KEY = dictionary['KEY']
    PROXY = dictionary['PROXY']

if __name__ == '__main__':
    main()
