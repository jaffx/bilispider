import threading

from . import *

# 获取热门列表
API_POPULAR_LIST = "https://api.bilibili.com/x/web-interface/popular"


class popularClnt(biliClnt):
    popAllLock = threading.Lock()

    def __init__(self):
        biliClnt.__init__(self)

    def getPopListByPage(self, pageSize=20, pageNo=1) -> (list, bool):
        params = {
            "ps": pageSize,
            "pn": pageNo,
        }
        body = self.get(API_POPULAR_LIST, params=params)
        if not body:
            self.logger.error(f"getPopularList1Page error, page ={pageNo}, page_size={pageSize}")
            return None, True
        vList, noMore = body['data']['list'], body['data']['no_more']
        # self.logger.info(f"Popular list page {pageNo}, page_size {pageSize}, get {len(vList)} videos in this Page")
        return vList, noMore

    def getPopListAll(self, limited: int = 1e4, noCache=False) -> list:
        """
        :param limited: 最多返回多少条数据，默认10000
        :param noCache: 不走cache
        :return:
        """
        cacheKey = f"popularList"

        if not noCache:
            result = self.ttlCache.get(cacheKey)
            if result is not None:
                return result
        # 以下代码互斥访问
        with self.popAllLock:
            # DCL
            if not noCache:
                result = self.ttlCache.get(cacheKey)
                if result is not None:
                    return result
            pageNo = 1
            pageSize = limited if limited < 40 else 20
            noMore = False
            videoList = []
            try:
                while not noMore and len(videoList) < limited:
                    vList, noMore = self.getPopListByPage(pageNo=pageNo, pageSize=pageSize)
                    if not vList:
                        continue
                    videoList.extend(vList)
                    pageNo += 1
            except Exception as e:
                self.logger.warning(f"getPopListAll failed for reason {e}")
            self.ttlCache[cacheKey] = videoList
        return videoList

    def videoIDInPopList(self, limited=1000) -> (list | None):
        popList = self.getPopListAll(limited)
        if not popList:
            self.logger.error("Get popular list failed!")
            return None
        aids = [{"aid": v["aid"], "bvid": v["bvid"]} for v in popList]
        return aids

    def bvidInPopList(self, limited=1000) -> (list | None):
        popList = self.getPopListAll(limited)
        if not popList:
            self.logger.error("Get popular list failed!")
            return None
        bvids = [v["bvid"] for v in popList]
        return bvids

    def upIDInPopList(self, limited=100) -> (list | None):
        popList = self.getPopListAll(limited=limited)
        if not popList:
            self.logger.error("Get popular list failed!")
            return None
        upIds = [v["owner"]["mid"] for v in popList]
        return upIds
