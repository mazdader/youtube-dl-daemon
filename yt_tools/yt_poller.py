from yt_tools import yt_logger, yt_db
from xml.dom import minidom
import urllib

class yt_Poller:
    def __init__(self, yt_user):
        self.logger = yt_logger.yt_Logger()
        self.db = yt_db.yt_DB_my()
        self.videolist = []
        self.yt_user = yt_user
        self.url = "http://gdata.youtube.com/feeds/api/users/" + yt_user + "/newsubscriptionvideos"

    def get_all_videos(self):
        self.logger.log('Polling Youtube feed with videos')
        self.videolist = []
        xmldoc = minidom.parse(urllib.urlopen(self.url))
        itemlist = xmldoc.getElementsByTagName('link')
        for s in itemlist :
            if s.attributes['rel'].value == 'alternate' and s.attributes['href'].value != 'http://www.youtube.com/subscription_center':
                self.videolist.append(s.attributes['href'].value.split('&')[0].split('v=')[1])
        return tuple(self.videolist)

    def get_new_videos(self):
        self.logger.log('Adding new videos to database')

        new_videos = []
        for id_video in self.get_all_videos():
            if not self.db.video_exists(id_video):
                new_videos.append(id_video)

        if len(new_videos) > 0:
            self.db.add_videos(new_videos)
            self.logger.log('Added ' + str(len(new_videos)) + ' videos to database')

