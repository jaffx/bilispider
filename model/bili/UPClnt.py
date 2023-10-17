import threading

from . import *

# 获取up主基本信息
URL_UP_INFO = "https://api.bilibili.com/x/space/wbi/acc/info"
# 获取up主关注、粉丝信息
URL_UP_RELATION = "https://api.bilibili.com/x/relation/stat"
# 获取up主导航栏数据，视频量等
URL_UP_NAVNUM = "https://api.bilibili.com/x/space/navnum"


class UPClnt(biliClnt):
    def __init__(self):
        biliClnt.__init__(self)

    def getUPBaseInfo(self, mid: int):
        params = {
            "mid": mid
        }
        body = self.get(url=URL_UP_INFO, params=params)
        if body is None:
            self.logger.warning("获取UP主基本信息失败")
            return None
        data = body["data"]
        return {
            "name": data["name"],
            "mid": data["mid"],
            "sex": data["sex"],
            "sign": data["sign"],
            "level": data["level"],
            "title": data["official"]["title"],
            "face": data["face"]
        }

    def getUPVideoNum(self, mid: int):
        params = {
            "mid": mid
        }
        body = self.get(url=URL_UP_NAVNUM, params=params)
        if body is None:
            self.logger.warning("获取UP主视频数量失败")
            return None
        data = body["data"]
        return data["video"]

    def getUPFollowerNum(self, mid: int):
        params = {
            "vmid": mid
        }
        body = self.get(url=URL_UP_RELATION, params=params)
        if body is None:
            self.logger.warning("获取UP主粉丝量失败")
            return None
        data = body["data"]
        return data["follower"]

    def getUPInfo(self, mid: int):
        upInfo, follower = {}, -1

        def f1():
            nonlocal upInfo
            upInfo = self.getUPBaseInfo(mid)

        def f2():
            nonlocal follower
            follower = self.getUPFollowerNum(mid)

        t1, t2 = threading.Thread(target=f1), threading.Thread(target=f2)
        t1.start(), t2.start()
        t1.join(), t2.join()
        upInfo["follower"] = follower
        return upInfo
