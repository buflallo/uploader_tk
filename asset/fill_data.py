import os
import pandas as pd


# Define the directory where the videos are stored
Data = "data.xlsx"
videos_dir = "videos/"
cookies_dir = "cookies/"
path= "asset/"

with open("desc.txt") as f:
    descriptions = [line.strip() for line in f.readlines()]
# Get a list of all the video file names and cookies in the directory
video_files = [os.path.join(path, videos_dir, f) for f in os.listdir(videos_dir) if os.path.isfile(os.path.join(videos_dir, f)) and f.endswith(".mp4")]
cookie_files = [os.path.join(path, cookies_dir, f) for f in os.listdir(cookies_dir) if os.path.isfile(os.path.join(cookies_dir, f)) and f.endswith(".txt")]

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(Data)
j = 0


#iterate through the cookies and add them to cookies_list
cookies_list = []
for cookie_file in cookie_files:
    if cookie_file in df['cookies'].values:
        continue
    else:
        cookies_list.append(cookie_file)

# iterate through video_files and adds missing videos to videos_list
videos_list = []
for video_file in video_files:
    if video_file not in df['file_path'].values:
        videos_list.append(video_file)

# Iterate through the video files and add their paths to the file_path column

for i, video_file in enumerate(videos_list):
        df = df._append({'file_path': video_file, 'cookies': cookies_list[i], 'description': descriptions[i], 'uploaded': False}, ignore_index=True)

# Save the DataFrame to the Excel file
df.to_excel(Data, index=False)

print("Done")
