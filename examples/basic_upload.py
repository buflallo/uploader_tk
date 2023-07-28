"""Gets a video from the internet and uplaods it"""
import urllib.request

from src.tiktok_uploader.upload import upload_video
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# URL = "https://download-video.akamaized.net/2/download/cc655524-b05b-4a25-9968-a739e5caa133/e7fa5462-c0da9187/pexels-nathan-j-hilton-17512964%20%282160p%29.mp4?__token__=st=1689384973~exp=1689465214~acl=%2F2%2Fdownload%2Fcc655524-b05b-4a25-9968-a739e5caa133%2Fe7fa5462-c0da9187%2Fpexels-nathan-j-hilton-17512964%2520%25282160p%2529.mp4%2A~hmac=14f8f4d3df96d8bb707fdc76a0e851ea8ff11092b69254eadac0f1acf608d836&r=dXMtY2VudHJhbDE%3D"
FILENAME = "Download.mp4"

if __name__ == "__main__":
    # download random video
    # urllib.request.urlretrieve(URL, FILENAME)

    # upload video to TikTok
    upload_video(FILENAME,
                 description="lorem ipsum dolor sit amet",
                 cookies="cookies.txt")
