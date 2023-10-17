import queue
import random

from . import *
import threading
import concurrent.futures as future

URL_VIDEO_INFO = "https://api.bilibili.com/x/web-interface/view"


class videoClnt(biliClnt):
    def __init__(self):
        biliClnt.__init__(self)

    def getVideoInfo(self, bvid: str) -> (dict | None):
        params = {
            "bvid": bvid
        }
        body = self.get(url=URL_VIDEO_INFO, params=params)
        if body is None:
            self.logger.error(f"getVideoInfo for {bvid} failed!")
            return None
        data = body['data']
        videoInfor = {
            "aid": data["aid"],
            "bvid": bvid,
            "tid": data["tid"],
            "tname": data["tname"],
            "pic": data["pic"],
            "title": data["title"],
            "pubdate": data["pubdate"],
            "desc": data["desc"],
            "duration": data["duration"],
            "upname": data["owner"]["name"],
            "mid": data["owner"]["mid"],
            "like": data["stat"]["like"],
            "coin": data["stat"]["coin"],
            "favorite": data["stat"]["favorite"],
            "share": data["stat"]["share"],
            "view": data["stat"]["view"],
            "danmaku": data["stat"]["danmaku"],
            "reply": data["stat"]["reply"],
            "his_rank": data["stat"]["his_rank"]
        }
        return videoInfor

    def getVideoInfosWithTheadingPool(self, bvidList):
        assert len(bvidList) < 10000, "视频数量不能超过10000"

        # 初始化线程数量,最多不超过5个
        threadNum = min(len(bvidList) // 10 + 1, 5)
        # 初始化任务队列
        taksQueue = queue.Queue()
        for bvid in bvidList:
            taksQueue.put(bvid)
        # 读写锁
        readLock = threading.Lock()
        writeLock = threading.Lock()
        # 任务结果产物
        infoList = []

        def _work():
            while True:
                with readLock:
                    if taksQueue.empty():
                        break
                    _vBvid = taksQueue.get()
                try:
                    info = self.getVideoInfo(_vBvid)
                except Exception:
                    self.logger.error("Get video info error!")
                    continue
                with writeLock:
                    infoList.append(info)
                time.sleep(random.random())

        ths = []
        for _ in range(threadNum):
            th = threading.Thread(target=_work, args=())
            ths.append(th)
            th.start()
        for th in ths:
            th.join()
        return infoList
