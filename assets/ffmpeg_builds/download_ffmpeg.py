import os
import sys
import platform
from dotenv import load_dotenv, find_dotenv
from urllib.request import urlopen, urlretrieve

from zipfile import ZipFile
import tarfile

load_dotenv(find_dotenv())
PROJECT_PATH = os.getenv("PROJECT_PATH")
sys.path.append(PROJECT_PATH)  # to make the util module recognizeable by python path
from discord_bot.main.util.Environment import find_binary

def download_ffmpeg():
    base_path = os.path.dirname(os.path.abspath(__file__))
    system = platform.system().lower()
    
    if system == 'windows':
        download_url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' # return .zip file
        extract_folder = os.path.join(base_path, 'ffmpeg-windows')
    elif system == 'darwin':
        download_url = 'https://evermeet.cx/ffmpeg/getrelease/zip' # return .zip file
        extract_folder = os.path.join(base_path, 'ffmpeg-macos')
    elif system == 'linux':
        download_url = 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz' # return .tar.xz file
        extract_folder = os.path.join(base_path, 'ffmpeg-linux')
    
    else:
        print(f"Unsupported operating system: {system}")
        return None
    
    try:
        if not os.path.isdir(extract_folder):
            print(f"Downloading {download_url}...")
            response = urlopen(download_url)
            file_size = int(response.headers['Content-Length'])
            print(f"File size: {file_size / (1024 * 1024):.2f} MB")
            
            def progress_callback(count, block_size, total_size): # User feedback
                progress = count * block_size
                percent = (progress / total_size) * 100
                print(f"\rDownloading... {percent:.2f}% complete", end='', flush=True)
            
            if system == 'windows' or system == 'darwin':
                ext = 'zip'
            elif system == 'linux':
                ext = 'tar.xz'
            
            urlretrieve(download_url, os.path.join(base_path, f'ffmpeg.{ext}'), reporthook=progress_callback)
            
            print(f"\nUnpacking ffmpeg.{ext} into {extract_folder}")
            if system == 'windows' or system == 'darwin':
                # Extract the zip file
                with ZipFile(os.path.join(base_path, f'ffmpeg.{ext}'), 'r') as zip:
                    zip.extractall(extract_folder)
            elif system == 'linux':
                # Extract the tar.xz file
                with tarfile.open(os.path.join(base_path, f'ffmpeg.{ext}')) as tar:
                    tar.extractall(extract_folder)
                
            os.remove(os.path.join(base_path, f'ffmpeg.{ext}'))
            
            print("FFmpeg has been downloaded and extracted successfully.")
        return find_binary(extract_folder, "ffmpeg")
        
    except Exception as e:
        print(f"Error downloading FFmpeg: {e}")
        return None
    
if __name__ == "__main__":
    # os.environ['FFMPEG'] = download_ffmpeg() # save as environ variable
    print(download_ffmpeg())