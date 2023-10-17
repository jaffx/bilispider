from .. import *
from ...data import dataBili
import threading


class TaskSpiderUPVidInPop(TaskBase):
    __taskName__ = "热门页UP主&视频信息爬取"

    def __init__(self, UPLimited=400, videoLimited=200):
        super(TaskSpiderUPVidInPop, self).__init__()
        self.UPLimited = UPLimited
        self.videoLimited = videoLimited

    def main(self):
        dBili = dataBili.dataBili()

        def getUPInfos():
            upInfos = dBili.upInfosInPopList(self.UPLimited, sleepDuration=1)
            print(f"获取UP主数量{len(upInfos)}")
            succ = dBili.saveUPInfos(upInfoList=upInfos)
            print(f"保存UP主数量{succ}")

        def getVideoInfos():
            vInfos = dBili.videoInfosInPopList(self.videoLimited)
            print(f"获取视频数量{len(vInfos)}")
            succ = dBili.saveVideoInfo(vInfoList=vInfos)
            print(f"保存视频数量{succ}")

        t1 = threading.Thread(target=getUPInfos, args=())
        t2 = threading.Thread(target=getVideoInfos, args=())
        t1.start(), t2.start()
        t1.join(), t2.join()
