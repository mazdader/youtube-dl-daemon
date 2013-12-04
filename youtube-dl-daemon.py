from yt_tools import yt_poller, yt_db, yt_downloader
import time

if __name__ == '__main__':

    poller = yt_poller.yt_Poller("mazdader")
    downloader = yt_downloader.yt_Downloader()

    interval = 0
    count = 1

    while count > 0:
        poller.get_new_videos()
        downloader.download_videos()
        time.sleep(interval)
        count -= 1
