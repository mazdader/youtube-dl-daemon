from yt_tools import yt_logger, yt_db
import youtube_dl

class yt_Downloader:
    def __init__(self):
        self.logger = yt_logger.yt_Logger()
        self.db = yt_db.yt_DB_my()
        pass

    def download_videos(self):
        """videolist = self.db.get_all_videos(self.db.STATUS_NEW)"""
        videolist = self.db.get_all_videos()
        print videolist
        for video in videolist:
            video = video[0]
            print video
            self.logger.log('Starting download of video ' + video)
            self.db.change_video_status(video, self.db.STATUS_DOWNLOADING)
            self.logger.log('Done loading of video ' + video)
            self.db.change_video_status(video, self.db.STATUS_DONE)
        return True

